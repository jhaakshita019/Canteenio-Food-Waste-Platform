import reflex as rx
from app.components.shared import (
    PRIMARY_LINK,
    SECONDARY_LINK,
    SECTION,
    section_heading,
    workspace_links,
)
from app.components.assistant import assistant
from app.states.home_state import HomeState
from app.states.demo_records import FoodRecord, WORKFLOW, CAPABILITIES


def photo_credit() -> rx.Component:
    return rx.el.a(
        "Photo: Anna Pelzer / Unsplash ↗",
        href="https://unsplash.com/photos/IGfIGP5ONV0",
        target="_blank",
        rel="noopener noreferrer",
        class_name="rounded text-[10px] text-gray-500 underline decoration-gray-300 underline-offset-2 hover:text-[#2E6B52] focus-visible:outline-2 focus-visible:outline-[#2E6B52]",
    )


def hero() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    rx.icon("leaf", class_name="h-3.5 w-3.5"),
                    "A little less waste. A lot more possibility.",
                    class_name="mb-6 inline-flex w-fit items-center gap-2 rounded-full border border-[#2E6B52]/15 bg-[#DCEBDC]/45 px-3 py-1.5 text-[11px] font-medium text-[#2E6B52]",
                ),
                rx.el.h1(
                    "Good food deserves",
                    rx.el.br(),
                    rx.el.span("a second chance.", class_name="text-[#2E6B52]"),
                    class_name="font-['DM_Sans'] text-[43px] font-semibold leading-[1.1] tracking-[-2px] text-[#192D26] sm:text-[54px] lg:text-[62px]",
                ),
                rx.el.p(
                    "Smarter canteens. Stronger communities.",
                    class_name="mt-5 text-lg font-medium text-[#192D26]",
                ),
                rx.el.p(
                    "Canteenio connects campus canteens with NGOs to make food planning simpler and give surplus food a meaningful next stop. Because every portion matters.",
                    class_name="mt-3 max-w-lg text-sm leading-7 text-gray-500",
                ),
                rx.el.div(
                    rx.el.a(
                        "Explore Canteenio",
                        rx.icon("arrow-right", class_name="h-4 w-4"),
                        href="#how-it-works",
                        class_name=PRIMARY_LINK,
                    ),
                    rx.el.a(
                        "Login to Dashboard",
                        href="/login",
                        class_name=SECONDARY_LINK,
                    ),
                    class_name="mt-7 flex flex-wrap gap-3",
                ),
                rx.el.p(
                    rx.icon("info", class_name="h-3.5 w-3.5 shrink-0"),
                    "A public concept demo. Sample records, real possibilities.",
                    class_name="mt-4 flex items-center gap-2 text-[11px] text-gray-400",
                ),
                rx.el.figure(
                    rx.el.div(
                        rx.el.img(
                            src="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1000&q=85",
                            alt="Fresh vegetable salad in a bowl, photographed by Anna Pelzer",
                            class_name="h-[164px] w-full object-cover sm:h-[180px]",
                        ),
                        rx.el.div(
                            rx.icon(
                                "sprout", class_name="h-5 w-5 text-[#2E6B52]"
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Fresh thinking. Less waste.",
                                    class_name="text-sm font-semibold text-[#192D26]",
                                ),
                                rx.el.p(
                                    "From the canteen to the community",
                                    class_name="mt-0.5 text-[11px] text-gray-500",
                                ),
                            ),
                            class_name="absolute bottom-3 left-3 right-3 flex items-center gap-3 rounded-xl bg-white/95 px-4 py-3 backdrop-blur-sm",
                        ),
                        class_name="relative overflow-hidden rounded-2xl bg-[#DCEBDC]",
                    ),
                    rx.el.figcaption(
                        rx.el.span(
                            "Illustrative photography · not the listed food",
                            class_name="text-[10px] text-gray-400",
                        ),
                        photo_credit(),
                        class_name="mt-2 flex flex-wrap items-center justify-between gap-1",
                    ),
                    class_name="mt-8",
                ),
                class_name="min-w-0",
            ),
            rx.el.div(assistant(), class_name="w-full min-w-0 lg:pt-3"),
            class_name="grid w-full grid-cols-1 items-start gap-10 lg:grid-cols-[1.08fr_1fr] lg:gap-14",
        ),
        id="home",
        class_name="mx-auto w-full max-w-[1200px] px-6 pb-14 pt-12 lg:px-10 lg:pb-16 lg:pt-16",
    )


