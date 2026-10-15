import reflex as rx
from app.components.shared import brand
from app.components.collection_requests import request_card, BUTTON, OUTLINE
from app.states.canteen_state import (
    CanteenState,
    Operation,
    ConversationMessage,
)
from app.states.demo_records import OrganizationRecord

CARD = "w-full min-w-0 rounded-xl border border-[#E8DADC] bg-white p-5"
INPUT = "w-full min-w-0 rounded-lg border border-[#DCCDCF] bg-white px-3 py-2 text-sm text-gray-800 focus-visible:outline-2 focus-visible:outline-[#2E6B52]"


def heading(title: str, description: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5 text-[#2E6B52]"),
            rx.el.h2(
                title,
                class_name="font-['DM_Sans'] text-lg font-semibold text-[#192D26]",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(description, class_name="mt-2 text-xs leading-6 text-gray-500"),
        class_name="mb-4",
    )


def empty(title: str, text: str) -> rx.Component:
    return rx.el.div(
        rx.icon("inbox", class_name="mb-3 h-6 w-6 text-[#2E6B52]"),
        rx.el.h3(title, class_name="text-sm font-semibold text-[#192D26]"),
        rx.el.p(text, class_name="mt-2 text-xs leading-6 text-gray-500"),
        class_name="rounded-xl border border-dashed border-[#DCCDCF] bg-[#FCF7F8] p-6",
    )


def approval(approved: bool) -> rx.Component:
    return rx.cond(
        approved,
        rx.el.span(
            rx.icon("shield-check", class_name="h-3.5 w-3.5 shrink-0"),
            "Verified · demo approval",
            class_name="inline-flex w-fit items-center gap-1.5 rounded-lg border border-[#B58B36]/30 bg-[#FCF5E5] px-2 py-1 text-[10px] font-semibold text-[#946D21]",
        ),
        rx.el.span(
            "Pending · not approved",
            class_name="inline-flex w-fit rounded-lg bg-gray-100 px-2 py-1 text-[10px] font-medium text-gray-600",
        ),
    )


def section_button(tab: str) -> rx.Component:
    return rx.el.button(
        rx.match(
            tab,
            ("Directory", rx.icon("building-2", class_name="h-4 w-4 shrink-0")),
            ("Available food", rx.icon("leaf", class_name="h-4 w-4 shrink-0")),
            (
                "My requests",
                rx.icon("clipboard-list", class_name="h-4 w-4 shrink-0"),
            ),
            (
                "Collection history",
                rx.icon("history", class_name="h-4 w-4 shrink-0"),
            ),
            rx.icon("messages-square", class_name="h-4 w-4 shrink-0"),
        ),
        tab,
        on_click=lambda: CanteenState.select_ngo_tab(tab),
        aria_current=rx.cond(CanteenState.ngo_tab == tab, "page", "false"),
        class_name=rx.cond(
            CanteenState.ngo_tab == tab,
            "flex shrink-0 items-center gap-3 whitespace-nowrap rounded-lg bg-[#F4E4E5] px-3 py-3 text-xs font-semibold text-[#192D26] focus-visible:outline-2 focus-visible:outline-[#2E6B52]",
            "flex shrink-0 items-center gap-3 whitespace-nowrap rounded-lg bg-white px-3 py-3 text-xs font-medium text-gray-600 hover:bg-[#FCF7F8] focus-visible:outline-2 focus-visible:outline-[#2E6B52]",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.p(
                "COMMUNITY CONNECTIONS",
                class_name="text-[10px] font-semibold tracking-widest text-[#2E6B52]",
            ),
            rx.el.p(
                "NGO workspace",
                class_name="mt-2 text-sm font-semibold text-[#192D26]",
            ),
            rx.el.p(
                "15 fictional organizations",
                class_name="mt-1 text-xs text-gray-500",
            ),
            class_name="shrink-0 border-b border-[#E8DADC] p-5",
        ),
        rx.el.nav(
            rx.foreach(CanteenState.ngo_tabs, section_button),
            aria_label="NGO sections",
            class_name="flex min-h-0 flex-1 flex-col gap-1 overflow-y-auto p-3",
        ),
        rx.el.div(
            rx.icon("sprout", class_name="mb-3 h-5 w-5 text-[#2E6B52]"),
            rx.el.p(
                "Good food. Shared thoughtfully.",
                class_name="text-xs font-semibold text-[#192D26]",
            ),
            rx.el.p(
                "This browser session is the whole demo. No real NGO is connected, no data is shared between users, and nothing is delivered.",
                class_name="mt-2 text-[11px] leading-5 text-gray-500",
            ),
            class_name="m-3 rounded-xl border border-[#2E6B52]/15 bg-[#DCEBDC]/30 p-4",
        ),
        class_name="hidden h-full w-56 shrink-0 flex-col border-r border-[#E8DADC] bg-white lg:flex",
    )


def organization_card(row: OrganizationRecord) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.icon("building-2", class_name="h-5 w-5 text-[#2E6B52]"),
            approval(row["approved"]),
            class_name="flex items-start justify-between gap-2",
        ),
        rx.el.h3(
            row["name"],
            class_name="mt-3 text-sm font-semibold leading-5 text-[#192D26]",
        ),
        rx.el.p(
            f"{row['id']} · {row['city']}",
            class_name="mt-2 text-[11px] text-gray-500",
        ),
        rx.el.p(
            row["mission"], class_name="mt-3 text-xs leading-6 text-gray-600"
        ),
        rx.el.button(
            rx.cond(
                CanteenState.organization_id == row["id"],
                "Selected demo profile",
                "Select / view profile",
            ),
            on_click=lambda: CanteenState.select_organization(row["id"]),
            aria_pressed=CanteenState.organization_id == row["id"],
            class_name=OUTLINE,
        ),
        key=row["id"],
        class_name=rx.cond(
            CanteenState.organization_id == row["id"],
            "flex min-w-0 flex-col items-start gap-2 rounded-xl border border-[#2E6B52] bg-[#FCF7F8] p-4",
            "flex min-w-0 flex-col items-start gap-2 rounded-xl border border-[#E8DADC] bg-white p-4",
        ),
    )


