import reflex as rx
from app.components.shared import brand
from app.components.collection_requests import canteen_requests
from app.components.targeted_announcements import targeted_card
from app.states.canteen_state import (
    CanteenState,
    BreakSlot,
    OperationView,
    AccountRecord,
    TargetedAnnouncement,
)
from app.states.demo_records import OrganizationRecord

BUTTON = "inline-flex items-center justify-center gap-2 rounded-lg bg-[#C9972A] px-4 py-2 text-xs font-semibold text-[#30250F] hover:bg-[#D6AB49] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#6A4B10] disabled:opacity-40"
OUTLINE = "inline-flex items-center justify-center gap-2 rounded-lg border border-[#DDD8C9] bg-white px-3 py-2 text-xs font-medium text-[#192D26] hover:bg-[#FFF7E2] focus-visible:outline-2 focus-visible:outline-[#6A4B10]"
INPUT = "w-full min-w-0 rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-800 focus-visible:outline-2 focus-visible:outline-[#C9972A]"
CARD = "w-full min-w-0 rounded-xl border border-[#E5E1D6] bg-white p-4 sm:p-5"


def field(
    label: str, name: str, default: str | int = "", kind: str = "text", **props
) -> rx.Component:
    return rx.el.label(
        rx.el.span(
            label, class_name="mb-1.5 block text-xs font-medium text-gray-600"
        ),
        rx.el.input(
            name=name,
            type=kind,
            default_value=default,
            key=default,
            class_name=INPUT,
            **props,
        ),
        class_name="block min-w-0",
    )


def select_field(
    label: str, name: str, options: list[str], default: str
) -> rx.Component:
    return rx.el.label(
        rx.el.span(
            label, class_name="mb-1.5 block text-xs font-medium text-gray-600"
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    options, lambda option: rx.el.option(option, value=option)
                ),
                name=name,
                default_value=default,
                key=default,
                class_name="w-full appearance-none rounded-lg border border-gray-300 bg-white py-2 pl-3 pr-8 text-sm text-gray-800 focus-visible:outline-2 focus-visible:outline-[#C9972A]",
            ),
            rx.icon(
                "chevron-down",
                class_name="pointer-events-none absolute right-3 top-3 h-4 w-4 text-gray-500",
            ),
            class_name="relative",
        ),
        class_name="block min-w-0",
    )


def title(title: str, description: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5 text-[#8A641B]"),
            rx.el.h2(
                title,
                class_name="font-['DM_Sans'] text-lg font-semibold text-[#192D26]",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(description, class_name="mt-2 text-xs leading-6 text-gray-600"),
        class_name="mb-4",
    )


def metric(label: str, value: str, note: str, icon: str) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.p(label, class_name="text-xs font-medium text-gray-600"),
            rx.icon(icon, class_name="h-4 w-4 shrink-0 text-[#8A641B]"),
            class_name="flex items-center justify-between gap-2",
        ),
        rx.el.p(
            value,
            class_name="mt-3 font-['DM_Sans'] text-3xl font-semibold text-[#192D26]",
        ),
        rx.el.p(note, class_name="mt-2 text-[11px] leading-5 text-gray-500"),
        class_name=CARD,
    )


def student_metrics() -> rx.Component:
    return rx.el.div(
        metric(
            "Total enrolled",
            f"{CanteenState.student_totals['enrolled']}",
            "All 28 branch/year aggregates",
            "graduation-cap",
        ),
        metric(
            "Estimated on-campus",
            f"{CanteenState.student_totals['campus']}",
            "Enrollment × campus attendance %",
            "users",
        ),
        metric(
            "Estimated canteen visitors",
            f"{CanteenState.student_totals['visitors']}",
            "On-campus × visitor %",
            "footprints",
        ),
        metric(
            "Estimated meal demand",
            f"{CanteenState.student_totals['meals']}",
            "Visitors × meal-demand %",
            "utensils",
        ),
        metric(
            "Actual meals sold · DEMO",
            f"{CanteenState.totals['sold']}",
            "Recorded sold portions; not a student count or live sales",
            "receipt-text",
        ),
        class_name="grid w-full grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-5",
    )


