import reflex as rx
import unittest
from app.states.demo_records import (
    DEMO_FOOD,
    DEMO_ORGANIZATIONS,
    WORKFLOW,
    CAPABILITIES,
    SUGGESTED_QUESTIONS,
)
from app.states.home_state import HomeState


class PublicDemoTests(unittest.TestCase):
    def setUp(self):
        self.state = HomeState(_reflex_internal_init=True)

    def test_sample_metrics(self):
        self.assertEqual(sum(row["portions"] for row in DEMO_FOOD), 96)
        self.assertEqual(sum(row["collected"] for row in DEMO_FOOD), 55)
        self.assertAlmostEqual(sum(row["weight_kg"] for row in DEMO_FOOD), 36.0)
        self.assertEqual(len(DEMO_ORGANIZATIONS), 15)
        self.assertEqual(sum(org["approved"] for org in DEMO_ORGANIZATIONS), 10)

    def test_content_counts(self):
        self.assertEqual(len(WORKFLOW), 7)
        self.assertEqual(len(CAPABILITIES), 8)
        self.assertEqual(len(SUGGESTED_QUESTIONS), 6)

    def test_all_suggestions_have_grounded_answers(self):
        for question in SUGGESTED_QUESTIONS:
            reply = self.state._answer(question)
            self.assertTrue(reply)
            self.assertNotIn("I can't answer that", reply)

    def test_empty_records_are_transparent(self):
        self.state.food = []
        self.assertIn("unavailable", self.state._answer("What is available?"))

    def test_unsupported_question(self):
        self.assertIn(
            "can't answer", self.state._answer("What is tomorrow's weather?")
        )

    def test_vegan_filter(self):
        reply = self.state._answer("What vegan food is available?")
        self.assertIn("Fresh seasonal salad", reply)
        self.assertNotIn("Garden vegetable bowls", reply)


if __name__ == "__main__":
    unittest.main()
