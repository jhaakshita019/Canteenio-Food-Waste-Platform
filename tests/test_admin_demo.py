import reflex as rx
import unittest
from app.states.canteen_state import CanteenState, BRANCHES, YEARS
from app.states.home_state import HomeState


class AdminDemoTests(unittest.TestCase):
    def setUp(self):
        self.state = CanteenState(_reflex_internal_init=True)

    def test_enrollment_distribution_and_slots(self):
        self.assertEqual(len(self.state.breaks), 28)
        self.assertEqual(
            {(row["branch"], row["year"]) for row in self.state.breaks},
            {(branch, year) for branch in BRANCHES for year in YEARS},
        )
        for year, expected in (("FY", 1000), ("SY", 800), ("TY", 0), ("BE", 0)):
            self.assertEqual(
                sum(
                    row["enrolled"]
                    for row in self.state.breaks
                    if row["year"] == year
                ),
                expected,
            )
        self.assertEqual(
            {row["start"] for row in self.state.breaks},
            {"11:15", "12:15", "13:15"},
        )
        self.assertEqual(self.state.student_totals["enrolled"], 1800)

    def test_student_validation_is_atomic_and_estimates_separate(self):
        row_id = self.state.breaks[0]["id"]
        before = dict(self.state.breaks[0])
        data = {
            "enrolled": "100",
            "attendance": "80",
            "visitors_pct": "50",
            "meals_pct": "25",
        }
        for key, bad in (
            ("enrolled", "-1"),
            ("attendance", "101"),
            ("visitors_pct", "1.5"),
            ("meals_pct", ""),
        ):
            CanteenState.save_students.fn(
                self.state, row_id, {**data, key: bad}
            )
            self.assertTrue(self.state.error)
            self.assertEqual(self.state.breaks[0], before)
        sold = self.state.totals["sold"]
        CanteenState.save_students.fn(self.state, row_id, data)
        row = self.state.breaks[0]
        self.assertEqual(
            (row["enrolled"], row["expected"], row["visitors"], row["meals"]),
            (100, 80, 40, 10),
        )
        self.assertEqual(self.state.totals["sold"], sold)

    def test_schedule_changes_do_not_change_enrollment(self):
        row = self.state.breaks[0]
        total = self.state.student_totals["enrolled"]
        CanteenState.save_admin_schedule.fn(
            self.state,
            row["id"],
            {"start": "13:15", "end": "12:15", "active": "on"},
        )
        self.assertTrue(self.state.error)
        CanteenState.save_admin_schedule.fn(
            self.state, row["id"], {"start": "11:15", "end": "12:15"}
        )
        self.assertFalse(self.state.error)
        self.assertFalse(self.state.breaks[0]["active"])
        self.assertEqual(self.state.visible_breaks[0]["end"], "12:15")
        CanteenState.save_break.fn(
            self.state,
            row["id"],
            {"start": "12:15", "end": "12:45", "attendance": "0"},
        )
        self.assertEqual(self.state.student_totals["enrolled"], total)
        self.assertEqual(self.state.breaks[0]["expected"], 0)

    def test_ngo_approval_changes_eligibility_and_partners(self):
        organization = self.state.organizations[0]
        CanteenState.set_ngo_approval.fn(self.state, organization["id"], False)
        self.assertNotIn(organization["name"], self.state.partners)
        self.assertFalse(self.state.selected_organization["approved"])
        CanteenState.create_request.fn(
            self.state, "F01", {"quantity": "1", "notes": "Demo plan"}
        )
        self.assertEqual(self.state.requests, [])
        pending = self.state.organizations[2]
        CanteenState.set_ngo_approval.fn(self.state, pending["id"], True)
        self.assertIn(pending["name"], self.state.partners)
        self.assertLess(self.state.approved_organizations, 15)

    def test_targeted_announcements_and_roster_are_local(self):
        data = {
            "title": "Demo break reminder",
            "year": "FY",
            "CS/CSE": "on",
            "ECS": "on",
            "start": "11:15",
            "crowd": "High",
            "note": "Illustrative queue note, not measured",
        }
        CanteenState.save_targeted_announcement.fn(
            self.state, "", {**data, "start": "not-time"}
        )
        self.assertEqual(self.state.targeted_announcements, [])
        CanteenState.save_targeted_announcement.fn(self.state, "", data)
        notice = self.state.targeted_announcements[0]
        self.assertEqual(notice["branches"], ["CS/CSE", "ECS"])
        CanteenState.save_targeted_announcement.fn(
            self.state, notice["id"], {**data, "crowd": "Low"}
        )
        self.assertEqual(len(self.state.targeted_announcements), 1)
        self.assertEqual(self.state.targeted_announcements[0]["crowd"], "Low")
        CanteenState.remove_targeted_announcement.fn(self.state, notice["id"])
        self.assertEqual(self.state.targeted_announcements, [])
        organizations = [dict(row) for row in self.state.organizations]
        CanteenState.save_account_label.fn(
            self.state,
            self.state.accounts[0]["id"],
            {"role": "Admin", "status": "Illustrative inactive"},
        )
        self.assertEqual(self.state.organizations, organizations)

    def test_assistant_sales_and_no_forecast(self):
        state = HomeState(_reflex_internal_init=True)
        reply = state._answer("Which dish is most popular?")
        self.assertIn("Rice & vegetable plates", reply)
        self.assertIn("140", reply)
        self.assertIn(
            "cannot reliably predict",
            state._answer("How much food should we prepare tomorrow?"),
        )
        self.assertIn("96", state._answer("How much food is remaining?"))
        state.operation_snapshot[0]["sold"] += 5
        self.assertIn("91", state._answer("How much food is remaining?"))


if __name__ == "__main__":
    unittest.main()