def slot_card(row: dict[str, str | int]) -> rx.Component:
    return rx.el.article(
        rx.el.h3(
            f"Break {row['start'].to(str)}",
            class_name="text-sm font-semibold text-[#192D26]",
        ),
        rx.el.p(
            f"{row['groups'].to(int)} active branch/year groups",
            class_name="mt-2 text-xs text-gray-600",
        ),
        rx.el.p(
            f"{row['campus'].to(int)} on-campus · {row['visitors'].to(int)} visitors · {row['meals'].to(int)} meal demand",
            class_name="mt-2 text-xs leading-6 text-[#6A4B10]",
        ),
        class_name="rounded-lg border border-[#E5D6AD] bg-[#FFF9EA] p-4",
    )


def overview() -> rx.Component:
    return rx.el.div(
        student_metrics(),
        rx.el.div(
            rx.el.section(
                title(
                    "Planning assumptions, not live attendance",
                    "FY and SY are whole-year totals distributed across seven branches. TY and BE start at zero because enrollment is unknown; zero is an editable assumption, not evidence of no students.",
                    "graduation-cap",
                ),
                rx.el.div(
                    rx.foreach(
                        CanteenState.year_totals,
                        lambda row: rx.el.div(
                            rx.el.p(
                                row["year"].to(str),
                                class_name="text-xs text-gray-600",
                            ),
                            rx.el.p(
                                f"{row['enrolled'].to(int)} enrolled",
                                class_name="mt-2 text-sm font-semibold text-[#192D26]",
                            ),
                            class_name="rounded-lg bg-[#F1F6EF] p-4",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-3 sm:grid-cols-4",
                ),
                rx.el.p(
                    "Visitor % is the share of on-campus students visiting the canteen; meal-demand % is the share of visitors expected to purchase one meal. Each stage is rounded per aggregate before summing. Inactive breaks are excluded from slot crowd summaries, not enrollment totals. Estimates are never substituted for recorded sales.",
                    class_name="mt-4 text-xs leading-6 text-gray-600",
                ),
                rx.el.button(
                    "Edit student assumptions",
                    on_click=lambda: CanteenState.select_admin_tab("Students"),
                    class_name=BUTTON,
                ),
                class_name=CARD,
            ),
            rx.el.section(
                title(
                    "Fictional organization review",
                    "Approval is a demo label, not a real due-diligence or safety process.",
                    "badge-check",
                ),
                rx.el.p(
                    f"{CanteenState.approved_organizations} approved / {CanteenState.organizations.length()} fictional NGOs",
                    class_name="text-xl font-semibold text-[#192D26]",
                ),
                rx.el.p(
                    f"{CanteenState.organizations.length() - CanteenState.approved_organizations} pending or revoked examples · {CanteenState.requests.length()} local requests",
                    class_name="my-4 text-xs leading-6 text-gray-600",
                ),
                rx.el.button(
                    "Review NGOs",
                    on_click=lambda: CanteenState.select_admin_tab(
                        "NGO verification"
                    ),
                    class_name=BUTTON,
                ),
                rx.el.p(
                    "Changing approval updates NGO golden badges and canteen partners immediately in this session. Revocation blocks new requests and progression; reject/cancel existing reservations to release portions.",
                    class_name="mt-4 text-xs leading-6 text-gray-600",
                ),
                class_name=CARD,
            ),
            class_name="grid grid-cols-1 gap-4 xl:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]",
        ),
        rx.el.section(
            title(
                "Active break start groups",
                "Multiple branches may share a start time. These are sums of active groups with exactly the same start, not measured occupancy or a full overlapping-time simulation.",
                "calendar-clock",
            ),
            rx.cond(
                CanteenState.slot_summary.length() > 0,
                rx.el.div(
                    rx.foreach(CanteenState.slot_summary, slot_card),
                    class_name="grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-3",
                ),
                rx.el.p(
                    "No active schedule groups.",
                    class_name="text-sm text-gray-500",
                ),
            ),
            class_name=CARD,
        ),
        class_name="flex w-full flex-col gap-4",
    )


def organization_card(row: OrganizationRecord) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.h3(
                row["name"], class_name="text-sm font-semibold text-[#192D26]"
            ),
            rx.cond(
                row["approved"],
                rx.el.span(
                    rx.icon("badge-check", class_name="h-4 w-4 text-[#8A641B]"),
                    "Demo approved",
                    class_name="flex h-fit w-fit shrink-0 items-center gap-1 rounded-full border border-[#C9972A]/40 bg-[#FFF0C9] px-2 py-1 text-[11px] font-semibold text-[#5A410F]",
                ),
                rx.el.span(
                    "Pending / revoked",
                    class_name="h-fit w-fit shrink-0 rounded-full bg-gray-100 px-2 py-1 text-[11px] text-gray-600",
                ),
            ),
            class_name="flex flex-wrap items-start justify-between gap-3",
        ),
        rx.el.p(
            f"{row['id']} · {row['city']}",
            class_name="mt-2 text-xs text-gray-500",
        ),
        rx.el.p(
            row["mission"], class_name="mt-3 text-xs leading-6 text-gray-600"
        ),
        rx.el.details(
            rx.el.summary(
                "Fictional contact & review context",
                class_name="my-3 cursor-pointer text-xs font-medium text-[#2E6B52]",
            ),
            rx.el.p(row["contact"], class_name="text-xs text-gray-600"),
            rx.el.p(
                row["email"], class_name="my-2 break-all text-xs text-gray-600"
            ),
            rx.el.p(
                row["contact_notes"],
                class_name="text-xs leading-6 text-gray-600",
            ),
        ),
        rx.el.div(
            rx.el.button(
                "Approve locally",
                disabled=row["approved"],
                on_click=lambda: CanteenState.set_ngo_approval(row["id"], True),
                class_name=BUTTON,
            ),
            rx.el.button(
                "Revoke locally",
                disabled=~row["approved"],
                on_click=lambda: CanteenState.set_ngo_approval(
                    row["id"], False
                ),
                class_name="rounded-lg border border-gray-300 bg-white px-3 py-2 text-xs font-medium text-gray-700 hover:bg-gray-100 focus-visible:outline-2 focus-visible:outline-[#6A4B10] disabled:opacity-40",
            ),
            class_name="mt-4 flex gap-2",
        ),
        rx.el.p(
            "No documents checked, external contact or real-world verification.",
            class_name="mt-3 text-[11px] text-gray-500",
        ),
        key=row["id"],
        class_name=CARD,
    )