def profile() -> rx.Component:
    return rx.el.section(
        heading(
            "Selected fictional profile",
            "Selection acts as this NGO inside the local demo; this is not authentication.",
            "contact",
        ),
        approval(CanteenState.selected_organization["approved"]),
        rx.el.h3(
            CanteenState.selected_organization["name"],
            class_name="mt-3 text-base font-semibold text-[#192D26]",
        ),
        rx.el.p(
            f"{CanteenState.selected_organization['id']} · {CanteenState.selected_organization['city']}",
            class_name="mt-2 text-xs text-gray-500",
        ),
        rx.el.p(
            CanteenState.selected_organization["mission"],
            class_name="mt-3 text-xs leading-6 text-gray-600",
        ),
        rx.el.div(
            rx.el.p(
                "ILLUSTRATIVE CONTACT · DO NOT CONTACT",
                class_name="text-[10px] font-semibold tracking-wide text-gray-500",
            ),
            rx.el.p(
                CanteenState.selected_organization["contact"],
                class_name="mt-2 text-xs text-gray-700",
            ),
            rx.el.p(
                CanteenState.selected_organization["email"],
                class_name="mt-2 break-all text-xs text-gray-600",
            ),
            rx.el.p(
                CanteenState.selected_organization["contact_notes"],
                class_name="mt-2 text-xs leading-6 text-gray-500",
            ),
            class_name="mt-4 rounded-lg bg-[#FCF7F8] p-3",
        ),
        rx.cond(
            CanteenState.selected_organization["approved"],
            rx.el.button(
                "Explore reviewed surplus",
                on_click=lambda: CanteenState.select_ngo_tab("Available food"),
                class_name=BUTTON,
            ),
            rx.el.p(
                "Pending profiles can browse but cannot request food or compose messages. Approval is a fictional flag, not real-world verification.",
                class_name="text-xs leading-6 text-gray-500",
            ),
        ),
        class_name="flex w-full min-w-0 flex-col items-start gap-3 rounded-xl border border-[#E8DADC] bg-white p-5",
    )


