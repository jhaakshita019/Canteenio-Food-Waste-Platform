import reflex as rx
import reflex_xy
from app.components.shared import brand
from app.components.collection_requests import canteen_requests
from app.components.targeted_announcements import targeted_list
from app.states.canteen_state import (
    CanteenState,
    OperationView,
    BreakSlot,
    Notice,
    ConversationMessage,
)

BUTTON = "inline-flex items-center justify-center gap-2 rounded-lg bg-[#17324F] px-4 py-2 text-xs font-semibold text-white transition-colors hover:bg-[#244868] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#17324F] disabled:cursor-not-allowed disabled:opacity-40"
OUTLINE = "inline-flex items-center justify-center gap-2 rounded-lg border border-gray-200 bg-white px-3 py-2 text-xs font-medium text-[#17324F] hover:bg-[#F0F5FA] focus-visible:outline-2 focus-visible:outline-[#17324F] disabled:cursor-not-allowed disabled:opacity-40"
INPUT = "w-full min-w-0 rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-800 focus:border-[#17324F] focus:outline-2 focus:outline-[#17324F]/20"
CARD = "w-full min-w-0 rounded-xl border border-gray-200 bg-white p-5"
CELL = "px-4 py-3 text-left text-xs text-gray-600"


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
                class_name="w-full appearance-none rounded-lg border border-gray-300 bg-white py-2 pl-3 pr-8 text-sm text-gray-800 focus:outline-2 focus:outline-[#17324F]",
            ),
            rx.icon(
                "chevron-down",
                class_name="pointer-events-none absolute right-3 top-3 h-4 w-4 text-gray-500",
            ),
            class_name="relative",
        ),
        class_name="block min-w-0",
    )


def title_block(title: str, description: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5 text-[#17324F]"),
            rx.el.h2(
                title,
                class_name="font-['DM_Sans'] text-lg font-semibold text-[#17324F]",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(description, class_name="mt-2 text-xs leading-5 text-gray-500"),
        class_name="mb-5",
    )


def workspace_routes() -> rx.Component:
    return rx.el.nav(
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
                    item["label"] == "Canteen", "page", "false"
                ),
                class_name=rx.cond(
                    item["label"] == "Canteen",
                    "rounded-lg bg-[#17324F] px-3 py-2 text-xs font-semibold text-white",
                    "rounded-lg bg-white px-3 py-2 text-xs font-medium text-gray-600 hover:bg-[#F0F5FA] focus-visible:outline-2 focus-visible:outline-[#17324F]",
                ),
            ),
        ),
        aria_label="Demo workspaces",
        class_name="flex flex-wrap items-center gap-1",
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
                "Inventory",
                rx.icon("cooking-pot", class_name="h-4 w-4 shrink-0"),
            ),
            ("Surplus", rx.icon("leaf", class_name="h-4 w-4 shrink-0")),
            (
                "Break planning",
                rx.icon("calendar-clock", class_name="h-4 w-4 shrink-0"),
            ),
            ("Notifications", rx.icon("bell", class_name="h-4 w-4 shrink-0")),
            (
                "Requests",
                rx.icon("clipboard-list", class_name="h-4 w-4 shrink-0"),
            ),
            rx.icon("messages-square", class_name="h-4 w-4 shrink-0"),
        ),
        tab,
        rx.cond(
            tab == "Notifications",
            rx.el.span(
                CanteenState.unread,
                class_name="ml-auto w-fit rounded-md bg-white/20 px-1.5 text-[10px]",
            ),
        ),
        on_click=lambda: CanteenState.select_tab(tab),
        aria_current=rx.cond(CanteenState.tab == tab, "page", "false"),
        class_name=rx.cond(
            CanteenState.tab == tab,
            "flex shrink-0 items-center gap-3 whitespace-nowrap rounded-lg bg-[#17324F] px-3 py-3 text-xs font-semibold text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#17324F]",
            "flex shrink-0 items-center gap-3 whitespace-nowrap rounded-lg bg-transparent px-3 py-3 text-xs font-medium text-gray-600 hover:bg-[#EAF1F7] focus-visible:outline-2 focus-visible:outline-[#17324F]",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.p(
                "CAMPUS OPERATIONS",
                class_name="text-[10px] font-semibold tracking-widest text-gray-400",
            ),
            rx.el.p(
                "Canteen workspace",
                class_name="mt-2 text-sm font-semibold text-[#17324F]",
            ),
            rx.el.p(
                "Local demo session", class_name="mt-1 text-xs text-gray-500"
            ),
            class_name="shrink-0 border-b border-gray-200 p-5",
        ),
        rx.el.nav(
            rx.foreach(CanteenState.tabs, tab_button),
            aria_label="Canteen sections",
            class_name="flex min-h-0 flex-1 flex-col gap-1 overflow-y-auto p-3",
        ),
        rx.el.div(
            rx.icon("shield", class_name="mb-3 h-5 w-5 text-[#2E6B52]"),
            rx.el.p(
                "A safe place to explore",
                class_name="text-xs font-semibold text-[#192D26]",
            ),
            rx.el.p(
                "No sign-in. No live database. Changes are temporary and may reset when the session ends.",
                class_name="mt-2 text-[11px] leading-5 text-gray-500",
            ),
            class_name="m-3 rounded-xl border border-[#2E6B52]/15 bg-[#DCEBDC]/30 p-4",
        ),
        class_name="hidden h-full w-56 shrink-0 flex-col border-r border-gray-200 bg-[#FAFCFD] lg:flex",
    )