def verification() -> rx.Component:
    return rx.el.div(
        rx.el.section(
            title(
                "NGO verification · fictional directory",
                "All 15 profiles are fictional. Initial state deliberately mixes 10 approved and 5 pending examples. Actions are open demo controls, not protected review decisions.",
                "badge-check",
            ),
            rx.el.p(
                f"{CanteenState.approved_organizations} currently approved; only these examples have a golden NGO badge and request eligibility.",
                class_name="text-xs text-[#6A4B10]",
            ),
            class_name=CARD,
        ),
        rx.el.div(
            rx.foreach(CanteenState.organizations, organization_card),
            class_name="grid grid-cols-1 gap-4 xl:grid-cols-2",
        ),
        class_name="flex w-full flex-col gap-4",
    )


def filters() -> rx.Component:
    return rx.el.form(
        select_field(
            "Year",
            "year",
            ["All years", "FY", "SY", "TY", "BE"],
            CanteenState.planning_year,
        ),
        select_field(
            "Branch",
            "branch",
            CanteenState.branches,
            CanteenState.planning_branch,
        ),
        rx.el.button(
            rx.icon("filter", class_name="h-4 w-4"),
            "Apply view",
            type="submit",
            class_name=OUTLINE,
        ),
        on_submit=CanteenState.save_planning_filter,
        class_name="mb-4 grid grid-cols-1 items-end gap-3 sm:grid-cols-[1fr_1fr_auto]",
    )


def group_metrics(row: BreakSlot) -> rx.Component:
    return rx.el.p(
        f"{row['enrolled']} enrolled → {row['expected']} on-campus → {row['visitors']} visitors → {row['meals']} meal demand",
        class_name="my-3 text-xs font-medium leading-6 text-[#6A4B10]",
    )


def student_row(row: BreakSlot) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.h3(
                f"{row['year']} · {row['branch']}",
                class_name="text-sm font-semibold text-[#192D26]",
            ),
            rx.el.span(
                rx.cond(
                    (row["year"] == "TY") | (row["year"] == "BE"),
                    "Editable assumption · initially unknown",
                    "Allocated whole-year seed total",
                ),
                class_name="text-[11px] text-gray-500",
            ),
            class_name="flex flex-wrap justify-between gap-2",
        ),
        group_metrics(row),
        rx.el.form(
            field(
                "Enrollment (whole students)",
                "enrolled",
                row["enrolled"],
                "number",
                min=0,
                max=100000,
                step=1,
                required=True,
            ),
            field(
                "Campus attendance %",
                "attendance",
                row["attendance"],
                "number",
                min=0,
                max=100,
                step=1,
                required=True,
            ),
            field(
                "Canteen visitors % of campus",
                "visitors_pct",
                row["visitors_pct"],
                "number",
                min=0,
                max=100,
                step=1,
                required=True,
            ),
            field(
                "Meal demand % of visitors",
                "meals_pct",
                row["meals_pct"],
                "number",
                min=0,
                max=100,
                step=1,
                required=True,
            ),
            rx.el.button("Save aggregate", type="submit", class_name=BUTTON),
            on_submit=lambda data: CanteenState.save_students(row["id"], data),
            key=CanteenState.planning_revision,
            class_name="grid grid-cols-1 items-end gap-3 sm:grid-cols-2 xl:grid-cols-[repeat(4,minmax(0,1fr))_auto]",
        ),
        key=row["id"],
        class_name=CARD,
    )


