import reflex as rx
from app.components.shared import header, footer
from app.components.home import (
    hero,
    how_it_works,
    capabilities,
    available_food,
    impact,
    about,
    route_notice,
)
from app.states.home_state import HomeState
from app.components.canteen import canteen_workspace
from app.components.ngo import ngo_workspace
from app.components.admin import admin_workspace


def index() -> rx.Component:
    return rx.el.div(
        rx.el.a(
            "Skip to content",
            href="#main-content",
            class_name="sr-only rounded-lg bg-white p-3 text-[#2E6B52] focus:not-sr-only focus:fixed focus:left-3 focus:top-3 focus:z-50",
        ),
        header(),
        rx.el.main(
            route_notice(),
            hero(),
            how_it_works(),
            capabilities(),
            available_food(),
            impact(),
            about(),
            id="main-content",
            class_name="w-full",
        ),
        rx.el.div(footer(), class_name="border-t border-gray-200 bg-[#FAFBFA]"),
        class_name="min-h-dvh w-full bg-white font-['Inter'] text-[#192D26] antialiased",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=["/theme.css"],
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            cross_origin="",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(
    index,
    route="/",
    title="Canteenio | Good food deserves a second chance",
    description="Explore the Canteenio public demo: thoughtful canteen planning, surplus food sharing and transparent sample data.",
    on_load=HomeState.load_route,
)
app.add_page(
    index,
    route="/login",
    title="Canteenio | Login preview",
    on_load=HomeState.load_route,
)
app.add_page(
    index,
    route="/get-started",
    title="Canteenio | Get started",
    on_load=HomeState.load_route,
)
app.add_page(
    canteen_workspace,
    route="/canteen",
    title="Canteenio | Canteen demo workspace",
    description="Session-local demo operations, inventory, surplus, branch breaks and simulated messaging. No live services.",
)
app.add_page(
    ngo_workspace,
    route="/ngo",
    title="Canteenio | Fictional NGO demo workspace",
    description="15 fictional NGO profiles, reviewed session-local surplus, simulated collection requests and local messaging. No real pickups or live services.",
)
app.add_page(
    admin_workspace,
    route="/admin",
    title="Canteenio | Open admin demo workspace",
    description="Open, session-local fictional NGO verification, aggregate enrollment assumptions, break schedules, food oversight and announcements. Not access-protected or saved to Supabase.",
)