def stat(label: str, value: str, icon: str, note: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(label, class_name="text-xs font-medium text-gray-500"),
            rx.icon(icon, class_name="h-4 w-4 text-[#17324F]"),
            class_name="flex items-center justify-between gap-2",
        ),
        rx.el.p(
            value,
            class_name="mt-3 font-['DM_Sans'] text-3xl font-semibold tracking-tight text-[#17324F]",
        ),
        rx.el.p(note, class_name="mt-2 text-[10px] leading-4 text-gray-500"),
        class_name=CARD,
    )


def empty(text: str) -> rx.Component:
    return rx.el.div(
        rx.icon("inbox", class_name="mx-auto mb-3 h-6 w-6 text-gray-400"),
        rx.el.p(text, class_name="text-xs leading-5 text-gray-500"),
        class_name="rounded-xl border border-dashed border-gray-300 bg-[#F7FAFD] px-5 py-8 text-center",
    )


def chart_panel() -> rx.Component:
    return rx.el.section(
        title_block(
            "Demo Data · Portion balance",
            "Values come directly from your editable food records. Sold + collected + remaining = prepared. Listed surplus is part of remaining, not additional food.",
            "chart-no-axes-combined",
        ),
        rx.cond(
            CanteenState.operations.length() > 0,
            rx.el.div(
                reflex_xy.chart(
                    reflex_xy.bar(
                        "food",
                        "sold",
                        name="Sold",
                        color="#17324F",
                        orientation="horizontal",
                    ),
                    reflex_xy.bar(
                        "food",
                        "collected",
                        name="Collected (simulated)",
                        color="#2E6B52",
                        orientation="horizontal",
                    ),
                    reflex_xy.bar(
                        "food",
                        "remaining",
                        name="Remaining",
                        color="#A8C5DB",
                        orientation="horizontal",
                    ),
                    reflex_xy.x_axis(label="Sample portions"),
                    reflex_xy.y_axis(label="Food record"),
                    reflex_xy.legend(),
                    reflex_xy.modebar(False),
                    reflex_xy.interaction_config(navigation=False),
                    data=CanteenState.portion_chart,
                    height="340px",
                    class_name="w-full min-w-[300px]",
                ),
                class_name="h-[340px] w-full shrink-0 overflow-x-auto",
            ),
            empty("No food records to chart. Add a food record in Inventory."),
        ),
        class_name=CARD,
    )


def overview_row(row: OperationView) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.p(row["name"], class_name="font-medium text-[#17324F]"),
            rx.el.p(
                row["location"], class_name="mt-1 text-[10px] text-gray-400"
            ),
            class_name=CELL,
        ),
        rx.el.td(row["prepared"], class_name=CELL),
        rx.el.td(row["sold"], class_name=CELL),
        rx.el.td(row["remaining"], class_name=CELL),
        rx.el.td(
            rx.el.span(
                row["status"],
                class_name=rx.cond(
                    row["status"] == "Available",
                    "w-fit rounded-md bg-green-100 px-2 py-1 text-[10px] text-green-600",
                    "w-fit rounded-md bg-[#EAF1F7] px-2 py-1 text-[10px] text-[#17324F]",
                ),
            ),
            class_name=CELL,
        ),
        key=row["id"],
        class_name="border-b border-gray-100 last:border-0 even:bg-[#F8FAFC] hover:bg-[#F0F5FA]",
    )


def table_header(label: str, icon: str) -> rx.Component:
    return rx.el.th(
        rx.el.div(
            rx.icon(icon, class_name="h-3.5 w-3.5"),
            label,
            class_name="flex items-center gap-2",
        ),
        class_name="whitespace-nowrap px-4 py-3 text-left text-[10px] font-semibold uppercase tracking-wider text-gray-500",
    )


