import reflex as rx
from typing import Any, TypedDict
from uuid import uuid4
from faker import Faker
import reflex_xy
from app.states.demo_records import (
    DEMO_FOOD,
    DEMO_ORGANIZATIONS,
    OrganizationRecord,
)


class Operation(TypedDict):
    id: str
    name: str
    location: str
    allergens: str
    prepared: int
    sold: int
    collected: int
    listed: int
    start: str
    end: str
    handling: str
    status: str
    reviewed: bool


class OperationView(Operation):
    remaining: int
    unallocated: int
    eligibility: str


class CollectionRequest(TypedDict):
    id: str
    organization_id: str
    organization: str
    operation_id: str
    food: str
    location: str
    window: str
    quantity: int
    notes: str
    status: str


class BreakSlot(TypedDict):
    id: str
    branch: str
    year: str
    start: str
    end: str
    enrolled: int
    attendance: int
    expected: int
    visitors_pct: int
    meals_pct: int
    visitors: int
    meals: int
    active: bool


class TargetedAnnouncement(TypedDict):
    id: str
    title: str
    year: str
    branches: list[str]
    start: str
    crowd: str
    note: str


class AccountRecord(TypedDict):
    id: str
    name: str
    email: str
    role: str
    status: str


class Notice(TypedDict):
    id: str
    title: str
    text: str
    audience: str
    read: bool


class ConversationMessage(TypedDict):
    id: str
    side: str
    text: str


def seed_operations() -> list[Operation]:
    return [
        Operation(
            id=row["id"],
            name=row["name"],
            location=row["canteen"],
            allergens=row["allergens"],
            prepared=100 + index * 20 + row["portions"] + row["collected"],
            sold=100 + index * 20,
            collected=row["collected"],
            listed=row["portions"],
            start=row["collection"].split("–")[0],
            end=row["collection"].split("–")[1],
            handling="Sample handling note: covered containers; temperature and allergens must be checked by a real provider.",
            status="Draft",
            reviewed=False,
        )
        for index, row in enumerate(DEMO_FOOD)
    ]


BRANCHES: tuple[str, ...] = (
    "CS/CSE",
    "ECS",
    "IT",
    "Mechanical",
    "AI&DS",
    "AI&ML",
    "Civil",
)
YEARS: tuple[str, ...] = ("FY", "SY", "TY", "BE")


def seed_breaks() -> list[BreakSlot]:
    slots: list[BreakSlot] = []
    for year_index, year in enumerate(YEARS):
        total = {"FY": 1000, "SY": 800}.get(year, 0)
        for index, branch in enumerate(BRANCHES):
            enrolled = total // 7 + int(index < total % 7)
            hour = 11 + (index + year_index) % 3
            campus = round(enrolled * 0.8)
            visitors = round(campus * 0.5)
            slots.append(
                BreakSlot(
                    id=f"{year}-{index}",
                    branch=branch,
                    year=year,
                    start=f"{hour}:15",
                    end=f"{hour}:45",
                    enrolled=enrolled,
                    attendance=80,
                    expected=campus,
                    visitors_pct=50,
                    meals_pct=60,
                    visitors=visitors,
                    meals=round(visitors * 0.6),
                    active=True,
                )
            )
    return slots


def seed_accounts() -> list[AccountRecord]:
    fake = Faker("en_IN")
    fake.seed_instance(81)
    return [
        AccountRecord(
            id=f"ACCOUNT-{index + 1}",
            name=f"Fictional · {fake.name()}",
            email=f"account{index + 1}@example.invalid",
            role=("Student", "Canteen", "NGO", "Admin")[index % 4],
            status="Illustrative active"
            if index % 3
            else "Illustrative inactive",
        )
        for index in range(12)
    ]