def students() -> rx.Component:
    return rx.el.div(
        student_metrics(),
        rx.el.section(
            title(
                "Year / branch aggregate enrollment",
                "No individual student records. FY starts at 1000 total and SY at 800 total, each distributed over seven branches. TY and BE start at 0 (unknown). Enrollment edits change the whole-year total; no hidden multiplication or automatic redistribution. All percentages must be whole numbers from 0–100.",
                "graduation-cap",
            ),
            filters(),
            rx.el.p(
                "Estimates use sequential percentages: enrolled → on-campus → canteen visitors → meal demand. Food operations supply recorded sales separately; sales are not assigned to a branch/year without observations.",
                class_name="text-xs leading-6 text-gray-600",
            ),
            class_name=CARD,
        ),
        rx.foreach(CanteenState.planning_rows, student_row),
        class_name="flex w-full flex-col gap-4",
    )


def schedule_row(row: BreakSlot) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.h3(
                f"{row['year']} · {row['branch']}",
                class_name="text-sm font-semibold text-[#192D26]",
            ),
            rx.el.span(
                rx.cond(row["active"], "Active", "Inactive"),
                class_name=rx.cond(
                    row["active"],
                    "w-fit rounded-md bg-[#EAF2E6] px-2 py-1 text-xs text-[#2E6B52]",
                    "w-fit rounded-md bg-gray-100 px-2 py-1 text-xs text-gray-600",
                ),
            ),
            class_name="flex justify-between gap-2",
        ),
        group_metrics(row),
        rx.el.form(
            field(
                "Start · campus local time",
                "start",
                row["start"],
                "time",
                required=True,
            ),
            field(
                "End · same sample day",
                "end",
                row["end"],
                "time",
                required=True,
            ),
            rx.el.label(
                rx.el.input(
                    type="checkbox",
                    name="active",
                    default_checked=row["active"],
                    key=row["active"],
                    class_name="h-4 w-4 accent-[#C9972A]",
                ),
                "Active schedule",
                class_name="flex items-center gap-2 py-2 text-xs text-gray-700",
            ),
            rx.el.button("Save schedule", type="submit", class_name=BUTTON),
            on_submit=lambda data: CanteenState.save_admin_schedule(
                row["id"], data
            ),
            key=CanteenState.planning_revision,
            class_name="grid grid-cols-1 items-end gap-3 sm:grid-cols-2 xl:grid-cols-4",
        ),
        key=row["id"],
        class_name=CARD,
    )


def schedules() -> rx.Component:
    return rx.el.div(
        rx.el.section(
            title(
                "Break schedules · all 28 combinations",
                "Initial starts cycle through 11:15, 12:15 and 13:15, with 30-minute windows. End must follow start on the same sample day. Shared slots are allowed. These settings update canteen Break planning without altering enrollment or sales.",
                "calendar-clock",
            ),
            filters(),
            class_name=CARD,
        ),
        rx.el.div(
            rx.foreach(CanteenState.slot_summary, slot_card),
            class_name="grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-3",
        ),
        rx.foreach(CanteenState.planning_rows, schedule_row),
        class_name="flex w-full flex-col gap-4",
    )