def directory() -> rx.Component:
    return rx.el.div(
        rx.el.section(
            heading(
                "Fictional NGO directory",
                "15 distinct examples, with approved and pending profiles. Only approved examples display the golden shield; no real verification is claimed.",
                "building-2",
            ),
            rx.el.label(
                rx.el.span(
                    "Search name, ID, city or mission",
                    class_name="mb-2 block text-xs font-medium text-gray-600",
                ),
                rx.el.input(
                    placeholder="Find a fictional organization…",
                    default_value=CanteenState.directory_query,
                    on_change=CanteenState.search_directory.debounce(500),
                    class_name=INPUT,
                ),
                class_name="mb-3 block",
            ),
            rx.el.div(
                rx.foreach(
                    ["All", "Approved", "Pending"],
                    lambda value: rx.el.button(
                        value,
                        on_click=lambda: CanteenState.filter_directory(value),
                        aria_pressed=CanteenState.directory_filter == value,
                        class_name=rx.cond(
                            CanteenState.directory_filter == value,
                            BUTTON,
                            OUTLINE,
                        ),
                    ),
                ),
                class_name="mb-4 flex flex-wrap gap-2",
            ),
            rx.el.p(
                f"{CanteenState.directory.length()} matching profiles",
                aria_live="polite",
                class_name="mb-3 text-xs text-gray-500",
            ),
            rx.cond(
                CanteenState.directory.length() > 0,
                rx.el.div(
                    rx.foreach(CanteenState.directory, organization_card),
                    class_name="grid grid-cols-1 gap-3 md:grid-cols-2",
                ),
                empty(
                    "No matching profiles",
                    "Try a shorter search or switch to All to include both approved and pending examples.",
                ),
            ),
            class_name=CARD,
        ),
        profile(),
        class_name="grid w-full grid-cols-1 items-start gap-4 xl:grid-cols-[minmax(0,2fr)_minmax(280px,1fr)]",
    )


def surplus_card(row: Operation) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.h3(
                row["name"], class_name="text-sm font-semibold text-[#192D26]"
            ),
            rx.el.span(
                "Reviewed · demo only",
                class_name="w-fit rounded-lg bg-green-100 px-2 py-1 text-[10px] text-green-600",
            ),
            class_name="flex flex-wrap items-start justify-between gap-2",
        ),
        rx.el.p(row["location"], class_name="mt-2 text-xs text-gray-500"),
        rx.el.p(
            f"{row['listed']} unreserved portions · {row['start']}–{row['end']}",
            class_name="mt-3 text-sm font-semibold text-[#2E6B52]",
        ),
        rx.el.p(
            f"Allergens: {row['allergens']}",
            class_name="mt-2 text-xs text-gray-600",
        ),
        rx.el.p(
            row["handling"], class_name="mt-2 text-xs leading-6 text-gray-500"
        ),
        rx.el.form(
            rx.el.label(
                rx.el.span(
                    "Requested portions",
                    class_name="mb-2 block text-xs font-medium text-gray-600",
                ),
                rx.el.input(
                    name="quantity",
                    type="number",
                    min=1,
                    max=row["listed"],
                    step=1,
                    default_value=1,
                    key=row["listed"],
                    required=True,
                    class_name=INPUT,
                ),
            ),
            rx.el.label(
                rx.el.span(
                    "Pickup / packaging notes",
                    class_name="mb-2 block text-xs font-medium text-gray-600",
                ),
                rx.el.textarea(
                    name="notes",
                    rows=2,
                    required=True,
                    max_length=500,
                    placeholder="Illustrative pickup plan, packaging or access needs…",
                    class_name=INPUT,
                ),
            ),
            rx.el.button(
                rx.icon("clipboard-plus", class_name="h-4 w-4"),
                "Request locally",
                type="submit",
                disabled=~CanteenState.selected_organization["approved"],
                class_name=BUTTON,
            ),
            on_submit=lambda data: CanteenState.create_request(row["id"], data),
            class_name="mt-4 flex flex-col gap-3",
        ),
        rx.el.p(
            "Local demo only, resets on reload. Sample campus-local window, not a dated pickup. Real food safety and suitability must be assessed by a provider.",
            class_name="mt-3 text-[10px] leading-5 text-gray-500",
        ),
        key=row["id"],
        class_name=CARD,
    )