def overview() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            stat(
                "Prepared",
                f"{CanteenState.totals['prepared']}",
                "cooking-pot",
                "Total sample portions prepared",
            ),
            stat(
                "Sold",
                f"{CanteenState.totals['sold']}",
                "receipt-text",
                f"{CanteenState.sell_through:.1f}% of prepared portions",
            ),
            stat(
                "Remaining",
                f"{CanteenState.totals['remaining']}",
                "package",
                f"{CanteenState.totals['listed']} portions allocated to surplus",
            ),
            stat(
                "Available surplus",
                f"{CanteenState.totals['available']}",
                "leaf",
                "Reviewed, available demo listings only",
            ),
            class_name="grid w-full grid-cols-2 gap-3 xl:grid-cols-4",
        ),
        rx.el.div(
            chart_panel(),
            rx.el.section(
                title_block(
                    "Your next steps",
                    "Small actions keep the demo food cycle coherent.",
                    "clipboard-check",
                ),
                rx.el.div(
                    rx.icon("cooking-pot", class_name="h-5 w-5 text-[#17324F]"),
                    rx.el.p(
                        "1. Prepare and record sales",
                        class_name="text-sm font-semibold text-[#17324F]",
                    ),
                    rx.el.p(
                        "Only unallocated portions can be sold with quick actions.",
                        class_name="text-xs leading-5 text-gray-500",
                    ),
                    rx.el.button(
                        "Open inventory",
                        on_click=lambda: CanteenState.select_tab("Inventory"),
                        class_name=OUTLINE,
                    ),
                    class_name="flex flex-col items-start gap-3 border-b border-gray-100 pb-5",
                ),
                rx.el.div(
                    rx.icon("leaf", class_name="h-5 w-5 text-[#2E6B52]"),
                    rx.el.p(
                        "2. Review surplus drafts",
                        class_name="text-sm font-semibold text-[#17324F]",
                    ),
                    rx.el.p(
                        "Start with portions, a pickup window and handling notes. Nothing is actually published.",
                        class_name="text-xs leading-5 text-gray-500",
                    ),
                    rx.el.button(
                        "Manage surplus",
                        on_click=lambda: CanteenState.select_tab("Surplus"),
                        class_name=OUTLINE,
                    ),
                    class_name="mt-5 flex flex-col items-start gap-3",
                ),
                rx.el.p(
                    f"{CanteenState.totals['collected']} portions recorded as collected in sample records; not real donations.",
                    class_name="mt-5 rounded-lg bg-[#F0F5FA] p-3 text-[11px] leading-5 text-gray-500",
                ),
                class_name=CARD,
            ),
            class_name="grid w-full grid-cols-1 gap-4 xl:grid-cols-[minmax(0,2fr)_minmax(300px,1fr)]",
        ),
        rx.el.section(
            title_block(
                "Food at a glance",
                "All locations · one editable local dataset",
                "utensils",
            ),
            rx.cond(
                CanteenState.rows.length() > 0,
                rx.el.div(
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    table_header("Food / location", "utensils"),
                                    table_header("Prepared", "cooking-pot"),
                                    table_header("Sold", "receipt-text"),
                                    table_header("Remaining", "package"),
                                    table_header("Listing", "leaf"),
                                ),
                                class_name="bg-[#F4F7FA]",
                            ),
                            rx.el.tbody(
                                rx.foreach(CanteenState.rows, overview_row)
                            ),
                            class_name="table-auto w-full min-w-[600px]",
                        ),
                        class_name="overflow-x-auto",
                    ),
                    class_name="overflow-hidden rounded-lg border border-gray-200",
                ),
                empty("No local inventory yet. Open Inventory to add food."),
            ),
            class_name=CARD,
        ),
        class_name="flex w-full flex-col gap-4",
    )


def inventory_row(row: OperationView) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.p(row["name"], class_name="font-semibold text-[#17324F]"),
            rx.el.p(
                row["location"], class_name="mt-1 text-[10px] text-gray-500"
            ),
            rx.el.p(
                f"Allergens: {row['allergens']}",
                class_name="mt-1 text-[10px] text-gray-500",
            ),
            class_name=CELL,
        ),
        rx.el.td(row["prepared"], class_name=CELL),
        rx.el.td(row["sold"], class_name=CELL),
        rx.el.td(row["collected"], class_name=CELL),
        rx.el.td(row["remaining"], class_name=CELL),
        rx.el.td(row["unallocated"], class_name=CELL),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    "+10 prepare",
                    on_click=lambda: CanteenState.quick_update(
                        row["id"], "prepare"
                    ),
                    class_name=OUTLINE,
                ),
                rx.el.button(
                    "+5 sold",
                    on_click=lambda: CanteenState.quick_update(
                        row["id"], "sell"
                    ),
                    disabled=row["unallocated"] < 5,
                    class_name=BUTTON,
                ),
                rx.el.details(
                    rx.el.summary(
                        "Edit totals",
                        class_name="cursor-pointer rounded-md px-2 py-2 text-xs font-semibold text-[#17324F] hover:bg-[#F0F5FA]",
                    ),
                    rx.el.form(
                        field(
                            "Food name",
                            "name",
                            row["name"],
                            required=True,
                            max_length=100,
                        ),
                        field(
                            "Prepared total",
                            "prepared",
                            row["prepared"],
                            "number",
                            min=0,
                            max=100000,
                            step=1,
                            required=True,
                        ),
                        field(
                            "Sold total",
                            "sold",
                            row["sold"],
                            "number",
                            min=0,
                            max=100000,
                            step=1,
                            required=True,
                        ),
                        rx.el.button(
                            "Save totals", type="submit", class_name=BUTTON
                        ),
                        on_submit=lambda data: CanteenState.save_operation(
                            row["id"], data
                        ),
                        key=CanteenState.inventory_revision,
                        class_name="mt-2 flex min-w-[220px] flex-col gap-3 rounded-lg border border-gray-200 bg-white p-3",
                    ),
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-3.5 w-3.5"),
                    aria_label=f"Remove empty record {row['name']}",
                    on_click=lambda: CanteenState.remove_operation(row["id"]),
                    disabled=row["prepared"] > 0,
                    class_name=OUTLINE,
                ),
                class_name="flex flex-wrap items-start gap-2",
            ),
            class_name=CELL,
        ),
        key=row["id"],
        class_name="border-b border-gray-100 last:border-0 even:bg-[#F8FAFC] hover:bg-[#F0F5FA]",
    )