def food_row(row: OperationView) -> rx.Component:
    return rx.el.article(
        rx.el.h3(
            row["name"], class_name="text-sm font-semibold text-[#192D26]"
        ),
        rx.el.p(
            f"{row['location']} · {row['status']} · {row['eligibility']}",
            class_name="mt-2 text-xs text-gray-500",
        ),
        rx.el.p(
            f"{row['prepared']} prepared · {row['sold']} sold · {row['collected']} collected (simulated) · {row['remaining']} remaining · {row['listed']} listed",
            class_name="my-3 text-xs leading-6 text-gray-600",
        ),
        rx.el.form(
            field(
                "Food name", "name", row["name"], required=True, max_length=100
            ),
            field(
                "Prepared portions",
                "prepared",
                row["prepared"],
                "number",
                min=0,
                max=100000,
                step=1,
                required=True,
            ),
            field(
                "Sold portions",
                "sold",
                row["sold"],
                "number",
                min=0,
                max=100000,
                step=1,
                required=True,
            ),
            rx.el.button("Save food record", type="submit", class_name=BUTTON),
            on_submit=lambda data: CanteenState.save_operation(row["id"], data),
            key=CanteenState.inventory_revision,
            class_name="grid grid-cols-1 items-end gap-3 sm:grid-cols-2 xl:grid-cols-4",
        ),
        rx.el.a(
            "Review surplus / handling in Canteen →",
            href="/canteen",
            class_name="mt-3 inline-block text-xs font-medium text-[#2E6B52] underline",
        ),
        key=row["id"],
        class_name=CARD,
    )


def account_row(row: AccountRecord) -> rx.Component:
    return rx.el.article(
        rx.el.h3(
            row["name"], class_name="text-sm font-semibold text-[#192D26]"
        ),
        rx.el.p(
            row["email"], class_name="mt-2 break-all text-xs text-gray-500"
        ),
        rx.el.form(
            select_field(
                "Illustrative role label",
                "role",
                ["Student", "Canteen", "NGO", "Admin"],
                row["role"],
            ),
            select_field(
                "Illustrative roster status",
                "status",
                ["Illustrative active", "Illustrative inactive"],
                row["status"],
            ),
            rx.el.button(
                "Save fictional labels", type="submit", class_name=OUTLINE
            ),
            on_submit=lambda data: CanteenState.save_account_label(
                row["id"], data
            ),
            class_name="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2",
        ),
        rx.el.p(
            "Not a login, account activation, permission grant or real user record.",
            class_name="mt-3 text-[11px] leading-5 text-gray-500",
        ),
        key=row["id"],
        class_name=CARD,
    )


def food_users() -> rx.Component:
    return rx.el.div(
        rx.el.section(
            title(
                "Food oversight · shared local operations",
                "Uses the same editable food records and request workflow as Canteen/NGO. Prepared must cover sold + collected + listed portions. No real orders, prices or food-safety checks.",
                "cooking-pot",
            ),
            class_name=CARD,
        ),
        rx.foreach(CanteenState.rows, food_row),
        canteen_requests(),
        rx.el.section(
            title(
                "Fictional account roster · NOT real user management",
                "12 Faker-generated illustrative profiles with non-operational addresses. Role and status changes only edit roster labels; they provide no authentication, access protection or permissions. NGO approval remains in the separate verification directory.",
                "users",
            ),
            class_name=CARD,
        ),
        rx.el.div(
            rx.foreach(CanteenState.accounts, account_row),
            class_name="grid grid-cols-1 gap-4 xl:grid-cols-2",
        ),
        class_name="flex w-full flex-col gap-4",
    )


def announcement_editor(row: TargetedAnnouncement) -> rx.Component:
    return rx.el.article(
        rx.cond(row["id"] != "", targeted_card(row)),
        rx.el.form(
            field(
                "Announcement title",
                "title",
                row["title"],
                required=True,
                max_length=80,
            ),
            select_field(
                "Target year",
                "year",
                ["All years", "FY", "SY", "TY", "BE"],
                row["year"],
            ),
            field("Break time", "start", row["start"], "time", required=True),
            select_field(
                "Expected crowd · assumption",
                "crowd",
                ["Low", "Moderate", "High"],
                row["crowd"],
            ),
            rx.el.fieldset(
                rx.el.legend(
                    "Target branches · select at least one",
                    class_name="mb-2 text-xs font-medium text-gray-600",
                ),
                rx.el.div(
                    rx.foreach(
                        CanteenState.branches[1:],
                        lambda branch: rx.el.label(
                            rx.el.input(
                                type="checkbox",
                                name=branch,
                                default_checked=row["branches"].contains(
                                    branch
                                ),
                                key=row["branches"].contains(branch),
                                class_name="h-4 w-4 accent-[#C9972A]",
                            ),
                            branch,
                            class_name="flex items-center gap-2 text-xs text-gray-700",
                        ),
                    ),
                    class_name="flex flex-wrap gap-4",
                ),
                class_name="col-span-full",
            ),
            rx.el.label(
                rx.el.span(
                    "Optional queue / occupancy note · illustrative, not live measured",
                    class_name="mb-2 block text-xs text-gray-600",
                ),
                rx.el.textarea(
                    name="note",
                    default_value=row["note"],
                    key=row["note"],
                    max_length=500,
                    rows=2,
                    class_name=INPUT,
                ),
                class_name="col-span-full",
            ),
            rx.el.div(
                rx.el.button(
                    rx.cond(
                        row["id"] == "",
                        "Save targeted announcement locally",
                        "Save local edits",
                    ),
                    type="submit",
                    class_name=BUTTON,
                ),
                rx.cond(
                    row["id"] != "",
                    rx.el.button(
                        "Remove",
                        type="button",
                        on_click=lambda: (
                            CanteenState.remove_targeted_announcement(row["id"])
                        ),
                        class_name=OUTLINE,
                    ),
                ),
                class_name="col-span-full flex flex-wrap gap-2",
            ),
            on_submit=lambda data: CanteenState.save_targeted_announcement(
                row["id"], data
            ),
            class_name="mt-3 grid grid-cols-1 gap-3 sm:grid-cols-2",
        ),
        key=row["id"],
        class_name=CARD,
    )


