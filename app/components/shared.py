import reflex as rx
from app.states.home_state import HomeState

PRIMARY_LINK = "inline-flex items-center justify-center gap-2 rounded-xl bg-[#2E6B52] px-5 py-3 text-sm font-semibold text-white transition-colors hover:bg-[#24553F] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#2E6B52]"
SECONDARY_LINK = "inline-flex items-center justify-center gap-2 rounded-xl border border-gray-200 bg-white px-5 py-3 text-sm font-semibold text-[#192D26] transition-colors hover:border-[#2E6B52] hover:bg-[#DCEBDC]/30 focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#2E6B52]"
TEXT_LINK = "rounded-md text-sm font-medium text-gray-600 transition-colors hover:text-[#2E6B52] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#2E6B52]"
SECTION = "mx-auto w-full max-w-[1200px] px-6 lg:px-10"


def brand() -> rx.Component:
    return rx.el.a(
        rx.el.span(
            rx.icon("utensils", class_name="h-6 w-6 text-[#2E6B52]"),
            rx.icon(
                "leaf",
                class_name="absolute -right-1 -top-1 h-4 w-4 bg-white text-[#2E6B52]",
            ),
            class_name="relative mr-1 flex h-9 w-9 items-center justify-center rounded-xl border border-[#2E6B52]/30 bg-white",
        ),
        rx.el.span(
            "canteenio",
            class_name="font-['DM_Sans'] text-[25px] font-bold tracking-[-1px] text-[#192D26]",
        ),
        href="/",
        aria_label="Canteenio home",
        class_name="flex w-fit items-center gap-2 rounded-md focus-visible:outline-2 focus-visible:outline-[#2E6B52]",
    )


def navigation() -> rx.Component:
    return rx.fragment(
        rx.el.a(
            "Home",
            href="/#home",
            on_click=HomeState.close_menu,
            class_name=TEXT_LINK,
        ),
        rx.el.a(
            "How It Works",
            href="/#how-it-works",
            on_click=HomeState.close_menu,
            class_name=TEXT_LINK,
        ),
        rx.el.a(
            "Available Food",
            href="/#available-food",
            on_click=HomeState.close_menu,
            class_name=TEXT_LINK,
        ),
        rx.el.a(
            "About Us",
            href="/#about",
            on_click=HomeState.close_menu,
            class_name=TEXT_LINK,
        ),
    )


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            brand(),
            rx.el.nav(
                navigation(),
                aria_label="Main navigation",
                class_name="hidden items-center gap-7 lg:flex",
            ),
            rx.el.div(
                rx.el.a(
                    "Login",
                    href="/login",
                    class_name="hidden rounded-lg px-3 py-2 text-sm font-semibold text-[#192D26] hover:bg-[#DCEBDC]/40 focus-visible:outline-2 focus-visible:outline-[#2E6B52] sm:inline-flex",
                ),
                rx.el.a(
                    "Get Started",
                    rx.icon("arrow-up-right", class_name="h-4 w-4"),
                    href="/get-started",
                    class_name=PRIMARY_LINK,
                ),
                rx.el.button(
                    rx.icon("menu", class_name="h-5 w-5"),
                    on_click=HomeState.toggle_menu,
                    aria_label="Toggle navigation",
                    aria_expanded=HomeState.mobile_menu,
                    class_name="rounded-lg p-2 text-[#192D26] hover:bg-[#DCEBDC] focus-visible:outline-2 focus-visible:outline-[#2E6B52] lg:hidden",
                ),
                class_name="flex items-center gap-2 sm:gap-3",
            ),
            class_name="mx-auto flex h-20 w-full max-w-[1200px] items-center justify-between gap-4 px-6 lg:px-10",
        ),
        rx.cond(
            HomeState.mobile_menu,
            rx.el.nav(
                navigation(),
                rx.el.a("Login", href="/login", class_name=TEXT_LINK),
                aria_label="Mobile navigation",
                class_name="flex flex-col gap-5 border-t border-gray-100 bg-white px-6 py-5 lg:hidden",
            ),
        ),
        class_name="sticky top-0 z-40 w-full border-b border-gray-100 bg-white/95 backdrop-blur-md",
    )


def section_heading(eyebrow: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            eyebrow,
            class_name="mb-3 text-xs font-semibold uppercase tracking-[0.18em] text-[#2E6B52]",
        ),
        rx.el.h2(
            title,
            class_name="font-['DM_Sans'] text-3xl font-semibold leading-tight tracking-[-1px] text-[#192D26] md:text-[38px]",
        ),
        rx.el.p(
            description,
            class_name="mt-4 max-w-2xl text-sm leading-7 text-gray-500 md:text-base",
        ),
        class_name="mb-9",
    )


def workspace_links() -> rx.Component:
    return rx.el.div(
        rx.el.a(
            rx.icon("cooking-pot", class_name="h-4 w-4"),
            "Canteen",
            rx.icon("arrow-up-right", class_name="h-4 w-4"),
            href="/canteen",
            class_name=SECONDARY_LINK,
        ),
        rx.el.a(
            rx.icon("hand-heart", class_name="h-4 w-4"),
            "NGO",
            rx.icon("arrow-up-right", class_name="h-4 w-4"),
            href="/ngo",
            class_name=SECONDARY_LINK,
        ),
        rx.el.a(
            rx.icon("shield-check", class_name="h-4 w-4"),
            "Admin",
            rx.icon("arrow-up-right", class_name="h-4 w-4"),
            href="/admin",
            class_name=SECONDARY_LINK,
        ),
        class_name="flex flex-wrap gap-3",
    )


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                brand(),
                rx.el.p(
                    "Good food. Better connections.",
                    class_name="mt-3 text-sm text-gray-500",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Explore the concept",
                    class_name="mb-4 text-sm font-semibold text-[#192D26]",
                ),
                workspace_links(),
                rx.el.p(
                    "Canteen, NGO & Admin demos ready · session-local only",
                    class_name="mt-3 text-xs text-gray-500",
                ),
            ),
            class_name="flex flex-col justify-between gap-8 border-b border-gray-200 pb-8 md:flex-row",
        ),
        rx.el.div(
            rx.el.p(
                "Canteenio · Public demo", class_name="text-xs text-gray-500"
            ),
            rx.el.p(
                "Sample data only. No live accounts, pickups or AI service.",
                class_name="text-xs text-gray-500",
            ),
            rx.el.a("Back to top ↑", href="#home", class_name=TEXT_LINK),
            class_name="flex flex-col justify-between gap-4 pt-6 md:flex-row md:items-center",
        ),
        class_name="mx-auto w-full max-w-[1200px] px-6 py-10 lg:px-10",
    )