def workflow_card(step: dict[str, str]) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.span(
                step["number"],
                class_name="text-[11px] font-semibold tracking-wider text-[#2E6B52]/60",
            ),
            rx.icon(step["icon"], class_name="h-5 w-5 text-[#2E6B52]"),
            class_name="mb-5 flex items-center justify-between",
        ),
        rx.el.h3(
            step["title"],
            class_name="mb-2 font-['DM_Sans'] text-base font-semibold text-[#192D26]",
        ),
        rx.el.p(
            step["description"], class_name="text-xs leading-6 text-gray-500"
        ),
        key=step["number"],
        class_name="rounded-xl border border-gray-200/80 bg-white p-5 transition-colors hover:border-[#2E6B52]/30",
    )


def how_it_works() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            section_heading(
                "From planning to purpose",
                "Small steps. A better food cycle.",
                "A proposed workflow that puts canteens, collection partners and good food on the same page.",
            ),
            rx.el.div(
                rx.foreach(WORKFLOW, workflow_card),
                class_name="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4",
            ),
            rx.el.p(
                "Explore local canteen operations and the NGO directory, surplus requests and chat. Admin demo tools include fictional approvals and aggregate planning.",
                class_name="mt-5 text-xs text-gray-500",
            ),
            class_name=SECTION,
        ),
        id="how-it-works",
        class_name="border-y border-gray-100 bg-[#F7FAF7] py-16",
    )


def capability_card(capability: dict[str, str]) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.icon(capability["icon"], class_name="h-5 w-5 text-[#2E6B52]"),
            class_name="mb-4 flex h-10 w-10 items-center justify-center rounded-xl bg-[#DCEBDC]/60",
        ),
        rx.el.h3(
            capability["title"],
            class_name="mb-2 text-sm font-semibold text-[#192D26]",
        ),
        rx.el.p(
            capability["description"],
            class_name="text-xs leading-6 text-gray-500",
        ),
        key=capability["title"],
        class_name="rounded-xl border border-gray-200 bg-white p-5 transition-colors hover:border-[#2E6B52]/30",
    )


def capabilities() -> rx.Component:
    return rx.el.section(
        section_heading(
            "One thoughtful platform",
            "Built around the everyday.",
            "Eight capabilities designed for campus life. Try canteen planning and inventory, plus the NGO directory and local collection requests; Admin includes local verification and student/break assumptions. No live services are connected.",
        ),
        rx.el.div(
            rx.foreach(CAPABILITIES, capability_card),
            class_name="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4",
        ),
        class_name="mx-auto w-full max-w-[1200px] px-6 py-16 lg:px-10",
    )


