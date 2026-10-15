import reflex as rx
from app.states.canteen_state import CanteenState, CollectionRequest

BUTTON = "inline-flex items-center justify-center gap-2 rounded-lg bg-[#2E6B52] px-3 py-2 text-xs font-semibold text-white hover:bg-[#24553F] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#2E6B52] disabled:opacity-40"
OUTLINE = "inline-flex items-center justify-center gap-2 rounded-lg border border-gray-200 bg-white px-3 py-2 text-xs font-medium text-gray-700 hover:bg-gray-50 focus-visible:outline-2 focus-visible:outline-[#2E6B52]"


def request_card(row: CollectionRequest, canteen: bool = False) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    row["food"],
                    class_name="text-sm font-semibold text-[#192D26]",
                ),
                rx.el.p(
                    row["organization"], class_name="mt-1 text-xs text-gray-600"
                ),
            ),
            rx.el.span(
                row["status"],
                class_name=rx.match(
                    row["status"],
                    (
                        "Collected",
                        "h-fit w-fit rounded-lg bg-green-100 px-2 py-1 text-xs font-medium text-green-600",
                    ),
                    (
                        "Cancelled",
                        "h-fit w-fit rounded-lg bg-gray-100 px-2 py-1 text-xs text-gray-600",
                    ),
                    (
                        "Rejected",
                        "h-fit w-fit rounded-lg bg-red-100 px-2 py-1 text-xs text-red-600",
                    ),
                    "h-fit w-fit rounded-lg bg-yellow-100 px-2 py-1 text-xs font-medium text-yellow-700",
                ),
            ),
            class_name="flex items-start justify-between gap-3",
        ),
        rx.el.p(
            f"{row['quantity']} portions · {row['location']} · {row['window']}",
            class_name="mt-3 text-xs font-medium text-gray-700",
        ),
        rx.el.p(
            row["notes"],
            class_name="mt-2 whitespace-pre-wrap break-words text-xs leading-5 text-gray-600",
        ),
        rx.el.p(
            f"Request ID: {row['id']}",
            class_name="mt-2 break-all text-[10px] text-gray-400",
        ),
        rx.el.div(
            rx.cond(
                canteen,
                rx.fragment(
                    rx.cond(
                        row["status"] == "Pending",
                        rx.el.button(
                            "Approve locally",
                            on_click=lambda: CanteenState.progress_request(
                                row["id"], "approve"
                            ),
                            class_name=BUTTON,
                        ),
                    ),
                    rx.cond(
                        row["status"] == "Confirmed",
                        rx.el.button(
                            "Mark collected · simulation",
                            on_click=lambda: CanteenState.progress_request(
                                row["id"], "collect"
                            ),
                            class_name=BUTTON,
                        ),
                    ),
                    rx.cond(
                        (row["status"] == "Pending")
                        | (row["status"] == "Approved")
                        | (row["status"] == "Confirmed"),
                        rx.el.button(
                            "Reject / release",
                            on_click=lambda: CanteenState.progress_request(
                                row["id"], "reject"
                            ),
                            class_name=OUTLINE,
                        ),
                    ),
                ),
                rx.fragment(
                    rx.cond(
                        row["status"] == "Approved",
                        rx.el.button(
                            "Confirm demo pickup plan",
                            on_click=lambda: CanteenState.progress_request(
                                row["id"], "confirm"
                            ),
                            class_name=BUTTON,
                        ),
                    ),
                    rx.cond(
                        (row["status"] == "Pending")
                        | (row["status"] == "Approved")
                        | (row["status"] == "Confirmed"),
                        rx.el.button(
                            "Cancel / release",
                            on_click=lambda: CanteenState.progress_request(
                                row["id"], "cancel"
                            ),
                            class_name=OUTLINE,
                        ),
                    ),
                ),
            ),
            class_name="mt-3 flex flex-wrap gap-2",
        ),
        rx.el.p(
            "Local demo only, resets on reload · not a real pickup or delivery",
            class_name="mt-3 text-[10px] leading-5 text-gray-500",
        ),
        key=row["id"],
        class_name="min-w-0 rounded-xl border border-gray-200 bg-white p-4",
    )


def canteen_requests() -> rx.Component:
    return rx.el.section(
        rx.el.h2(
            "Collection requests",
            class_name="font-['DM_Sans'] text-lg font-semibold text-[#17324F]",
        ),
        rx.el.p(
            "Local demo only, resets on reload. Pending requests reserve listed portions. Approve → NGO confirms → mark collected in this simulation. Cancellation or rejection releases portions without changing physical inventory.",
            class_name="mb-4 mt-2 text-xs leading-6 text-gray-500",
        ),
        rx.el.a(
            "Open NGO workspace to create a local request →",
            href="/ngo",
            class_name="mb-4 inline-block text-xs font-semibold text-[#2E6B52] underline focus-visible:outline-2",
        ),
        rx.cond(
            CanteenState.requests.length() > 0,
            rx.el.div(
                rx.foreach(
                    CanteenState.requests, lambda row: request_card(row, True)
                ),
                class_name="grid grid-cols-1 gap-3 xl:grid-cols-2",
            ),
            rx.el.p(
                "No local requests yet. Review and make a surplus listing available, then request it as an approved fictional NGO in the same browser session.",
                class_name="rounded-xl border border-dashed border-gray-300 bg-gray-50 p-6 text-xs leading-6 text-gray-500",
            ),
        ),
        class_name="rounded-xl border border-gray-200 bg-white p-5",
    )