def available_food() -> rx.Component:
    return rx.el.div(
        rx.el.section(
            heading(
                "Available reviewed surplus",
                "Drawn directly from the same canteen operations. Only Available + reviewed + positive unreserved portions appear. Pending requests reserve portions immediately; they do not record donations.",
                "leaf",
            ),
            rx.cond(
                ~CanteenState.selected_organization["approved"],
                rx.el.p(
                    "Your selected NGO is pending. Browse freely, but select an approved fictional profile in Directory before requesting.",
                    class_name="mb-3 rounded-lg bg-yellow-50 p-3 text-xs leading-6 text-yellow-800",
                ),
            ),
            rx.el.a(
                "Review / publish local surplus in Canteen →",
                href="/canteen",
                on_click=lambda: CanteenState.select_tab("Surplus"),
                class_name="text-xs font-semibold text-[#2E6B52] underline focus-visible:outline-2",
            ),
            class_name=CARD,
        ),
        rx.cond(
            CanteenState.available_surplus.length() > 0,
            rx.el.div(
                rx.foreach(CanteenState.available_surplus, surplus_card),
                class_name="grid w-full grid-cols-1 gap-4 xl:grid-cols-2",
            ),
            empty(
                "No unreserved reviewed surplus",
                "Sample food starts as drafts. Open Canteen → Surplus, add the simulated review and save as Available. If portions are all reserved, cancellation or rejection releases them.",
            ),
        ),
        class_name="flex w-full flex-col gap-4",
    )


def my_requests() -> rx.Component:
    return rx.el.section(
        heading(
            "My local requests",
            "Pending → canteen approves → you confirm the sample pickup plan → canteen records a simulated collection. Cancel anytime before collection; no actual pickup is arranged.",
            "clipboard-list",
        ),
        rx.el.a(
            "Open canteen Requests panel →",
            href="/canteen",
            on_click=lambda: CanteenState.select_tab("Requests"),
            class_name="mb-4 inline-block text-xs font-semibold text-[#2E6B52] underline focus-visible:outline-2",
        ),
        rx.cond(
            CanteenState.ngo_requests.length() > 0,
            rx.el.div(
                rx.foreach(CanteenState.ngo_requests, request_card),
                class_name="grid grid-cols-1 gap-3 xl:grid-cols-2",
            ),
            empty(
                "No requests for this profile",
                "Choose Available food to request reviewed surplus, or select another NGO in Directory to inspect its local requests.",
            ),
        ),
        class_name=CARD,
    )


def history() -> rx.Component:
    return rx.el.section(
        heading(
            "Locally completed collections",
            "Only requests completed via the local canteen workflow appear here. Seed collected inventory is excluded. These are simulated records, not real donations or deliveries.",
            "history",
        ),
        rx.cond(
            CanteenState.collection_history.length() > 0,
            rx.el.div(
                rx.foreach(CanteenState.collection_history, request_card),
                class_name="grid grid-cols-1 gap-3 xl:grid-cols-2",
            ),
            empty(
                "No locally completed requests",
                "Create a request, approve it in Canteen → Requests, confirm here, then mark collected in the canteen panel. Nothing is recorded as a real pickup.",
            ),
        ),
        class_name=CARD,
    )


def message_bubble(message: ConversationMessage) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            rx.match(
                message["side"],
                ("ngo", "NGO · local demo"),
                ("canteen", "Canteen · local demo"),
                "Partner · scripted example",
            ),
            class_name="mb-1 text-[10px] font-semibold text-[#2E6B52]",
        ),
        rx.el.p(
            message["text"],
            class_name="whitespace-pre-wrap break-words text-xs leading-6 text-gray-700",
        ),
        rx.el.p(
            "Local demo only, resets on reload",
            class_name="mt-2 text-[10px] text-gray-500",
        ),
        key=message["id"],
        class_name=rx.cond(
            message["side"] == "ngo",
            "ml-auto w-fit max-w-[90%] rounded-xl border border-[#E8DADC] bg-[#F4E4E5] p-3",
            "mr-auto w-fit max-w-[90%] rounded-xl border border-[#E8DADC] bg-white p-3",
        ),
    )