def food_card(food: FoodRecord) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.img(
                src=food["image"],
                alt=f"Illustrative food photograph for {food['name']}",
                loading="lazy",
                class_name="h-44 w-full object-cover transition-transform duration-300 group-hover:scale-105",
            ),
            rx.el.span(
                "Sample listing",
                class_name="absolute left-3 top-3 w-fit rounded-full bg-white/95 px-3 py-1 text-[10px] font-semibold text-[#2E6B52]",
            ),
            class_name="relative overflow-hidden bg-[#DCEBDC]",
        ),
        rx.el.div(
            rx.el.p(
                food["canteen"],
                class_name="mb-2 text-[10px] font-semibold uppercase tracking-wider text-gray-400",
            ),
            rx.el.h3(
                food["name"],
                class_name="font-['DM_Sans'] text-lg font-semibold text-[#192D26]",
            ),
            rx.el.div(
                rx.el.span(
                    food["diet"],
                    class_name="w-fit rounded-md bg-[#DCEBDC]/60 px-2 py-1 text-[10px] font-medium text-[#2E6B52]",
                ),
                rx.el.span(
                    f"{food['portions']} portions",
                    class_name="text-sm font-semibold text-[#192D26]",
                ),
                class_name="mt-4 flex items-center justify-between gap-2",
            ),
            rx.el.div(
                rx.icon("clock-3", class_name="h-3.5 w-3.5 text-gray-400"),
                rx.el.p(
                    f"Collection: {food['collection']}",
                    class_name="text-xs text-gray-500",
                ),
                class_name="mt-4 flex items-center gap-2 border-t border-gray-100 pt-4",
            ),
            rx.el.p(
                f"Listed allergens: {food['allergens']}",
                class_name="mt-2 text-[10px] text-gray-500",
            ),
            rx.el.a(
                "Ask about this food",
                rx.icon("arrow-right", class_name="h-3.5 w-3.5"),
                href="#assistant",
                on_click=lambda: HomeState.ask_question(
                    f"What food is available: {food['name']}?"
                ),
                class_name="mt-4 inline-flex items-center gap-2 rounded text-xs font-semibold text-[#2E6B52] hover:underline focus-visible:outline-2 focus-visible:outline-[#2E6B52]",
            ),
            class_name="p-5",
        ),
        key=food["id"],
        class_name="group overflow-hidden rounded-2xl border border-gray-200 bg-white transition-colors hover:border-[#2E6B52]/40",
    )


def available_food() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                section_heading(
                    "Good food, looking ahead",
                    "A taste of what's possible.",
                    "Explore local sample listings. Quantities and windows below are illustrative, not current availability.",
                ),
                rx.el.span(
                    rx.icon("database", class_name="h-3.5 w-3.5"),
                    "Demo records",
                    class_name="mb-8 inline-flex w-fit items-center gap-2 self-start rounded-full border border-[#2E6B52]/20 bg-[#DCEBDC]/40 px-3 py-1.5 text-xs font-medium text-[#2E6B52]",
                ),
                class_name="flex flex-col justify-between gap-2 md:flex-row",
            ),
            rx.cond(
                HomeState.food.length() > 0,
                rx.el.div(
                    rx.foreach(HomeState.food, food_card),
                    class_name="grid grid-cols-1 gap-6 md:grid-cols-3",
                ),
                rx.el.div(
                    rx.icon(
                        "package-open",
                        class_name="mx-auto mb-3 h-8 w-8 text-[#2E6B52]",
                    ),
                    rx.el.p(
                        "No sample food records available.",
                        class_name="text-sm text-gray-500",
                    ),
                    class_name="rounded-xl border border-dashed border-gray-300 bg-white py-12 text-center",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Sample campus-local windows; no date or food-safety guarantee. No collections can be requested in this phase.",
                    class_name="text-[10px] leading-5 text-gray-500",
                ),
                rx.el.p(
                    "Illustrative photos: Anna Pelzer, Anh Nguyen & Eiliv Aceron / Unsplash.",
                    class_name="text-[10px] leading-5 text-gray-500",
                ),
                rx.el.a(
                    "View photography source ↗",
                    href="https://unsplash.com",
                    target="_blank",
                    rel="noopener noreferrer",
                    class_name="text-[10px] text-[#2E6B52] underline underline-offset-2",
                ),
                class_name="mt-5 flex flex-col gap-1",
            ),
            class_name=SECTION,
        ),
        id="available-food",
        class_name="border-y border-gray-100 bg-[#FAFBFA] py-16",
    )


def metric(value: str, label: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="mb-5 h-5 w-5 text-[#2E6B52]"),
        rx.el.p(
            value,
            class_name="font-['DM_Sans'] text-4xl font-semibold tracking-tight text-[#192D26]",
        ),
        rx.el.p(label, class_name="mt-2 text-xs text-gray-600"),
        class_name="w-full rounded-xl border border-[#2E6B52]/15 bg-white/70 p-5 md:p-6",
    )


