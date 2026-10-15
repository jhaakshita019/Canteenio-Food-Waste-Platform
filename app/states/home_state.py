import reflex as rx
from typing import Any, TypedDict
from app.states.demo_records import (
    DEMO_FOOD,
    DEMO_ORGANIZATIONS,
    FoodRecord,
    OrganizationRecord,
)


from app.states.canteen_state import (
    CollectionRequest,
    Operation,
    seed_operations,
)


class ChatMessage(TypedDict):
    id: str
    role: str
    text: str


class HomeState(rx.State):
    food: list[FoodRecord] = [dict(record) for record in DEMO_FOOD]
    organizations: list[OrganizationRecord] = [
        dict(record) for record in DEMO_ORGANIZATIONS
    ]
    operation_snapshot: list[Operation] = seed_operations()
    request_snapshot: list[CollectionRequest] = []
    planning_snapshot: str = "Demo aggregate assumptions: FY total 1000, SY total 800; TY and BE unknown (0)."
    mobile_menu: bool = False
    route_notice: str = ""

    @rx.event
    async def load_route(self):
        from app.states.canteen_state import CanteenState

        canteen = await self.get_state(CanteenState)
        self.organizations = [dict(row) for row in canteen.organizations]
        self.operation_snapshot = [dict(row) for row in canteen.operations]
        self.request_snapshot = [dict(row) for row in canteen.requests]
        self.mobile_menu = False
        notices = {
            "/login": "Choose a demo workspace below. Login is not connected; no account or credentials are required or collected.",
            "/get-started": "Open the local canteen, NGO and admin demos below. Admin offers fictional verification, aggregate student assumptions and break schedules. No sign-in or live services are connected.",
        }
        self.route_notice = notices.get(self.router.url.path.rstrip("/"), "")

    messages: list[ChatMessage] = [
        {
            "id": "welcome",
            "role": "assistant",
            "text": "Hi, I'm your Canteenio demo guide. Ask me about sample food, collection windows or recorded impact. Everything here comes from local sample records, not live availability.",
        }
    ]

    @rx.var
    def available_portions(self) -> int:
        return sum(item["portions"] for item in self.food)

    @rx.var
    def collected_portions(self) -> int:
        return sum(item["collected"] for item in self.food)

    @rx.var
    def available_weight(self) -> float:
        return sum(item["weight_kg"] for item in self.food)

    @rx.var
    def approved_count(self) -> int:
        return sum(org["approved"] for org in self.organizations)

    @rx.event
    def toggle_menu(self):
        self.mobile_menu = not self.mobile_menu

    @rx.event
    def close_menu(self):
        self.mobile_menu = False

    @rx.event
    def clear_chat(self):
        self.messages = self.messages[:1]

    @rx.event
    async def submit_question(self, form_data: dict[str, Any]):
        return HomeState.ask_question(str(form_data.get("question", "")))

    @rx.event
    async def ask_question(self, question: str):
        from app.states.canteen_state import CanteenState

        canteen = await self.get_state(CanteenState)
        self.organizations = [dict(row) for row in canteen.organizations]
        self.operation_snapshot = [dict(row) for row in canteen.operations]
        totals = canteen.student_totals
        self.planning_snapshot = f"DEMO assumptions: {totals['enrolled']} enrolled, {totals['campus']} estimated on-campus, {totals['visitors']} estimated canteen visitors, {totals['meals']} estimated meal demand. These are sequential rounded estimates, not measured crowd or purchases."
        question = question.strip()[:400]
        if not question:
            return
        self.messages = self.messages[-18:]
        self.messages.append(
            {
                "id": f"user-{len(self.messages)}",
                "role": "user",
                "text": question,
            }
        )
        self.messages.append(
            {
                "id": f"reply-{len(self.messages)}",
                "role": "assistant",
                "text": self._answer(question),
            }
        )

    def _answer(self, question: str) -> str:
        query = question.lower()
        reservations: dict[str, int] = {}
        for request in self.request_snapshot:
            if request["status"] in ("Pending", "Approved", "Confirmed"):
                operation_id = request["operation_id"]
                reservations[operation_id] = (
                    reservations.get(operation_id, 0) + request["quantity"]
                )
        distribution_rows = [
            {
                **row,
                "listed": max(
                    0, row["listed"] - reservations.get(row["id"], 0)
                ),
            }
            for row in self.operation_snapshot
            if row["status"] == "Available" and row["reviewed"]
        ]
        distribution_total = sum(row["listed"] for row in distribution_rows)
        collected = sum(row["collected"] for row in self.operation_snapshot)
        if any(
            word in query
            for word in ("ngo", "verified", "approved", "organization")
        ):
            if not self.organizations:
                return "No fictional demo organization records are available, so I can't identify admin-approved demo profiles. No real-world verification or collection availability is established."
            approved = [
                org["name"] for org in self.organizations if org["approved"]
            ]
            names = "; ".join(approved) or "None"
            return f"DEMO: {len(approved)} of {len(self.organizations)} organizations are fictional admin-approved demo profiles: {names}. Approval only indicates eligibility for simulated requests in this session, not genuine verification, real partners or availability for an actual pickup. There are currently {distribution_total} unreserved distribution-ready demo portions."
        if any(
            word in query
            for word in (
                "impact",
                "saved",
                "waste",
                "wastage",
                "metric",
                "donated",
            )
        ):
            return f"DEMO: No measured wastage reduction is recorded. {collected} portions are marked Collected in current session operations for one illustrative day. This includes seeded sample counts and any simulated collections, not proof of actual waste prevention, pickups, donations, meals delivered or carbon savings. Separately, {distribution_total} unreserved portions are distribution-ready in the demo; inventory remaining is not the same as food available for distribution."
        if "distribution" in query:
            items = "; ".join(
                f"{row['name']}: {row['listed']} unreserved portions"
                for row in distribution_rows
                if row["listed"] > 0
            )
            return f"DEMO: {distribution_total} portions still remaining for distribution: reviewed Available listed portions minus Pending/Approved/Confirmed request reservations, calculated per listing. {items or 'No unreserved reviewed Available surplus; Draft, Paused and unreviewed listings are excluded'}. This is a subset of inventory remaining, not additional stock. Review is simulated, not real food-safety verification or live availability."
        if "popular" in query or "most sold" in query:
            maximum = max(
                (row["sold"] for row in self.operation_snapshot), default=0
            )
            if not maximum:
                return "DEMO: No sold portions recorded, so a popular dish cannot be identified."
            names = "; ".join(
                row["name"]
                for row in self.operation_snapshot
                if row["sold"] == maximum
            )
            return f"DEMO: {names} has the largest sample sold amount ({maximum} portions per tied dish). This is recorded sales, not live popularity or historical demand."
        if "tomorrow" in query and any(
            word in query
            for word in ("prepare", "preparation", "food", "demand")
        ):
            return "DEMO: I cannot reliably predict tomorrow's preparation. These records describe one illustrative day, not sufficient dated historical observations. Aggregate attendance and meal-demand assumptions are planning inputs, not a validated forecast."
        if "remaining" in query or "left" in query:
            items = "; ".join(
                f"{row['name']}: {row['prepared'] - row['sold'] - row['collected']}"
                for row in self.operation_snapshot
            )
            total = sum(
                row["prepared"] - row["sold"] - row["collected"]
                for row in self.operation_snapshot
            )
            return f"DEMO: {total} portions remaining today in current session inventory (prepared − sold − collected): {items or 'no records'}. Today means one illustrative day, not a dated live stock count. Listed and reserved surplus is included in inventory, not added again; only {distribution_total} unreserved reviewed Available portions are distribution-ready."
        if any(
            word in query
            for word in ("crowd", "student", "attendance", "visitor")
        ):
            return self.planning_snapshot
        if "available" in query and not any(
            word in query for word in ("vegan", "vegetarian", "allergen")
        ):
            items = "; ".join(
                f"{row['name']}: {row['listed']} unreserved portions, {row['start']}–{row['end']}"
                for row in distribution_rows
                if row["listed"] > 0
            )
            return f"DEMO: {distribution_total} unreserved distribution-ready portions. {items or 'No unreserved reviewed Available listings in local operations; Draft, Paused and unreviewed listings are excluded'}. Pending/Approved/Confirmed reservations are deducted per listing. Review is simulated, not real food-safety verification. No live availability."
        if (
            any(
                word in query
                for word in (
                    "when",
                    "time",
                    "window",
                    "pickup",
                    "pick up",
                    "collect",
                )
            )
            and "impact" not in query
        ):
            windows = "; ".join(
                f"{row['name']}: {row['start']}–{row['end']} ({row['status']}; {'reviewed in demo' if row['reviewed'] else 'unreviewed'})"
                for row in self.operation_snapshot
            )
            return f"DEMO collection windows in current session operations (campus local time): {windows or 'no records'}. These are illustrative windows with no current date attached, not confirmed pickups. Only {distribution_total} unreserved reviewed Available portions are distribution-ready; no actual pickup can be booked here."
        if any(
            word in query
            for word in ("how many", "quantity", "portions", "total", "much")
        ):
            remaining = sum(
                row["prepared"] - row["sold"] - row["collected"]
                for row in self.operation_snapshot
            )
            return f"DEMO: Current session operations for one illustrative day record {remaining} inventory portions remaining (prepared − sold − collected), {distribution_total} unreserved distribution-ready portions (reviewed Available listed minus Pending/Approved/Confirmed reservations), and {collected} portions marked Collected. These are distinct measures, not additive totals. No measured wastage reduction is recorded; no live stock or actual pickups are established."
        if any(
            word in query
            for word in (
                "food",
                "available",
                "menu",
                "vegan",
                "vegetarian",
                "allergen",
                "salad",
                "rice",
                "bowl",
            )
        ):
            diets = {item["id"]: item["diet"] for item in self.food}
            filtered = self.operation_snapshot
            if "vegan" in query:
                filtered = [
                    row for row in filtered if diets.get(row["id"]) == "Vegan"
                ]
            elif "vegetarian" in query:
                filtered = [
                    row
                    for row in filtered
                    if diets.get(row["id"]) in ("Vegetarian", "Vegan")
                ]
            if not filtered:
                return "No matching demo food descriptions are recorded. Diet labels may be unknown; I can't infer current availability or food safety."
            ready_by_id = {
                row["id"]: row["listed"] for row in distribution_rows
            }
            items = "; ".join(
                f"{row['name']} — at {row['location']} ({diets.get(row['id'], 'Diet unknown')}; recorded allergens: {row['allergens']}; {row['status']}; {ready_by_id.get(row['id'], 0)} unreserved distribution-ready portions)"
                for row in filtered
            )
            return f"DEMO current session food records: {items}. Diet labels are sample descriptions, not verified dietary guarantees. Distribution-ready counts require reviewed Available listings and deduct Pending/Approved/Confirmed reservations. Photos are illustrative. Food safety and allergens must be confirmed by a real provider before collection; no live availability."
        if any(
            word in query
            for word in (
                "how",
                "work",
                "canteenio",
                "start",
                "login",
                "sign",
                "account",
            )
        ):
            return "Canteenio's proposed workflow is: plan demand → prepare food → record sales → list surplus → connect with approved NGOs → coordinate collection → review outcomes. The public page shows sample listings and rule-based answers. The canteen workspace provides local inventory, preparation, sales, surplus, planning and simulated messaging. The NGO workspace has a 15-profile fictional directory, reviewed local surplus, simulated collection requests and local chat shared with the canteen workspace. Admin offers local fictional verification, aggregate enrollment assumptions, schedules, roster labels and announcements. Admin actions are open, not access-protected or saved to Supabase; authentication, live data and real messaging are not connected."
        return "I can't answer that from these sample records. Try asking about available food, portion totals, collection windows, approved demo organizations or demo impact. I don't access live services or provide food-safety guarantees."