def messages() -> rx.Component:
    return rx.el.section(
        heading(
            "Local canteen conversation",
            "The selected NGO and canteen read the same session-local thread. Canteen may add a clearly scripted reply; no other user receives messages.",
            "messages-square",
        ),
        rx.el.a(
            "Open canteen Messages →",
            href="/canteen",
            on_click=[
                CanteenState.select_tab("Messages"),
                CanteenState.select_partner(
                    CanteenState.selected_organization["name"]
                ),
            ],
            class_name="mb-4 inline-block text-xs font-semibold text-[#2E6B52] underline focus-visible:outline-2",
        ),
        rx.el.div(
            rx.cond(
                CanteenState.ngo_conversation.length() > 0,
                rx.foreach(CanteenState.ngo_conversation, message_bubble),
                empty(
                    "No local messages",
                    "Compose a message as an approved fictional NGO. Switch to the same partner in canteen Messages to read or reply in this session.",
                ),
            ),
            role="log",
            aria_live="polite",
            aria_label="Local NGO conversation",
            class_name="flex h-80 shrink-0 flex-col gap-3 overflow-y-auto rounded-xl border border-[#E8DADC] bg-[#FCF7F8] p-4",
        ),
        rx.el.form(
            rx.el.label(
                rx.el.span(
                    "Your local message",
                    class_name="mb-2 block text-xs font-medium text-gray-600",
                ),
                rx.el.textarea(
                    name="message",
                    rows=2,
                    required=True,
                    max_length=500,
                    placeholder="Discuss the sample portions or collection plan…",
                    class_name=INPUT,
                ),
                class_name="block flex-1",
            ),
            rx.el.button(
                rx.icon("send", class_name="h-4 w-4"),
                "Add locally",
                disabled=~CanteenState.selected_organization["approved"],
                type="submit",
                class_name=BUTTON,
            ),
            on_submit=CanteenState.compose_ngo_message,
            reset_on_submit=True,
            class_name="mt-4 flex flex-col gap-3 sm:flex-row sm:items-end",
        ),
        rx.cond(
            ~CanteenState.selected_organization["approved"],
            rx.el.p(
                "Pending profile: choose an approved NGO in Directory to compose messages.",
                class_name="mt-3 text-xs text-gray-500",
            ),
        ),
        class_name=CARD,
    )


def metric(label: str, value: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(label, class_name="text-xs text-gray-500"),
            rx.icon(icon, class_name="h-4 w-4 text-[#2E6B52]"),
            class_name="flex items-center justify-between gap-2",
        ),
        rx.el.p(
            value,
            class_name="mt-2 font-['DM_Sans'] text-2xl font-semibold text-[#192D26]",
        ),
        class_name=CARD,
    )