def impact() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            section_heading(
                "Transparent by design",
                "Demo Data",
                "A snapshot calculated directly from the same sample records used by the listings and assistant. Not real-world impact.",
            ),
            rx.el.div(
                metric(
                    f"{HomeState.available_portions}",
                    "Available sample portions",
                    "utensils",
                ),
                metric(
                    f"{HomeState.collected_portions}",
                    "Previously collected sample portions",
                    "hand-heart",
                ),
                metric(
                    f"{HomeState.available_weight:.1f} kg",
                    "Weight of available sample food",
                    "weight",
                ),
                metric(
                    f"{HomeState.approved_count}",
                    "Approved fictional organizations",
                    "badge-check",
                ),
                class_name="grid w-full grid-cols-2 gap-4 md:grid-cols-4",
            ),
            rx.el.p(
                "Available and collected counts are separate recorded fields. No inferred meals served, carbon savings or actual partnerships.",
                class_name="mt-5 text-xs leading-6 text-gray-500",
            ),
            class_name="rounded-2xl bg-[#DCEBDC]/55 p-6 md:p-10",
        ),
        class_name="mx-auto w-full max-w-[1200px] px-6 py-16 lg:px-10",
    )


def about() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("sprout", class_name="h-8 w-8 text-[#2E6B52]"),
                    class_name="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-[#DCEBDC]",
                ),
                section_heading(
                    "About Canteenio",
                    "Less food wasted.\nMore care shared.",
                    "A simple idea: better food planning and better connections can help good food go further.",
                ),
                class_name="min-w-0",
            ),
            rx.el.div(
                rx.el.p(
                    "Canteenio is a campus food-management and surplus-sharing concept. It brings the everyday needs of canteens and community organizations into one considered workflow.",
                    class_name="text-base leading-8 text-gray-600",
                ),
                rx.el.p(
                    "This is an early public demo, not an operational donation platform. Food and organization records are fictional examples. The assistant uses local rules, not an AI API. Authentication, live databases, messaging and collections are not connected.",
                    class_name="mt-4 text-sm leading-7 text-gray-500",
                ),
                rx.el.div(
                    rx.el.p(
                        "Different roles. One shared purpose.",
                        class_name="mb-4 text-sm font-semibold text-[#192D26]",
                    ),
                    workspace_links(),
                    rx.el.p(
                        "Open the canteen and NGO demos; Admin includes local verification and student/break assumptions. No sign-in needed.",
                        class_name="mt-3 text-xs text-gray-500",
                    ),
                    class_name="mt-6 border-t border-gray-200 pt-6",
                ),
                class_name="min-w-0",
            ),
            class_name="grid grid-cols-1 gap-6 md:grid-cols-2 md:gap-16",
        ),
        id="about",
        class_name="mx-auto w-full max-w-[1200px] px-6 pb-16 pt-2 lg:px-10",
    )


def route_notice() -> rx.Component:
    return rx.cond(
        HomeState.route_notice != "",
        rx.el.section(
            rx.el.div(
                rx.icon("info", class_name="h-5 w-5 shrink-0 text-[#2E6B52]"),
                rx.el.div(
                    rx.el.h2(
                        "Public demo · workspace preview",
                        class_name="text-base font-semibold text-[#192D26]",
                    ),
                    rx.el.p(
                        HomeState.route_notice,
                        class_name="mt-2 text-sm leading-6 text-gray-600",
                    ),
                    rx.el.div(workspace_links(), class_name="mt-4"),
                    rx.el.a(
                        "Return to home",
                        href="/",
                        class_name="mt-4 inline-block text-xs font-semibold text-[#2E6B52] underline underline-offset-4",
                    ),
                ),
                class_name="flex items-start gap-3 rounded-xl border border-[#2E6B52]/20 bg-[#DCEBDC]/30 p-6",
            ),
            aria_live="polite",
            class_name="mx-auto w-full max-w-[1200px] px-6 pt-8 lg:px-10",
        ),
    )