def analytics() -> rx.Component:
    return rx.el.div(
        rx.el.section(
            title(
                "Demo analytics · traceable portion balance",
                "Only local food records and request statuses. No invented live statistics, carbon estimates or historical trends. Remaining includes listed surplus; available excludes active reservations. Sold portions are demo recorded meals, not real-world outcomes.",
                "chart-no-axes-combined",
            ),
            rx.el.div(
                metric(
                    "Prepared",
                    f"{CanteenState.totals['prepared']}",
                    "Recorded portions",
                    "cooking-pot",
                ),
                metric(
                    "Sold",
                    f"{CanteenState.totals['sold']}",
                    f"{CanteenState.sell_through:.1f}% sell-through",
                    "receipt-text",
                ),
                metric(
                    "Collected · simulation",
                    f"{CanteenState.totals['collected']}",
                    "Sample seed + simulated handovers",
                    "hand-heart",
                ),
                metric(
                    "Remaining",
                    f"{CanteenState.totals['remaining']}",
                    f"{CanteenState.totals['available']} unreserved available surplus",
                    "package",
                ),
                class_name="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4",
            ),
            rx.el.p(
                f"Balance: {CanteenState.totals['prepared']} prepared = {CanteenState.totals['sold']} sold + {CanteenState.totals['collected']} collected + {CanteenState.totals['remaining']} remaining.",
                class_name="mt-4 text-xs text-gray-600",
            ),
            rx.el.div(
                rx.foreach(
                    [
                        "Pending",
                        "Approved",
                        "Confirmed",
                        "Collected",
                        "Rejected",
                        "Cancelled",
                    ],
                    lambda status: rx.el.div(
                        rx.el.p(status, class_name="text-xs text-gray-500"),
                        rx.el.p(
                            CanteenState.requests.filter(
                                lambda request: request["status"] == status
                            ).length(),
                            class_name="mt-1 text-xl font-semibold text-[#192D26]",
                        ),
                        class_name="rounded-lg border border-gray-200 bg-white p-3",
                    ),
                ),
                class_name="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-3 xl:grid-cols-6",
            ),
            class_name=CARD,
        ),
        rx.el.section(
            title(
                "Local notification settings",
                "These controls govern activity notices only, not email/SMS/push delivery. Saved targeted announcements stay visible locally even if activity alerts are paused.",
                "bell",
            ),
            rx.el.div(
                rx.el.button(
                    rx.cond(
                        CanteenState.alerts_enabled,
                        "Pause local activity alerts",
                        "Enable local activity alerts",
                    ),
                    on_click=CanteenState.toggle_alerts,
                    class_name=BUTTON,
                ),
                rx.el.button(
                    "Mark activity read",
                    on_click=CanteenState.mark_read,
                    class_name=OUTLINE,
                ),
                rx.el.button(
                    "Clear local activity",
                    on_click=CanteenState.clear_notices,
                    class_name=OUTLINE,
                ),
                class_name="flex flex-wrap gap-2",
            ),
            rx.el.p(
                f"{CanteenState.unread} unread local notices",
                class_name="my-3 text-xs text-gray-600",
            ),
            rx.el.div(
                rx.foreach(
                    CanteenState.notices,
                    lambda notice: rx.el.article(
                        rx.el.h3(
                            notice["title"],
                            class_name="text-xs font-semibold text-[#192D26]",
                        ),
                        rx.el.p(
                            notice["text"],
                            class_name="mt-2 text-xs leading-6 text-gray-600",
                        ),
                        rx.el.p(
                            rx.cond(notice["read"], "Read", "Unread"),
                            class_name="mt-2 text-[11px] text-gray-500",
                        ),
                        key=notice["id"],
                        class_name="rounded-lg border border-gray-200 bg-[#FAFBF8] p-3",
                    ),
                ),
                class_name="flex max-h-72 flex-col gap-3 overflow-y-auto",
            ),
            class_name=CARD,
        ),
        rx.el.section(
            title(
                "Targeted canteen announcements",
                "Save locally by year, branch and break time. Crowd level and optional queue notes are manual demo assumptions; no student recipients or external delivery. View them in Canteen Break planning and Notifications.",
                "megaphone",
            ),
            class_name=CARD,
        ),
        announcement_editor(
            rx.Var.create(
                {
                    "id": "",
                    "title": "",
                    "year": "All years",
                    "branches": [],
                    "start": "11:15",
                    "crowd": "Moderate",
                    "note": "",
                }
            ).to(TargetedAnnouncement)
        ),
        rx.cond(
            CanteenState.targeted_announcements.length() > 0,
            rx.foreach(
                CanteenState.targeted_announcements, announcement_editor
            ),
            rx.el.p(
                "No targeted announcements saved yet.",
                class_name="text-xs text-gray-500",
            ),
        ),
        class_name="flex w-full flex-col gap-4",
    )