def ngo_workspace() -> rx.Component:
    return rx.el.div(
        rx.el.a(
            "Skip to workspace",
            href="#ngo-main",
            class_name="sr-only bg-white p-3 text-[#2E6B52] focus:not-sr-only focus:fixed focus:left-3 focus:top-3 focus:z-50",
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
                    lambda route: rx.el.a(
                        route["label"],
                        href=route["href"],
                        aria_current=rx.cond(
                            route["label"] == "NGO", "page", "false"
                        ),
                        class_name=rx.cond(
                            route["label"] == "NGO",
                            "rounded-lg bg-[#F4E4E5] px-3 py-2 text-xs font-semibold text-[#192D26] focus-visible:outline-2 focus-visible:outline-[#2E6B52]",
                            "rounded-lg bg-white px-3 py-2 text-xs font-medium text-gray-600 hover:bg-[#FCF7F8] focus-visible:outline-2 focus-visible:outline-[#2E6B52]",
                        ),
                    ),
                ),
                aria_label="Demo workspaces",
                class_name="flex flex-wrap gap-1",
            ),
            rx.el.span(
                "Demo Data",
                class_name="hidden w-fit rounded-full border border-[#2E6B52]/20 bg-[#DCEBDC]/40 px-3 py-1.5 text-[11px] font-semibold text-[#2E6B52] sm:block",
            ),
            class_name="flex shrink-0 flex-wrap items-center justify-between gap-3 border-b border-[#E8DADC] bg-white px-4 py-3 sm:px-6",
        ),
        rx.el.div(
            sidebar(),
            rx.el.main(
                rx.el.nav(
                    rx.foreach(CanteenState.ngo_tabs, section_button),
                    aria_label="Mobile NGO sections",
                    class_name="mb-5 flex gap-2 overflow-x-auto pb-2 lg:hidden",
                ),
                rx.el.p(
                    "NGO / LOCAL DEMO",
                    class_name="text-[10px] font-semibold tracking-[0.16em] text-[#2E6B52]",
                ),
                rx.el.h1(
                    CanteenState.ngo_tab,
                    class_name="mt-2 font-['DM_Sans'] text-3xl font-semibold tracking-tight text-[#192D26]",
                ),
                rx.el.p(
                    "A thoughtful next chapter for surplus food.",
                    class_name="mb-5 mt-2 text-xs text-gray-500",
                ),
                rx.el.div(
                    rx.icon(
                        "info", class_name="h-4 w-4 shrink-0 text-[#2E6B52]"
                    ),
                    rx.el.p(
                        "Local demo only, resets on reload. Fictional profiles, simulated requests and messages; no live database, real safety certification, actual pickups, delivery or inter-user persistence.",
                        class_name="text-[11px] leading-5 text-gray-600",
                    ),
                    class_name="mb-4 flex items-start gap-2 rounded-lg border border-[#E8DADC] bg-white p-3",
                ),
                rx.el.div(
                    metric(
                        "Fictional profiles",
                        f"{CanteenState.organizations.length()}",
                        "building-2",
                    ),
                    metric(
                        "Approved examples",
                        f"{CanteenState.approved_organizations}",
                        "shield-check",
                    ),
                    metric(
                        "Unreserved portions",
                        f"{CanteenState.totals['available']}",
                        "leaf",
                    ),
                    metric(
                        "My local requests",
                        f"{CanteenState.ngo_requests.length()}",
                        "clipboard-list",
                    ),
                    class_name="mb-4 grid w-full grid-cols-2 gap-3 xl:grid-cols-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "ACTING AS · FICTIONAL PROFILE",
                            class_name="text-[10px] font-semibold tracking-wide text-gray-500",
                        ),
                        rx.el.p(
                            CanteenState.selected_organization["name"],
                            class_name="mt-1 text-xs font-semibold text-[#192D26]",
                        ),
                    ),
                    approval(CanteenState.selected_organization["approved"]),
                    rx.el.button(
                        "Change profile",
                        on_click=lambda: CanteenState.select_ngo_tab(
                            "Directory"
                        ),
                        class_name=OUTLINE,
                    ),
                    class_name="mb-4 flex flex-wrap items-center justify-between gap-3 rounded-xl border border-[#E8DADC] bg-white p-4",
                ),
                rx.cond(
                    CanteenState.feedback != "",
                    rx.el.div(
                        CanteenState.feedback,
                        role="status",
                        aria_live="polite",
                        class_name=rx.cond(
                            CanteenState.error,
                            "mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-xs leading-6 text-red-600",
                            "mb-4 rounded-lg border border-green-200 bg-green-50 p-3 text-xs leading-6 text-green-700",
                        ),
                    ),
                ),
                rx.match(
                    CanteenState.ngo_tab,
                    ("Directory", directory()),
                    ("Available food", available_food()),
                    ("My requests", my_requests()),
                    ("Collection history", history()),
                    ("Messages", messages()),
                    directory(),
                ),
                rx.el.p(
                    "Canteenio · fictional NGO demo · no real-world outcomes",
                    class_name="mt-6 text-center text-[10px] text-gray-500",
                ),
                id="ngo-main",
                class_name="w-full min-w-0 flex-1 overflow-y-auto bg-[#FCF7F8] p-4 sm:p-6 xl:p-8",
            ),
            class_name="flex min-h-0 flex-1",
        ),
        class_name="flex h-dvh w-full flex-col overflow-hidden bg-white font-['Inter'] text-gray-700 antialiased",
    )