def inventory() -> rx.Component:
    return rx.el.div(
        rx.el.section(
            title_block(
                "Inventory, preparation & sales",
                "Whole portions only. Remaining = prepared − sold − collected. Unallocated = remaining − listed surplus. Quick sales cannot consume allocated surplus.",
                "cooking-pot",
            ),
            rx.cond(
                CanteenState.rows.length() > 0,
                rx.el.div(
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    table_header("Food", "utensils"),
                                    table_header("Prepared", "cooking-pot"),
                                    table_header("Sold", "receipt-text"),
                                    table_header("Collected", "hand-heart"),
                                    table_header("Remaining", "package"),
                                    table_header("Free", "package-open"),
                                    table_header("Actions", "square-pen"),
                                ),
                                class_name="bg-[#F4F7FA]",
                            ),
                            rx.el.tbody(
                                rx.foreach(CanteenState.rows, inventory_row)
                            ),
                            class_name="table-auto w-full min-w-[960px]",
                        ),
                        class_name="overflow-x-auto",
                    ),
                    class_name="overflow-hidden rounded-lg border border-gray-200",
                ),
                empty("Inventory is empty. Add your first sample food below."),
            ),
            rx.el.p(
                "To remove a record, first set all its quantities to zero. Collected sample history is retained. No prices or financial transactions are recorded.",
                class_name="mt-3 text-[11px] leading-5 text-gray-500",
            ),
            class_name=CARD,
        ),
        rx.el.section(
            title_block(
                "Add food to the demo",
                "A new record starts with no surplus allocation or simulated collection.",
                "plus",
            ),
            rx.el.form(
                field(
                    "Food name",
                    "name",
                    required=True,
                    max_length=100,
                    placeholder="e.g. Vegetable wraps",
                ),
                field(
                    "Canteen / location",
                    "location",
                    required=True,
                    max_length=100,
                    placeholder="e.g. Main campus canteen",
                ),
                field(
                    "Allergen notes",
                    "allergens",
                    required=True,
                    max_length=100,
                    placeholder="e.g. Wheat, or Unknown",
                ),
                field(
                    "Prepared portions",
                    "prepared",
                    0,
                    "number",
                    min=0,
                    max=100000,
                    step=1,
                    required=True,
                ),
                field(
                    "Sold portions",
                    "sold",
                    0,
                    "number",
                    min=0,
                    max=100000,
                    step=1,
                    required=True,
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("plus", class_name="h-4 w-4"),
                        "Add local food",
                        type="submit",
                        class_name=BUTTON,
                    ),
                    class_name="flex items-end",
                ),
                on_submit=CanteenState.add_operation,
                class_name="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3",
            ),
            class_name=CARD,
        ),
        class_name="flex w-full flex-col gap-4",
    )