def tab_button(tab: str) -> rx.Component:
    return rx.el.button(
        rx.match(
            tab,
            (
                "Overview",
                rx.icon("layout-dashboard", class_name="h-4 w-4 shrink-0"),
            ),
            (
                "NGO verification",
                rx.icon("badge-check", class_name="h-4 w-4 shrink-0"),
            ),
            (
                "Students",
                rx.icon("graduation-cap", class_name="h-4 w-4 shrink-0"),
            ),
            (
                "Break schedules",
                rx.icon("calendar-clock", class_name="h-4 w-4 shrink-0"),
            ),
            ("Food & users", rx.icon("users", class_name="h-4 w-4 shrink-0")),
            rx.icon("bell", class_name="h-4 w-4 shrink-0"),
        ),
        tab,
        on_click=lambda: CanteenState.select_admin_tab(tab),
        aria_current=rx.cond(CanteenState.admin_tab == tab, "page", "false"),
        class_name=rx.cond(
            CanteenState.admin_tab == tab,
            "flex shrink-0 items-center gap-3 whitespace-nowrap rounded-lg bg-[#C9972A] px-3 py-3 text-left text-xs font-semibold text-[#30250F] focus-visible:outline-2 focus-visible:outline-[#6A4B10]",
            "flex shrink-0 items-center gap-3 whitespace-nowrap rounded-lg bg-transparent px-3 py-3 text-left text-xs font-medium text-gray-600 hover:bg-[#F4EDD9] focus-visible:outline-2 focus-visible:outline-[#6A4B10]",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.p(
                "CAMPUS / DEMO ADMIN",
                class_name="text-[10px] font-semibold tracking-widest text-[#8A641B]",
            ),
            rx.el.h2(
                "A clearer campus picture",
                class_name="mt-3 font-['DM_Sans'] text-base font-semibold text-[#192D26]",
            ),
            rx.el.p(
                "Local assumptions & oversight",
                class_name="mt-2 text-xs text-gray-500",
            ),
            class_name="shrink-0 border-b border-[#E5E1D6] p-5",
        ),
        rx.el.nav(
            rx.foreach(CanteenState.admin_tabs, tab_button),
            aria_label="Admin sections",
            class_name="flex min-h-0 flex-1 flex-col gap-1 overflow-y-auto p-3",
        ),
        rx.el.div(
            rx.icon("triangle-alert", class_name="mb-3 h-5 w-5 text-[#8A641B]"),
            rx.el.p(
                "Open controls, not role security",
                class_name="text-xs font-semibold text-[#192D26]",
            ),
            rx.el.p(
                "Session-local only. No real accounts or Supabase persistence. Do not enter personal information.",
                class_name="mt-2 text-[11px] leading-6 text-gray-600",
            ),
            class_name="m-3 rounded-xl border border-[#E5D6AD] bg-[#FFF9EA] p-4",
        ),
        class_name="hidden h-full w-60 shrink-0 flex-col border-r border-[#E5E1D6] bg-[#FAFCF7] lg:flex",
    )


