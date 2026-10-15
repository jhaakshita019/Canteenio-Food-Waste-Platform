import reflex as rx
import unittest
from app.states.canteen_state import CanteenState


class CanteenDemoTests(unittest.TestCase):
    def setUp(self):
        self.state = CanteenState(_reflex_internal_init=True)

    def assert_balance(self):
        for row in self.state.operations:
            remaining = row["prepared"] - row["sold"] - row["collected"]
            self.assertGreaterEqual(remaining, 0)
            self.assertGreaterEqual(row["listed"], 0)
            self.assertLessEqual(row["listed"], remaining)
        totals = self.state.totals
        self.assertEqual(
            totals["prepared"],
            totals["sold"] + totals["collected"] + totals["remaining"],
        )

    def test_seed_balance(self):
        self.assert_balance()
        self.assertEqual(self.state.totals["remaining"], 96)
        self.assertEqual(self.state.totals["available"], 0)

    def test_prepare_sales_and_surplus_protection(self):
        CanteenState.quick_update.fn(self.state, "F01", "sell")
        self.assertTrue(self.state.error)
        CanteenState.quick_update.fn(self.state, "F01", "prepare")
        CanteenState.quick_update.fn(self.state, "F01", "sell")
        self.assertFalse(self.state.error)
        self.assertEqual(self.state.totals["remaining"], 101)
        self.assert_balance()

    def test_invalid_inventory_edits_are_atomic(self):
        before = [dict(row) for row in self.state.operations]
        for value in ("-1", "2.5", "", "100001"):
            CanteenState.save_operation.fn(
                self.state,
                "F01",
                {"name": "Food", "prepared": value, "sold": "0"},
            )
            self.assertTrue(self.state.error)
            self.assertEqual(self.state.operations, before)
        CanteenState.save_operation.fn(
            self.state, "F01", {"name": "Food", "prepared": "1", "sold": "1"}
        )
        self.assertEqual(self.state.operations, before)

    def test_review_and_simulated_collection(self):
        data = {
            "listed": "32",
            "start": "12:30",
            "end": "13:30",
            "status": "Available",
            "handling": "Illustrative covered containers",
        }
        CanteenState.save_surplus.fn(self.state, "F01", data)
        self.assertTrue(self.state.error)
        data["reviewed"] = "on"
        CanteenState.save_surplus.fn(self.state, "F01", data)
        self.assertEqual(self.state.totals["available"], 32)
        prepared = self.state.totals["prepared"]
        CanteenState.simulate_collection.fn(self.state, "F01")
        self.assertEqual(self.state.totals["available"], 0)
        self.assertEqual(self.state.totals["remaining"], 64)
        self.assertEqual(self.state.totals["collected"], 87)
        self.assertEqual(self.state.totals["prepared"], prepared)
        self.assert_balance()

    def test_bad_window_does_not_change_listing(self):
        before = dict(self.state.operations[0])
        CanteenState.save_surplus.fn(
            self.state,
            "F01",
            {
                "listed": "10",
                "start": "15:00",
                "end": "14:00",
                "status": "Draft",
            },
        )
        self.assertTrue(self.state.error)
        self.assertEqual(self.state.operations[0], before)

    def test_branch_estimates_and_validation(self):
        row = self.state.breaks[0]
        CanteenState.save_break.fn(
            self.state,
            row["id"],
            {"attendance": "101", "start": "12:00", "end": "12:30"},
        )
        self.assertTrue(self.state.error)
        CanteenState.save_break.fn(
            self.state,
            row["id"],
            {"attendance": "0", "start": "12:00", "end": "12:30"},
        )
        self.assertEqual(self.state.breaks[0]["expected"], 0)
        self.assert_balance()

    def test_messages_and_announcements_are_local(self):
        CanteenState.compose_message.fn(self.state, {"message": "   "})
        self.assertTrue(self.state.error)
        CanteenState.compose_message.fn(
            self.state, {"message": "What is available?"}
        )
        self.assertIn(
            "no partner received", self.state.conversation[-1]["text"]
        )
        CanteenState.save_announcement.fn(
            self.state,
            "",
            {
                "title": "Sample reminder",
                "text": "Review surplus drafts",
                "audience": "Canteen team",
            },
        )
        self.assertEqual(len(self.state.announcements), 1)
        notice_id = self.state.announcements[0]["id"]
        CanteenState.save_announcement.fn(
            self.state,
            notice_id,
            {
                "title": "Edited reminder",
                "text": "Local edit",
                "audience": "All demo roles",
            },
        )
        self.assertEqual(len(self.state.announcements), 1)
        CanteenState.remove_announcement.fn(self.state, notice_id)
        self.assertEqual(self.state.announcements, [])


if __name__ == "__main__":
    unittest.main()
