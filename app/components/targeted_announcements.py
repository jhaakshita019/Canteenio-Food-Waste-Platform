import reflex as rx
from app.states.canteen_state import CanteenState, TargetedAnnouncement


def targeted_card(row: TargetedAnnouncement) -> rx.Component:
    return rx.el.article(
        rx.el.h3(
            row["title"], class_name="text-sm font-semibold text-[#192D26]"
        ),
        rx.el.p(
            f"{row['year']} · {row['branches'].join(', ')} · break {row['start']}",
            class_name="mt-2 text-xs text-gray-600",
        ),
        rx.el.p(
            f"Expected crowd: {row['crowd']} · manually selected demo assumption",
            class_name="mt-2 text-xs font-medium text-[#6A4B10]",
        ),
        rx.el.p(
            row["note"],
            class_name="mt-2 whitespace-pre-wrap text-xs leading-6 text-gray-600",
        ),
        rx.el.p(
            "Session-local announcement · not delivered externally or measured occupancy",
            class_name="mt-2 text-[11px] text-gray-500",
        ),
        key=row["id"],
        class_name="rounded-lg border border-[#C9972A]/30 bg-[#FFF9EA] p-4",
    )


def targeted_list() -> rx.Component:
    return rx.el.section(
        rx.el.h2(
            "Admin · targeted local announcements",
            class_name="mb-3 font-['DM_Sans'] text-base font-semibold text-[#192D26]",
        ),
        rx.cond(
            CanteenState.targeted_announcements.length() > 0,
            rx.el.div(
                rx.foreach(CanteenState.targeted_announcements, targeted_card),
                class_name="flex flex-col gap-3",
            ),
            rx.el.p(
                "No targeted announcements saved. Create one in Admin Notifications/analytics; it appears here in the same session only.",
                class_name="text-xs leading-6 text-gray-500",
            ),
        ),
        class_name="my-4 w-full",
    )