def admin_workspace() -> rx.Component:
    return rx.el.div(
        rx.el.a(
            "Skip to admin workspace",
            href="#admin-main",
            class_name="sr-only bg-white p-3 text-[#192D26] focus:not-sr-only focus:fixed focus:left-3 focus:top-3 focus:z-50",
        ),
        rx.el.header(
            brand(),
            rx.el.nav(
                rx.foreach(
                    [
                        {"label": "Home", "href": "/"},
                        {"label": "Canteen", "href": "/canteen"},
                        {"label": "NGO", "href": "/ngo"},
                        {"label": "Admin", "href": "/admin"},
                    ],
                    lambda item: rx.el.a(
                        item["label"],
                        href=item["href"],
                        aria_current=rx.cond(
                            item["label"] == "Admin", "page", "false"
                        ),
                        class_name=rx.cond(
                            item["label"] == "Admin",
                            "rounded-lg bg-[#C9972A] px-3 py-2 text-xs font-semibold text-[#30250F]",
                            "rounded-lg bg-white px-3 py-2 text-xs font-medium text-gray-600 hover:bg-[#F4EDD9] focus-visible:outline-2 focus-visible:outline-[#6A4B10]",
                        ),
                    ),
                ),
                aria_label="Demo workspaces",
                class_name="flex flex-wrap gap-1",
            ),
            rx.el.span(
                "Demo Data · no sign-in",
                class_name="hidden w-fit rounded-full border border-[#2E6B52]/20 bg-[#EAF2E6] px-3 py-2 text-xs text-[#2E6B52] sm:block",
            ),
            class_name="flex shrink-0 flex-wrap items-center justify-between gap-3 border-b border-gray-200 bg-white px-4 py-3 sm:px-6",
        ),
        rx.el.div(
            sidebar(),
            rx.el.main(
                rx.el.nav(
                    rx.foreach(CanteenState.admin_tabs, tab_button),
                    aria_label="Mobile admin sections",
                    class_name="mb-4 flex gap-2 overflow-x-auto pb-2 lg:hidden",
                ),
                rx.el.p(
                    "ADMIN / LOCAL DEMO",
                    class_name="text-[10px] font-semibold tracking-widest text-[#8A641B]",
                ),
                rx.el.h1(
                    CanteenState.admin_tab,
                    class_name="mb-2 mt-2 font-['DM_Sans'] text-3xl font-semibold tracking-tight text-[#192D26]",
                ),
                rx.el.p(
                    "Thoughtful planning. Transparent assumptions.",
                    class_name="mb-5 text-xs text-gray-600",
                ),
                rx.el.div(
                    rx.icon(
                        "triangle-alert",
                        class_name="h-5 w-5 shrink-0 text-[#6A4B10]",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Open demo — admin actions are not access-protected, not saved to Supabase",
                            class_name="text-sm font-semibold text-[#49360F]",
                        ),
                        rx.el.p(
                            "Fictional records only. Updates are session-local, may reset, and are shared only across demo workspaces in this session. No real account management, verified safety, live occupancy or external delivery.",
                            class_name="mt-2 text-xs leading-6 text-[#614A1B]",
                        ),
                    ),
                    role="note",
                    class_name="mb-5 flex items-start gap-3 rounded-xl border border-[#C9972A]/50 bg-[#FFF0CA] p-4",
                ),
                rx.cond(
                    CanteenState.feedback != "",
                    rx.el.div(
                        CanteenState.feedback,
                        role="status",
                        aria_live="polite",
                        class_name=rx.cond(
                            CanteenState.error,
                            "mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-xs leading-6 text-red-700",
                            "mb-4 rounded-lg border border-green-200 bg-green-50 p-3 text-xs leading-6 text-green-700",
                        ),
                    ),
                ),
                rx.match(
                    CanteenState.admin_tab,
                    ("Overview", overview()),
                    ("NGO verification", verification()),
                    ("Students", students()),
                    ("Break schedules", schedules()),
                    ("Food & users", food_users()),
                    ("Notifications/analytics", analytics()),
                    overview(),
                ),
                rx.el.p(
                    "Canteenio · open admin demo · no live backend or real-world outcomes",
                    class_name="mt-6 text-center text-[11px] text-gray-500",
                ),
                id="admin-main",
                class_name="min-w-0 w-full flex-1 overflow-y-auto bg-[#FBF8F0] p-4 sm:p-6 xl:p-8",
            ),
            class_name="flex min-h-0 flex-1",
        ),
        class_name="flex h-dvh w-full flex-col overflow-hidden bg-white font-['Inter'] text-[#192D26] antialiased",
    )