def surplus_card(row: OperationView) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    row["name"],
                    class_name="text-sm font-semibold text-[#17324F]",
                ),
                rx.el.p(
                    row["location"], class_name="mt-1 text-xs text-gray-500"
                ),
            ),
            rx.el.span(
                row["status"],
                class_name=rx.cond(
                    row["status"] == "Available",
                    "h-fit w-fit rounded-md bg-green-100 px-2 py-1 text-[10px] font-semibold text-green-600",
                    "h-fit w-fit rounded-md bg-[#EAF1F7] px-2 py-1 text-[10px] font-semibold text-[#17324F]",
                ),
            ),
            class_name="flex items-start justify-between gap-3",
        ),
        rx.el.p(
            f"{row['remaining']} remaining · {row['listed']} allocated · {row['collected']} simulated collected",
            class_name="mt-4 text-xs font-medium text-[#17324F]",
        ),
        rx.el.p(
            f"{row['eligibility']} · Approved fictional partners only",
            class_name="mt-2 text-[11px] text-gray-500",
        ),
        rx.el.p(
            f"Listed allergens: {row['allergens']} · must be confirmed by a real provider",
            class_name="mt-1 text-[11px] leading-5 text-gray-500",
        ),
        rx.el.form(
            field(
                "Allocated portions",
                "listed",
                row["listed"],
                "number",
                min=0,
                max=row["remaining"],
                step=1,
                required=True,
            ),
            select_field(
                "Demo listing status",
                "status",
                ["Draft", "Available", "Paused"],
                row["status"],
            ),
            field(
                "Pickup starts", "start", row["start"], "time", required=True
            ),
            field("Pickup ends", "end", row["end"], "time", required=True),
            rx.el.label(
                rx.el.span(
                    "Handling / storage notes",
                    class_name="mb-1.5 block text-xs font-medium text-gray-600",
                ),
                rx.el.textarea(
                    name="handling",
                    default_value=row["handling"],
                    key=row["handling"],
                    max_length=500,
                    placeholder="Record illustrative storage, packaging and handling details",
                    rows=3,
                    class_name=INPUT,
                ),
                class_name="col-span-full",
            ),
            rx.el.label(
                rx.el.input(
                    type="checkbox",
                    name="reviewed",
                    default_checked=row["reviewed"],
                    key=row["reviewed"],
                    class_name="mt-0.5 h-4 w-4 shrink-0 accent-[#17324F]",
                ),
                rx.el.span(
                    "Simulated review: handling, allergen notes and pickup window checked for this demo only. Not food safety certification.",
                    class_name="text-[11px] leading-5 text-gray-600",
                ),
                class_name="col-span-full flex items-start gap-2",
            ),
            rx.el.div(
                rx.el.button(
                    "Save local listing", type="submit", class_name=BUTTON
                ),
                rx.el.button(
                    "Simulate collection",
                    type="button",
                    disabled=(row["status"] != "Available")
                    | (~row["reviewed"])
                    | (row["listed"] <= 0),
                    on_click=lambda: CanteenState.simulate_collection(
                        row["id"]
                    ),
                    class_name=OUTLINE,
                ),
                class_name="col-span-full flex flex-wrap gap-2",
            ),
            on_submit=lambda data: CanteenState.save_surplus(row["id"], data),
            key=CanteenState.inventory_revision,
            class_name="mt-4 grid grid-cols-2 gap-3",
        ),
        rx.el.p(
            "Campus-local times on an illustrative day. Collection moves all allocated portions to the collected total, locally only.",
            class_name="mt-3 text-[10px] leading-5 text-gray-500",
        ),
        key=row["id"],
        class_name=CARD,
    )


def surplus() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            title_block(
                "Surplus management",
                "Draft → reviewed demo availability → simulated collection. Draft and paused portions remain allocated, but are not counted as available.",
                "leaf",
            ),
            rx.el.p(
                "Local demo listings and requests only; no live listings, real safety checks or verified real-world recipients. A real provider must assess temperature, storage, allergens and suitability before any food is shared.",
                class_name="rounded-lg border border-yellow-200 bg-yellow-50 px-4 py-3 text-xs leading-6 text-yellow-800",
            ),
            class_name=CARD,
        ),
        rx.cond(
            CanteenState.rows.length() > 0,
            rx.el.div(
                rx.foreach(CanteenState.rows, surplus_card),
                class_name="grid grid-cols-1 gap-4 xl:grid-cols-2",
            ),
            empty(
                "No food records for surplus. Add a food record in Inventory."
            ),
        ),
        class_name="flex w-full flex-col gap-4",
    )


def break_row(row: BreakSlot) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.p(row["branch"], class_name="font-semibold text-[#17324F]"),
            rx.el.p(row["year"], class_name="mt-1 text-[10px] text-gray-500"),
            class_name=CELL,
        ),
        rx.el.td(row["enrolled"], class_name=CELL),
        rx.el.td(
            rx.el.p(
                f"{row['expected']} on-campus · {row['visitors']} visitors · {row['meals']} meal demand"
            ),
            rx.el.p(
                rx.cond(row["active"], "Active schedule", "Inactive schedule"),
                class_name="mt-1 text-xs text-gray-500",
            ),
            class_name=CELL,
        ),
        rx.el.td(
            rx.el.form(
                field(
                    "Attendance %",
                    "attendance",
                    row["attendance"],
                    "number",
                    min=0,
                    max=100,
                    step=1,
                    required=True,
                ),
                field(
                    "Break start", "start", row["start"], "time", required=True
                ),
                field("Break end", "end", row["end"], "time", required=True),
                rx.el.div(
                    rx.el.button(
                        "Update assumption", type="submit", class_name=OUTLINE
                    ),
                    class_name="flex items-end",
                ),
                on_submit=lambda data: CanteenState.save_break(row["id"], data),
                key=CanteenState.planning_revision,
                class_name="grid min-w-[560px] grid-cols-4 gap-3",
            ),
            class_name=CELL,
        ),
        key=row["id"],
        class_name="border-b border-gray-100 last:border-0 even:bg-[#F8FAFC]",
    )