class CanteenState(rx.State):
    tab: str = "Overview"
    tabs: list[str] = [
        "Overview",
        "Inventory",
        "Surplus",
        "Break planning",
        "Notifications",
        "Requests",
        "Messages",
    ]
    operations: list[Operation] = seed_operations()
    breaks: list[BreakSlot] = seed_breaks()
    branch: str = "All branches"
    branches: list[str] = ["All branches", *BRANCHES]
    years: list[str] = list(YEARS)
    admin_tab: str = "Overview"
    admin_tabs: list[str] = [
        "Overview",
        "NGO verification",
        "Students",
        "Break schedules",
        "Food & users",
        "Notifications/analytics",
    ]
    planning_year: str = "All years"
    planning_branch: str = "All branches"
    planning_revision: int = 0
    accounts: list[AccountRecord] = seed_accounts()
    targeted_announcements: list[TargetedAnnouncement] = []
    feedback: str = ""
    error: bool = False
    inventory_revision: int = 0
    notices: list[Notice] = [
        Notice(
            id="intro",
            title="Review surplus drafts",
            text="All sample listings start as drafts. Check the simulated review fields before making a listing available in this demo.",
            audience="Canteen team",
            read=False,
        )
    ]
    announcements: list[Notice] = []
    alerts_enabled: bool = True
    partner: str = DEMO_ORGANIZATIONS[0]["name"]
    organizations: list[OrganizationRecord] = [
        dict(row) for row in DEMO_ORGANIZATIONS
    ]
    requests: list[CollectionRequest] = []
    ngo_tab: str = "Directory"
    ngo_tabs: list[str] = [
        "Directory",
        "Available food",
        "My requests",
        "Collection history",
        "Messages",
    ]
    organization_id: str = DEMO_ORGANIZATIONS[0]["id"]
    directory_query: str = ""
    directory_filter: str = "All"

    @rx.event
    def select_admin_tab(self, tab: str):
        if tab in self.admin_tabs:
            self.admin_tab = tab
            self.feedback = ""

    @rx.event
    def save_planning_filter(self, data: dict[str, Any]):
        year = str(data.get("year", "All years"))
        branch = str(data.get("branch", "All branches"))
        if year in ("All years", *YEARS) and branch in self.branches:
            self.planning_year, self.planning_branch = year, branch

    @rx.var
    def planning_rows(self) -> list[BreakSlot]:
        return [
            row
            for row in self.breaks
            if (
                self.planning_year == "All years"
                or row["year"] == self.planning_year
            )
            and (
                self.planning_branch == "All branches"
                or row["branch"] == self.planning_branch
            )
        ]

    @rx.var
    def student_totals(self) -> dict[str, int]:
        return {
            "enrolled": sum(row["enrolled"] for row in self.breaks),
            "campus": sum(row["expected"] for row in self.breaks),
            "visitors": sum(row["visitors"] for row in self.breaks),
            "meals": sum(row["meals"] for row in self.breaks),
        }

    @rx.var
    def year_totals(self) -> list[dict[str, str | int]]:
        return [
            {
                "year": year,
                "enrolled": sum(
                    row["enrolled"]
                    for row in self.breaks
                    if row["year"] == year
                ),
            }
            for year in YEARS
        ]

    @rx.var
    def slot_summary(self) -> list[dict[str, str | int]]:
        starts = sorted({row["start"] for row in self.breaks if row["active"]})
        return [
            {
                "start": start,
                "groups": sum(
                    row["active"] and row["start"] == start
                    for row in self.breaks
                ),
                "campus": sum(
                    row["expected"]
                    for row in self.breaks
                    if row["active"] and row["start"] == start
                ),
                "visitors": sum(
                    row["visitors"]
                    for row in self.breaks
                    if row["active"] and row["start"] == start
                ),
                "meals": sum(
                    row["meals"]
                    for row in self.breaks
                    if row["active"] and row["start"] == start
                ),
            }
            for start in starts
        ]

    def _recalculate_break(self, row: BreakSlot):
        row["expected"] = round(row["enrolled"] * row["attendance"] / 100)
        row["visitors"] = round(row["expected"] * row["visitors_pct"] / 100)
        row["meals"] = round(row["visitors"] * row["meals_pct"] / 100)

    @rx.event
    def save_students(self, slot_id: str, data: dict[str, Any]):
        row = next((row for row in self.breaks if row["id"] == slot_id), None)
        if row is None:
            self._feedback("Student aggregate not found.", True)
            return
        try:
            enrolled = self._number(data, "enrolled")
            attendance = self._number(data, "attendance", 100)
            visitors = self._number(data, "visitors_pct", 100)
            meals = self._number(data, "meals_pct", 100)
            row.update(
                enrolled=enrolled,
                attendance=attendance,
                visitors_pct=visitors,
                meals_pct=meals,
            )
            self._recalculate_break(row)
            self.planning_revision += 1
            self._feedback(
                "Aggregate assumptions saved locally. Enrollment and each estimate recalculated; food sales unchanged."
            )
        except ValueError as e:
            self._feedback(str(e), True)

    @rx.event
    def save_admin_schedule(self, slot_id: str, data: dict[str, Any]):
        row = next((row for row in self.breaks if row["id"] == slot_id), None)
        if row is None:
            self._feedback("Break slot not found.", True)
            return
        try:
            start, end = str(data.get("start", "")), str(data.get("end", ""))
            self._window(start, end)
            row.update(
                start=start,
                end=end,
                active=str(data.get("active", "")).lower()
                in ("on", "true", "1"),
            )
            self.planning_revision += 1
            self._feedback(
                "Schedule saved locally and reflected in canteen Break planning. Enrollment and food quantities unchanged."
            )
        except ValueError as e:
            self._feedback(str(e), True)

    @rx.event
    def set_ngo_approval(self, organization_id: str, approved: bool):
        row = next(
            (row for row in self.organizations if row["id"] == organization_id),
            None,
        )
        if row is None:
            self._feedback("Fictional organization not found.", True)
            return
        row["approved"] = approved
        if self.partner not in self.partners:
            self.partner = next(
                iter(self.partners), "No approved demo partners"
            )
        self.inventory_revision += 1
        self._feedback(
            "Fictional approval updated locally. Badges, partner list and request eligibility use this status. Existing reservations remain until rejected or cancelled; revoked NGOs cannot progress pickups."
        )
        self._notify(
            "Demo NGO status changed",
            f"{row['name']}: {'approved' if approved else 'revoked'} locally; not real verification.",
        )

    @rx.event
    def save_account_label(self, account_id: str, data: dict[str, Any]):
        row = next(
            (row for row in self.accounts if row["id"] == account_id), None
        )
        role, status = str(data.get("role", "")), str(data.get("status", ""))
        if (
            row is None
            or role not in ("Student", "Canteen", "NGO", "Admin")
            or status not in ("Illustrative active", "Illustrative inactive")
        ):
            self._feedback("Choose valid fictional roster labels.", True)
            return
        row.update(role=role, status=status)
        self._feedback(
            "Fictional roster labels changed only. No account, permissions or access were modified."
        )

    @rx.event
    def save_targeted_announcement(self, notice_id: str, data: dict[str, Any]):
        try:
            title = str(data.get("title", "")).strip()
            year, start, crowd = (
                str(data.get("year", "")),
                str(data.get("start", "")),
                str(data.get("crowd", "")),
            )
            note = str(data.get("note", "")).strip()
            branches = [
                branch
                for branch in BRANCHES
                if str(data.get(branch, "")).lower() in ("on", "true", "1")
            ]
            from datetime import time

            time.fromisoformat(start)
            if (
                not title
                or len(title) > 80
                or len(note) > 500
                or not branches
                or year not in ("All years", *YEARS)
                or crowd not in ("Low", "Moderate", "High")
            ):
                raise ValueError(
                    "Provide a title (1–80 characters), year, at least one branch, valid break time and crowd level; optional note at most 500 characters."
                )
            notice = TargetedAnnouncement(
                id=notice_id or str(uuid4()),
                title=title,
                year=year,
                branches=branches,
                start=start,
                crowd=crowd,
                note=note,
            )
            index = next(
                (
                    index
                    for index, row in enumerate(self.targeted_announcements)
                    if row["id"] == notice_id
                ),
                -1,
            )
            if index >= 0:
                self.targeted_announcements[index] = notice
            else:
                self.targeted_announcements.insert(0, notice)
            self._feedback(
                "Targeted announcement saved locally and visible to the canteen in this session. Crowd is a manually selected assumption, not measured occupancy. Not sent externally."
            )
        except ValueError as e:
            self._feedback(str(e), True)

    @rx.event
    def remove_targeted_announcement(self, notice_id: str):
        self.targeted_announcements = [
            row for row in self.targeted_announcements if row["id"] != notice_id
        ]
        self._feedback("Targeted local announcement removed.")

    @rx.var
    def partners(self) -> list[str]:
        return [row["name"] for row in self.organizations if row["approved"]]

    @rx.var
    def selected_organization(self) -> OrganizationRecord:
        return next(
            (
                row
                for row in self.organizations
                if row["id"] == self.organization_id
            ),
            OrganizationRecord(
                id="",
                name="No organization selected",
                city="",
                mission="",
                contact="",
                email="",
                contact_notes="",
                approved=False,
            ),
        )

    @rx.var
    def directory(self) -> list[OrganizationRecord]:
        query = self.directory_query.strip().lower()
        return [
            row
            for row in self.organizations
            if (
                not query
                or query
                in f"{row['id']} {row['name']} {row['city']} {row['mission']}".lower()
            )
            and (
                self.directory_filter == "All"
                or (self.directory_filter == "Approved" and row["approved"])
                or (self.directory_filter == "Pending" and not row["approved"])
            )
        ]

    @rx.var
    def approved_organizations(self) -> int:
        return sum(row["approved"] for row in self.organizations)

    def _reserved(self, operation_id: str) -> int:
        return sum(
            row["quantity"]
            for row in self.requests
            if row["operation_id"] == operation_id
            and row["status"] in ("Pending", "Approved", "Confirmed")
        )

    @rx.var
    def available_surplus(self) -> list[Operation]:
        return [
            Operation(
                **{**row, "listed": row["listed"] - self._reserved(row["id"])}
            )
            for row in self.operations
            if row["status"] == "Available"
            and row["reviewed"]
            and row["listed"] > self._reserved(row["id"])
        ]

    @rx.var
    def ngo_requests(self) -> list[CollectionRequest]:
        return [
            row
            for row in self.requests
            if row["organization_id"] == self.organization_id
        ]

    @rx.var
    def collection_history(self) -> list[CollectionRequest]:
        return [
            row for row in self.ngo_requests if row["status"] == "Collected"
        ]

    @rx.var
    def ngo_conversation(self) -> list[ConversationMessage]:
        return self.conversations.get(self.selected_organization["name"], [])

    @rx.event
    def select_ngo_tab(self, tab: str):
        if tab in self.ngo_tabs:
            self.ngo_tab = tab
            self.feedback = ""

    @rx.event
    def search_directory(self, query: str):
        self.directory_query = query[:150]

    @rx.event
    def filter_directory(self, value: str):
        if value in ("All", "Approved", "Pending"):
            self.directory_filter = value

    @rx.event
    def select_organization(self, organization_id: str):
        if any(row["id"] == organization_id for row in self.organizations):
            self.organization_id = organization_id
            self.feedback = ""

    @rx.event
    def create_request(self, operation_id: str, data: dict[str, Any]):
        organization = self.selected_organization
        row = next(
            (row for row in self.operations if row["id"] == operation_id), None
        )
        try:
            quantity = self._number(data, "quantity")
            notes = str(data.get("notes", "")).strip()
            if not organization["id"] or not organization["approved"]:
                raise ValueError(
                    "Only approved fictional NGOs can request surplus in this demo."
                )
            if (
                row is None
                or row["status"] != "Available"
                or not row["reviewed"]
            ):
                raise ValueError(
                    "Choose an available, reviewed surplus listing."
                )
            if quantity < 1 or quantity > row["listed"] - self._reserved(
                operation_id
            ):
                raise ValueError(
                    "Quantity must be positive and within the unreserved available portions."
                )
            if not notes or len(notes) > 500:
                raise ValueError("Enter pickup notes of 1–500 characters.")
            self.requests.insert(
                0,
                CollectionRequest(
                    id=str(uuid4()),
                    organization_id=organization["id"],
                    organization=organization["name"],
                    operation_id=row["id"],
                    food=row["name"],
                    location=row["location"],
                    window=f"{row['start']}–{row['end']}",
                    quantity=quantity,
                    notes=notes,
                    status="Pending",
                ),
            )
            self.inventory_revision += 1
            self._feedback(
                "Request reserved locally, awaiting demo canteen approval. Local demo only, resets on reload."
            )
            self._notify(
                "Local collection request",
                f"{organization['name']}: {quantity} portions of {row['name']} requested in this session only.",
            )
        except ValueError as e:
            self._feedback(str(e), True)

    @rx.event
    def progress_request(self, request_id: str, action: str):
        request = next(
            (row for row in self.requests if row["id"] == request_id), None
        )
        if request is None:
            self._feedback("Request not found.", True)
            return
        allowed = {
            "approve": ("Pending",),
            "reject": ("Pending", "Approved", "Confirmed"),
            "confirm": ("Approved",),
            "cancel": ("Pending", "Approved", "Confirmed"),
            "collect": ("Confirmed",),
        }
        if request["status"] not in allowed.get(action, ()):
            self._feedback(
                "This transition is not available for the current request status.",
                True,
            )
            return
        if (
            action in ("confirm", "cancel")
            and request["organization_id"] != self.organization_id
        ):
            self._feedback("Select the requesting organization first.", True)
            return
        row = next(
            (
                row
                for row in self.operations
                if row["id"] == request["operation_id"]
            ),
            None,
        )
        organization = next(
            (
                org
                for org in self.organizations
                if org["id"] == request["organization_id"]
            ),
            None,
        )
        if action in ("approve", "confirm", "collect"):
            if (
                organization is None
                or not organization["approved"]
                or row is None
                or row["status"] != "Available"
                or not row["reviewed"]
                or row["listed"] < self._reserved(row["id"])
            ):
                self._feedback(
                    "Approval and reviewed inventory must still be valid. Cancel or reject this request to release its reservation.",
                    True,
                )
                return
        if action == "collect":
            row["listed"] -= request["quantity"]
            row["collected"] += request["quantity"]
            if row["listed"] == 0:
                row["status"] = "Draft"
                row["reviewed"] = False
        request["status"] = {
            "approve": "Approved",
            "reject": "Rejected",
            "confirm": "Confirmed",
            "cancel": "Cancelled",
            "collect": "Collected",
        }[action]
        self.inventory_revision += 1
        self._feedback(
            f"Request {request['status'].lower()} · local demo only, resets on reload. No actual pickup occurred."
        )
        self._notify(
            "Request updated locally",
            f"{request['food']}: {request['status']} · {request['quantity']} simulated portions.",
        )

    @rx.event
    def compose_ngo_message(self, data: dict[str, Any]):
        text = str(data.get("message", "")).strip()
        organization = self.selected_organization
        if not organization["approved"]:
            self._feedback(
                "Choose an approved fictional NGO to use the demo chat.", True
            )
            return
        if not text or len(text) > 500:
            self._feedback("Enter a message of 1–500 characters.", True)
            return
        name = organization["name"]
        messages = list(self.conversations.get(name, []))
        messages.append(
            ConversationMessage(id=str(uuid4()), side="ngo", text=text)
        )
        self.conversations[name] = messages[-40:]
        self._feedback(
            "Message added to the same canteen thread. Local demo only, resets on reload; not delivered to anyone."
        )

    conversations: dict[str, list[ConversationMessage]] = {
        row["name"]: [
            ConversationMessage(
                id="welcome",
                side="partner",
                text="Scripted partner example: please share the sample portion count and pickup window. No real organization is connected.",
            )
        ]
        for row in DEMO_ORGANIZATIONS
        if row["approved"]
    }

    @rx.var
    def rows(self) -> list[OperationView]:
        result: list[OperationView] = []
        for row in self.operations:
            remaining = row["prepared"] - row["sold"] - row["collected"]
            result.append(
                OperationView(
                    **row,
                    remaining=remaining,
                    unallocated=remaining - row["listed"],
                    eligibility="Eligible in demo only"
                    if row["reviewed"]
                    else "Review required",
                )
            )
        return result

    @rx.var
    def totals(self) -> dict[str, int]:
        return {
            "prepared": sum(row["prepared"] for row in self.operations),
            "sold": sum(row["sold"] for row in self.operations),
            "remaining": sum(
                row["prepared"] - row["sold"] - row["collected"]
                for row in self.operations
            ),
            "collected": sum(row["collected"] for row in self.operations),
            "available": sum(
                row["listed"] - self._reserved(row["id"])
                for row in self.operations
                if row["status"] == "Available" and row["reviewed"]
            ),
            "listed": sum(row["listed"] for row in self.operations),
        }

    @rx.var
    def sell_through(self) -> float:
        prepared = sum(row["prepared"] for row in self.operations)
        return (
            100 * sum(row["sold"] for row in self.operations) / prepared
            if prepared
            else 0.0
        )

    @reflex_xy.data
    def portion_chart(self) -> dict[str, list[str] | list[int]]:
        return {
            "food": [row["name"] for row in self.operations],
            "sold": [row["sold"] for row in self.operations],
            "collected": [row["collected"] for row in self.operations],
            "remaining": [
                row["prepared"] - row["sold"] - row["collected"]
                for row in self.operations
            ],
        }

    @rx.var
    def visible_breaks(self) -> list[BreakSlot]:
        return [
            row
            for row in self.breaks
            if self.branch == "All branches" or row["branch"] == self.branch
        ]

    @rx.var
    def expected_attendance(self) -> int:
        return sum(
            row["expected"] for row in self.visible_breaks if row["active"]
        )

    @rx.var
    def unread(self) -> int:
        return sum(not row["read"] for row in self.notices)

    @rx.var
    def conversation(self) -> list[ConversationMessage]:
        return self.conversations.get(self.partner, [])

    @rx.event
    def select_tab(self, tab: str):
        if tab in self.tabs:
            self.tab = tab
            self.feedback = ""

    @rx.event
    def select_branch(self, branch: str):
        if branch in self.branches:
            self.branch = branch

    def _feedback(self, text: str, error: bool = False):
        self.feedback = text
        self.error = error

    def _notify(self, title: str, text: str):
        if self.alerts_enabled:
            self.notices.insert(
                0,
                Notice(
                    id=str(uuid4()),
                    title=title,
                    text=text,
                    audience="Canteen team",
                    read=False,
                ),
            )
            self.notices = self.notices[:30]

    def _number(
        self, data: dict[str, Any], key: str, maximum: int = 100000
    ) -> int:
        raw = str(data.get(key, "")).strip()
        if not raw.isdecimal():
            raise ValueError(
                f"{key.capitalize()} must be a non-negative whole number."
            )
        value = int(raw)
        if value > maximum:
            raise ValueError(f"{key.capitalize()} must be at most {maximum:,}.")
        return value

    def _window(self, start: str, end: str):
        from datetime import time

        try:
            first, last = time.fromisoformat(start), time.fromisoformat(end)
        except ValueError:
            raise ValueError("Enter valid start and end times.") from None
        if first >= last:
            raise ValueError(
                "End time must follow start time on the same sample day."
            )

    @rx.event
    def save_operation(self, record_id: str, data: dict[str, Any]):
        row = next(
            (row for row in self.operations if row["id"] == record_id), None
        )
        if row is None:
            self._feedback("This food record no longer exists.", True)
            return
        try:
            prepared = self._number(data, "prepared")
            sold = self._number(data, "sold")
            if sold + row["collected"] + row["listed"] > prepared:
                raise ValueError(
                    "Prepared must cover sold, collected and listed portions. Reduce the surplus listing first if needed."
                )
            name = str(data.get("name", "")).strip()
            if not name or len(name) > 100:
                raise ValueError("Enter a food name of 1–100 characters.")
            row.update(name=name, prepared=prepared, sold=sold)
            self.inventory_revision += 1
            self._feedback(
                "Local food record updated. All workspace totals have recalculated."
            )
            self._notify(
                "Inventory updated",
                f"{name}: {prepared} prepared, {sold} sold.",
            )
        except ValueError as e:
            self._feedback(str(e), True)

    @rx.event
    def add_operation(self, data: dict[str, Any]):
        try:
            name = str(data.get("name", "")).strip()
            location = str(data.get("location", "")).strip()
            allergens = str(data.get("allergens", "")).strip()
            if (
                not name
                or not location
                or not allergens
                or max(len(name), len(location), len(allergens)) > 100
            ):
                raise ValueError(
                    "Provide food, location and allergen notes (1–100 characters each). Use “Unknown” if allergens have not been checked."
                )
            prepared, sold = (
                self._number(data, "prepared"),
                self._number(data, "sold"),
            )
            if sold > prepared:
                raise ValueError(
                    "Sold portions cannot exceed prepared portions."
                )
            self.operations.append(
                Operation(
                    id=str(uuid4()),
                    name=name,
                    location=location,
                    allergens=allergens,
                    prepared=prepared,
                    sold=sold,
                    collected=0,
                    listed=0,
                    start="14:00",
                    end="15:00",
                    handling="",
                    status="Draft",
                    reviewed=False,
                )
            )
            self.inventory_revision += 1
            self._feedback("Food added to local demo inventory.")
            self._notify(
                "Food added", f"{name} added with {prepared} prepared portions."
            )
        except ValueError as e:
            self._feedback(str(e), True)

    @rx.event
    def quick_update(self, record_id: str, action: str):
        row = next(
            (row for row in self.operations if row["id"] == record_id), None
        )
        if row is None:
            self._feedback("Food record not found.", True)
            return
        if action == "prepare":
            if row["prepared"] > 99990:
                self._feedback("Maximum preparation is 100,000 portions.", True)
                return
            row["prepared"] += 10
        elif action == "sell":
            free = (
                row["prepared"] - row["sold"] - row["collected"] - row["listed"]
            )
            if free < 5:
                self._feedback(
                    "Not enough unallocated portions to sell 5. Prepare more or reduce the surplus listing.",
                    True,
                )
                return
            row["sold"] += 5
        else:
            return
        self.inventory_revision += 1
        self._feedback(
            "Local quantities updated; listed surplus is protected from sales."
        )
        self._notify(
            "Operations changed",
            f"{row['name']}: {action} action recorded in demo only.",
        )

    @rx.event
    def remove_operation(self, record_id: str):
        row = next(
            (row for row in self.operations if row["id"] == record_id), None
        )
        if row is None:
            return
        if row["prepared"] or row["sold"] or row["collected"] or row["listed"]:
            self._feedback(
                "Only zero-quantity records can be removed; operational records are retained for coherent totals.",
                True,
            )
            return
        self.operations = [
            row for row in self.operations if row["id"] != record_id
        ]
        self._feedback("Empty record removed.")

    @rx.event
    def save_surplus(self, record_id: str, data: dict[str, Any]):
        row = next(
            (row for row in self.operations if row["id"] == record_id), None
        )
        if row is None:
            self._feedback("Food record not found.", True)
            return
        if self._reserved(record_id):
            self._feedback(
                "Cancel, reject or complete active requests before editing this surplus listing. Reserved portions and pickup details are protected.",
                True,
            )
            return
        try:
            listed = self._number(data, "listed")
            if listed > row["prepared"] - row["sold"] - row["collected"]:
                raise ValueError(
                    "Listed portions cannot exceed remaining inventory."
                )
            start, end = str(data.get("start", "")), str(data.get("end", ""))
            self._window(start, end)
            status = str(data.get("status", "Draft"))
            handling = str(data.get("handling", "")).strip()
            reviewed = str(data.get("reviewed", "")).lower() in (
                "on",
                "true",
                "1",
            )
            if status not in ("Draft", "Available", "Paused"):
                raise ValueError("Choose a valid listing status.")
            if len(handling) > 500:
                raise ValueError(
                    "Handling notes must be at most 500 characters."
                )
            if status == "Available" and (
                not reviewed or not handling or not listed
            ):
                raise ValueError(
                    "Demo availability needs positive portions, handling notes and the simulated review checkbox. This is not actual safety verification."
                )
            row.update(
                listed=listed,
                start=start,
                end=end,
                status=status,
                handling=handling,
                reviewed=reviewed,
            )
            self.inventory_revision += 1
            self._feedback(
                "Surplus listing updated in both local workspaces. Nothing was published externally."
            )
            self._notify(
                "Surplus updated",
                f"{row['name']}: {listed} portions, {status.lower()} in demo.",
            )
        except ValueError as e:
            self._feedback(str(e), True)

    @rx.event
    def simulate_collection(self, record_id: str):
        if self._reserved(record_id):
            self._feedback(
                "Active requests reserve this food. Use the Requests panel to complete or release them first.",
                True,
            )
            return
        row = next(
            (row for row in self.operations if row["id"] == record_id), None
        )
        if (
            row is None
            or row["status"] != "Available"
            or not row["reviewed"]
            or row["listed"] <= 0
        ):
            self._feedback(
                "Only an available, reviewed demo listing with portions can simulate collection.",
                True,
            )
            return
        quantity = row["listed"]
        row["collected"] += quantity
        row["listed"] = 0
        row["status"] = "Draft"
        row["reviewed"] = False
        self.inventory_revision += 1
        self._feedback(
            f"{quantity} portions moved to simulated collected totals. No actual pickup occurred."
        )
        self._notify(
            "Simulated collection",
            f"{row['name']}: {quantity} sample portions marked collected.",
        )

    @rx.event
    def save_break(self, slot_id: str, data: dict[str, Any]):
        row = next((row for row in self.breaks if row["id"] == slot_id), None)
        if row is None:
            self._feedback("Break slot not found.", True)
            return
        try:
            attendance = self._number(data, "attendance", 100)
            start, end = str(data.get("start", "")), str(data.get("end", ""))
            self._window(start, end)
            row.update(
                attendance=attendance,
                start=start,
                end=end,
            )
            if "active" in data:
                row["active"] = str(data["active"]).lower() in (
                    "on",
                    "true",
                    "1",
                )
            self._recalculate_break(row)
            self.planning_revision += 1
            self._feedback(
                "Campus attendance assumption and times updated locally in admin and canteen views. Enrollment totals unchanged; visitors and meal demand are separate estimates, not actual sales."
            )
        except ValueError as e:
            self._feedback(str(e), True)

    @rx.event
    def toggle_alerts(self):
        self.alerts_enabled = not self.alerts_enabled
        self._feedback(
            "Local activity alerts enabled."
            if self.alerts_enabled
            else "Local activity alerts paused. No external notifications are sent."
        )

    @rx.event
    def mark_read(self):
        self.notices = [Notice(**{**row, "read": True}) for row in self.notices]

    @rx.event
    def clear_notices(self):
        self.notices = []

    @rx.event
    def save_announcement(self, notice_id: str, data: dict[str, Any]):
        title, text = (
            str(data.get("title", "")).strip(),
            str(data.get("text", "")).strip(),
        )
        audience = str(data.get("audience", "Canteen team"))
        if not title or not text or len(title) > 80 or len(text) > 500:
            self._feedback(
                "Enter a title (1–80 characters) and announcement (1–500 characters).",
                True,
            )
            return
        if audience not in (
            "Canteen team",
            "Collection partners",
            "All demo roles",
        ):
            self._feedback("Choose a valid audience.", True)
            return
        notice = Notice(
            id=notice_id or str(uuid4()),
            title=title,
            text=text,
            audience=audience,
            read=False,
        )
        existing = next(
            (
                index
                for index, row in enumerate(self.announcements)
                if row["id"] == notice_id
            ),
            -1,
        )
        if existing >= 0:
            self.announcements[existing] = notice
        else:
            self.announcements.insert(0, notice)
        self._feedback(
            "Announcement saved in this demo session only. Not broadcast or delivered."
        )

    @rx.event
    def remove_announcement(self, notice_id: str):
        self.announcements = [
            row for row in self.announcements if row["id"] != notice_id
        ]
        self._feedback("Local announcement removed.")

    @rx.event
    def select_partner(self, partner: str):
        if partner in self.partners:
            self.partner = partner
            self.feedback = ""

    @rx.event
    def compose_message(self, data: dict[str, Any]):
        text = str(data.get("message", "")).strip()
        if self.partner not in self.partners:
            self._feedback("Choose a currently approved demo partner.", True)
            return
        if not text or len(text) > 500:
            self._feedback("Enter a message of 1–500 characters.", True)
            return
        messages = list(self.conversations.get(self.partner, []))
        messages.append(
            ConversationMessage(id=str(uuid4()), side="canteen", text=text)
        )
        available = sum(
            row["listed"]
            for row in self.operations
            if row["status"] == "Available" and row["reviewed"]
        )
        messages.append(
            ConversationMessage(
                id=str(uuid4()),
                side="partner",
                text=f"Scripted demo reply: the workspace currently has {available} sample portions marked available. This response is generated locally; no partner received your message and no pickup was booked.",
            )
        )
        self.conversations[self.partner] = messages[-40:]
        self._feedback(
            "Message added locally with a scripted reply. Not sent to anyone."
        )

    @rx.event
    def clear_conversation(self):
        self.conversations[self.partner] = []
        self._feedback("Local conversation cleared.")
