import reflex as rx
import unittest
from app.states.canteen_state import CanteenState
from app.states.demo_records import DEMO_ORGANIZATIONS


class NgoDemoTests(unittest.TestCase):
    def setUp(self):
        self.state = CanteenState(_reflex_internal_init=True)
        CanteenState.save_surplus.fn(
            self.state,
            "F01",
            {
                "listed": "32",
                "start": "12:30",
                "end": "13:30",
                "status": "Available",
                "handling": "Simulated covered containers",
                "reviewed": "on",
            },
        )

    def request(self, quantity="10"):
        CanteenState.create_request.fn(
            self.state,
            "F01",
            {"quantity": quantity, "notes": "Sample packaging and pickup plan"},
        )

    def progress(self, action):
        CanteenState.progress_request.fn(
            self.state, self.state.requests[0]["id"], action
        )

    def test_directory(self):
        self.assertEqual(len(DEMO_ORGANIZATIONS), 15)
        self.assertEqual(len({row["id"] for row in DEMO_ORGANIZATIONS}), 15)
        self.assertEqual(len({row["name"] for row in DEMO_ORGANIZATIONS}), 15)
        self.assertTrue(
            all("Fictional" in row["name"] for row in DEMO_ORGANIZATIONS)
        )
        self.assertEqual(self.state.approved_organizations, 10)
        CanteenState.filter_directory.fn(self.state, "Pending")
        self.assertEqual(len(self.state.directory), 5)
        CanteenState.search_directory.fn(self.state, "not-a-real-profile")
        self.assertEqual(self.state.directory, [])
        self.state.organizations[0]["approved"] = False
        self.assertNotIn(
            self.state.organizations[0]["name"], self.state.partners
        )

    def test_approval_and_quantity_guards(self):
        self.state.organization_id = DEMO_ORGANIZATIONS[2]["id"]
        self.request()
        self.assertEqual(self.state.requests, [])
        self.state.organization_id = DEMO_ORGANIZATIONS[0]["id"]
        for quantity in ("0", "-1", "1.2", "33", ""):
            self.request(quantity)
            self.assertEqual(self.state.requests, [])
        self.state.operations[0]["reviewed"] = False
        self.request()
        self.assertEqual(self.state.requests, [])

    def test_reservation_and_release(self):
        self.request("20")
        self.assertEqual(self.state.totals["available"], 12)
        self.request("13")
        self.assertEqual(len(self.state.requests), 1)
        before = dict(self.state.operations[0])
        CanteenState.simulate_collection.fn(self.state, "F01")
        self.assertEqual(self.state.operations[0], before)
        CanteenState.save_surplus.fn(self.state, "F01", {"listed": "0"})
        self.assertEqual(self.state.operations[0], before)
        self.progress("cancel")
        self.assertEqual(self.state.totals["available"], 32)
        self.assertEqual(self.state.collection_history, [])
        self.progress("approve")
        self.assertEqual(self.state.requests[0]["status"], "Cancelled")

    def test_collection_workflow_and_balance(self):
        self.request()
        self.progress("collect")
        self.assertEqual(self.state.requests[0]["status"], "Pending")
        self.progress("approve")
        self.progress("confirm")
        self.progress("collect")
        self.assertEqual(self.state.operations[0]["listed"], 22)
        self.assertEqual(self.state.operations[0]["collected"], 28)
        self.assertEqual(len(self.state.collection_history), 1)
        self.progress("collect")
        self.assertEqual(self.state.operations[0]["collected"], 28)
        totals = self.state.totals
        self.assertEqual(
            totals["prepared"],
            totals["sold"] + totals["collected"] + totals["remaining"],
        )

    def test_revoked_approval_and_rejection(self):
        self.request()
        self.state.organizations[0]["approved"] = False
        self.progress("approve")
        self.assertEqual(self.state.requests[0]["status"], "Pending")
        self.progress("reject")
        self.assertEqual(self.state.totals["available"], 32)

    def test_messages_share_thread(self):
        CanteenState.compose_ngo_message.fn(
            self.state, {"message": "Local NGO plan"}
        )
        self.assertEqual(self.state.conversation[-1]["side"], "ngo")
        CanteenState.compose_message.fn(
            self.state, {"message": "Local canteen reply"}
        )
        self.assertTrue(
            any(
                row["text"] == "Local canteen reply"
                for row in self.state.ngo_conversation
            )
        )


if __name__ == "__main__":
    unittest.main()