def break_planning() -> rx.Component:
    return rx.el.section(
        title_block(
            "Branch-wise break planning",
            "28 branch/year aggregates shared with admin. FY starts at 1000 total, SY at 800 total; TY/BE unknown (0). Campus = enrollment × attendance %. Visitors = campus × visitor %. Meal demand = visitors × meal %. Each stage rounded. Edit enrollment and purchase assumptions in Admin Students; changing canteen attendance does not change enrolled totals.",
            "calendar-clock",
        ),
        rx.el.div(
            rx.el.div(
                rx.foreach(
                    CanteenState.branches,
                    lambda branch: rx.el.button(
                        branch,
                        on_click=lambda: CanteenState.select_branch(branch),
                        class_name=rx.cond(
                            CanteenState.branch == branch, BUTTON, OUTLINE
                        ),
                    ),
                ),
                class_name="flex flex-wrap gap-2",
            ),
            rx.el.p(
                f"{CanteenState.expected_attendance} expected students in this view",
                class_name="text-xs font-semibold text-[#17324F]",
            ),
            class_name="mb-5 flex flex-col justify-between gap-4 xl:flex-row xl:items-center",
        ),
        rx.cond(
            CanteenState.visible_breaks.length() > 0,
            rx.el.div(
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                table_header("Branch / year", "graduation-cap"),
                                table_header("Enrolled", "users"),
                                table_header("Expected", "user-check"),
                                table_header(
                                    "Edit local slot", "calendar-clock"
                                ),
                            ),
                            class_name="bg-[#F4F7FA]",
                        ),
                        rx.el.tbody(
                            rx.foreach(CanteenState.visible_breaks, break_row)
                        ),
                        class_name="table-auto w-full min-w-[900px]",
                    ),
                    class_name="overflow-x-auto",
                ),
                class_name="overflow-hidden rounded-lg border border-gray-200",
            ),
            empty("No break slots match this branch. Choose All branches."),
        ),
        targeted_list(),
        rx.el.p(
            "Demo schedule only; overlapping slots are allowed across branches. Student attendance is not a forecast of purchases, and editing it does not manufacture food inventory.",
            class_name="mt-4 text-xs leading-6 text-gray-500",
        ),
        class_name=CARD,
    )


def notice_card(notice: Notice) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.h3(
                notice["title"],
                class_name="text-xs font-semibold text-[#17324F]",
            ),
            rx.el.span(
                rx.cond(notice["read"], "Read", "New"),
                class_name="w-fit rounded-md bg-[#EAF1F7] px-2 py-1 text-[10px] text-[#17324F]",
            ),
            class_name="flex justify-between gap-3",
        ),
        rx.el.p(
            notice["text"], class_name="mt-2 text-xs leading-6 text-gray-600"
        ),
        key=notice["id"],
        class_name="rounded-lg border border-gray-200 bg-white p-4",
    )


def announcement_form(notice: Notice) -> rx.Component:
    return rx.el.article(
        rx.el.form(
            field(
                "Announcement title",
                "title",
                notice["title"],
                required=True,
                max_length=80,
            ),
            select_field(
                "Intended demo audience",
                "audience",
                ["Canteen team", "Collection partners", "All demo roles"],
                notice["audience"],
            ),
            rx.el.label(
                rx.el.span(
                    "Announcement text",
                    class_name="mb-1.5 block text-xs font-medium text-gray-600",
                ),
                rx.el.textarea(
                    name="text",
                    default_value=notice["text"],
                    key=notice["text"],
                    required=True,
                    max_length=500,
                    rows=3,
                    class_name=INPUT,
                ),
                class_name="sm:col-span-2",
            ),
            rx.el.div(
                rx.el.button(
                    rx.cond(
                        notice["id"] == "",
                        "Save local announcement",
                        "Save edits",
                    ),
                    type="submit",
                    class_name=BUTTON,
                ),
                rx.cond(
                    notice["id"] != "",
                    rx.el.button(
                        "Remove",
                        type="button",
                        on_click=lambda: CanteenState.remove_announcement(
                            notice["id"]
                        ),
                        class_name=OUTLINE,
                    ),
                ),
                class_name="flex gap-2 sm:col-span-2",
            ),
            on_submit=lambda data: CanteenState.save_announcement(
                notice["id"], data
            ),
            class_name="grid grid-cols-1 gap-3 sm:grid-cols-2",
        ),
        key=notice["id"],
        class_name="rounded-lg border border-gray-200 bg-white p-4",
    )


def notifications() -> rx.Component:
    return rx.el.div(
        rx.el.section(
            title_block(
                "Local activity notifications",
                "Generated by demo inventory and surplus actions. Nothing is emailed, pushed or delivered to another user.",
                "bell",
            ),
            rx.el.div(
                rx.el.button(
                    rx.cond(
                        CanteenState.alerts_enabled,
                        "Pause local alerts",
                        "Enable local alerts",
                    ),
                    on_click=CanteenState.toggle_alerts,
                    class_name=BUTTON,
                ),
                rx.el.button(
                    "Mark all read",
                    on_click=CanteenState.mark_read,
                    class_name=OUTLINE,
                ),
                rx.el.button(
                    "Clear activity",
                    on_click=CanteenState.clear_notices,
                    class_name=OUTLINE,
                ),
                class_name="mb-4 flex flex-wrap gap-2",
            ),
            rx.cond(
                CanteenState.notices.length() > 0,
                rx.el.div(
                    rx.foreach(CanteenState.notices, notice_card),
                    class_name="flex max-h-[420px] flex-col gap-3 overflow-y-auto",
                ),
                empty(
                    "No local notifications. Inventory or surplus actions will appear here while alerts are enabled."
                ),
            ),
            class_name=CARD,
        ),
        rx.el.section(
            targeted_list(),
            title_block(
                "Announcement editor",
                "Create and edit session-local announcements. Audience labels are illustrative, not a delivery list.",
                "megaphone",
            ),
            announcement_form(
                {
                    "id": "",
                    "title": "",
                    "text": "",
                    "audience": "Canteen team",
                    "read": False,
                }
            ),
            rx.el.h3(
                "Saved local announcements",
                class_name="mb-3 mt-6 text-sm font-semibold text-[#17324F]",
            ),
            rx.cond(
                CanteenState.announcements.length() > 0,
                rx.el.div(
                    rx.foreach(CanteenState.announcements, announcement_form),
                    class_name="flex flex-col gap-3",
                ),
                empty("No announcements yet. Save a local announcement above."),
            ),
            class_name=CARD,
        ),
        class_name="grid grid-cols-1 items-start gap-4 xl:grid-cols-2",
    )


def message_bubble(message: ConversationMessage) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                rx.cond(
                    message["side"] == "canteen",
                    "Canteen · local demo only, resets on reload",
                    rx.cond(
                        message["side"] == "ngo",
                        "NGO · local demo only, resets on reload",
                        "Partner · scripted example",
                    ),
                ),
                class_name=rx.cond(
                    message["side"] == "canteen",
                    "mb-2 text-[10px] font-semibold text-white/70",
                    "mb-2 text-[10px] font-semibold text-[#17324F]/60",
                ),
            ),
            rx.el.p(
                message["text"],
                class_name="whitespace-pre-wrap break-words text-xs leading-6",
            ),
            class_name=rx.cond(
                message["side"] == "canteen",
                "max-w-[85%] rounded-xl rounded-br-xs bg-[#17324F] px-4 py-3 text-white",
                "max-w-[85%] rounded-xl rounded-bl-xs border border-gray-200 bg-white px-4 py-3 text-gray-700",
            ),
        ),
        key=message["id"],
        class_name=rx.cond(
            message["side"] == "canteen",
            "flex w-full justify-end",
            "flex w-full justify-start",
        ),
    )


def messages() -> rx.Component:
    return rx.el.section(
        title_block(
            "Collection partner conversations",
            "Local demo only, resets on reload. This thread is shared with the NGO workspace in this browser session, with explicitly scripted replies. No real message, request or booking is delivered.",
            "messages-square",
        ),
        rx.el.div(
            rx.el.aside(
                rx.el.p(
                    "APPROVED DEMO EXAMPLES",
                    class_name="mb-3 text-[10px] font-semibold tracking-wider text-gray-500",
                ),
                rx.foreach(
                    CanteenState.partners,
                    lambda partner: rx.el.button(
                        rx.icon("building-2", class_name="h-4 w-4 shrink-0"),
                        partner,
                        on_click=lambda: CanteenState.select_partner(partner),
                        class_name=rx.cond(
                            CanteenState.partner == partner,
                            "flex items-center gap-2 rounded-lg bg-[#17324F] p-3 text-left text-xs font-medium text-white",
                            "flex items-center gap-2 rounded-lg border border-gray-200 bg-white p-3 text-left text-xs font-medium text-gray-600 hover:bg-[#F0F5FA]",
                        ),
                    ),
                ),
                rx.el.p(
                    "Fictional organizations from the central demo directory. Approval is illustrative, not real-world verification.",
                    class_name="mt-3 text-[11px] leading-5 text-gray-500",
                ),
                class_name="flex flex-col gap-2 rounded-xl bg-[#F0F5FA] p-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            CanteenState.partner,
                            class_name="text-sm font-semibold text-[#17324F]",
                        ),
                        rx.el.p(
                            "Simulation only · no delivery status",
                            class_name="mt-1 text-[10px] text-gray-500",
                        ),
                    ),
                    rx.el.button(
                        "Clear local chat",
                        on_click=CanteenState.clear_conversation,
                        class_name=OUTLINE,
                    ),
                    class_name="flex flex-wrap items-center justify-between gap-3 border-b border-gray-200 bg-white p-4",
                ),
                rx.el.div(
                    rx.cond(
                        CanteenState.conversation.length() > 0,
                        rx.foreach(CanteenState.conversation, message_bubble),
                        empty(
                            "No messages in this local thread. Write a message to see a scripted reply."
                        ),
                    ),
                    aria_live="polite",
                    role="log",
                    class_name="flex h-[360px] flex-col gap-4 overflow-y-auto bg-[#F5F8FB] p-4",
                ),
                rx.el.form(
                    rx.el.label(
                        rx.el.span(
                            "Your demo message",
                            class_name="mb-2 block text-xs font-medium text-gray-600",
                        ),
                        rx.el.textarea(
                            name="message",
                            placeholder="Ask about sample portions or pickup windows…",
                            rows=2,
                            required=True,
                            max_length=500,
                            class_name=INPUT,
                        ),
                        class_name="block flex-1",
                    ),
                    rx.el.button(
                        rx.icon("send", class_name="h-4 w-4"),
                        "Add locally",
                        type="submit",
                        class_name=BUTTON,
                    ),
                    on_submit=CanteenState.compose_message,
                    reset_on_submit=True,
                    class_name="flex flex-col items-stretch gap-3 border-t border-gray-200 bg-white p-4 sm:flex-row sm:items-end",
                ),
                class_name="min-w-0 overflow-hidden rounded-xl border border-gray-200",
            ),
            class_name="grid grid-cols-1 gap-4 xl:grid-cols-[240px_minmax(0,1fr)]",
        ),
        class_name=CARD,
    )


def canteen_workspace() -> rx.Component:
    return rx.el.div(
        rx.el.a(
            "Skip to workspace",
            href="#canteen-main",
            class_name="sr-only bg-white p-3 text-[#17324F] focus:not-sr-only focus:fixed focus:left-3 focus:top-3 focus:z-50",
        ),
        rx.el.header(
            rx.el.div(
                brand(),
                workspace_routes(),
                rx.el.span(
                    rx.icon("database", class_name="h-3.5 w-3.5"),
                    "Demo Data",
                    class_name="hidden w-fit items-center gap-2 rounded-full border border-[#2E6B52]/20 bg-[#DCEBDC]/40 px-3 py-1.5 text-[11px] font-semibold text-[#2E6B52] sm:flex",
                ),
                class_name="flex flex-wrap items-center justify-between gap-3 px-4 py-3 sm:px-6",
            ),
            class_name="shrink-0 border-b border-gray-200 bg-white",
        ),
        rx.el.div(
            sidebar(),
            rx.el.main(
                rx.el.nav(
                    rx.foreach(CanteenState.tabs, tab_button),
                    aria_label="Mobile canteen sections",
                    class_name="mb-5 flex gap-2 overflow-x-auto pb-2 lg:hidden",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "CANTEEN / LOCAL DEMO",
                            class_name="text-[10px] font-semibold tracking-[0.16em] text-[#2E6B52]",
                        ),
                        rx.el.h1(
                            CanteenState.tab,
                            class_name="mt-2 font-['DM_Sans'] text-3xl font-semibold tracking-tight text-[#17324F]",
                        ),
                        rx.el.p(
                            "Plan thoughtfully. Track every portion.",
                            class_name="mt-2 text-xs text-gray-500",
                        ),
                    ),
                    rx.el.span(
                        "All campus locations · sample day",
                        class_name="w-fit rounded-lg border border-gray-200 bg-white px-3 py-2 text-[11px] text-gray-500",
                    ),
                    class_name="mb-5 flex flex-wrap items-center justify-between gap-4",
                ),
                rx.el.div(
                    rx.icon(
                        "info", class_name="h-4 w-4 shrink-0 text-[#17324F]"
                    ),
                    rx.el.p(
                        "Demo Data only. Edits are session-local and may reset; no persistence, authentication, live availability, verified food safety or external delivery.",
                        class_name="text-[11px] leading-5 text-gray-600",
                    ),
                    class_name="mb-5 flex items-start gap-2 rounded-lg border border-[#CEDCE9] bg-[#EAF1F7] px-4 py-3",
                ),
                rx.cond(
                    CanteenState.feedback != "",
                    rx.el.div(
                        rx.icon("info", class_name="h-4 w-4 shrink-0"),
                        rx.el.p(CanteenState.feedback),
                        role="status",
                        aria_live="polite",
                        class_name=rx.cond(
                            CanteenState.error,
                            "mb-4 flex items-start gap-2 rounded-lg border border-red-200 bg-red-50 p-3 text-xs leading-5 text-red-600",
                            "mb-4 flex items-start gap-2 rounded-lg border border-green-200 bg-green-50 p-3 text-xs leading-5 text-green-700",
                        ),
                    ),
                ),
                rx.match(
                    CanteenState.tab,
                    ("Overview", overview()),
                    ("Inventory", inventory()),
                    ("Surplus", surplus()),
                    ("Break planning", break_planning()),
                    ("Notifications", notifications()),
                    ("Messages", messages()),
                    ("Requests", canteen_requests()),
                    overview(),
                ),
                rx.el.p(
                    "Canteenio · local canteen demo · sample records, not real-world outcomes",
                    class_name="mt-6 text-center text-[10px] text-gray-400",
                ),
                id="canteen-main",
                class_name="min-w-0 w-full flex-1 overflow-y-auto bg-[#F4F7FA] p-4 sm:p-6 xl:p-8",
            ),
            class_name="flex min-h-0 flex-1",
        ),
        class_name="flex h-dvh w-full flex-col overflow-hidden bg-white font-['Inter'] text-gray-700 antialiased",
    )
