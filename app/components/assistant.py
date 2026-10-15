import reflex as rx
from app.states.home_state import HomeState, ChatMessage
from app.states.demo_records import SUGGESTED_QUESTIONS


def message_bubble(message: ChatMessage) -> rx.Component:
    return rx.el.div(
        rx.cond(
            message["role"] == "assistant",
            rx.el.div(
                rx.icon("sprout", class_name="h-4 w-4 text-[#2E6B52]"),
                class_name="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-[#DCEBDC]",
            ),
        ),
        rx.el.div(
            rx.el.p(
                rx.cond(message["role"] == "assistant", "Canteenio", "You"),
                class_name="mb-1 text-[10px] font-semibold uppercase tracking-wider text-gray-500",
            ),
            rx.el.p(
                message["text"],
                class_name="text-[13px] leading-[1.75] text-[#192D26]",
            ),
            class_name=rx.cond(
                message["role"] == "assistant",
                "max-w-[92%] rounded-xl rounded-tl-sm border border-gray-100 bg-white px-4 py-3",
                "max-w-[92%] rounded-xl rounded-tr-sm bg-[#DCEBDC]/65 px-4 py-3",
            ),
        ),
        key=message["id"],
        class_name=rx.cond(
            message["role"] == "assistant",
            "flex items-start gap-2",
            "flex justify-end gap-2",
        ),
    )


def assistant() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("sparkles", class_name="h-5 w-5 text-[#2E6B52]"),
                    class_name="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-[#DCEBDC]",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Canteenio AI Assistant",
                        class_name="font-['DM_Sans'] text-lg font-bold text-[#192D26]",
                    ),
                    rx.el.p(
                        "Your guide to smarter canteens and less food waste.",
                        class_name="mt-1 text-xs leading-5 text-gray-500",
                    ),
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.button(
                rx.icon("rotate-ccw", class_name="h-4 w-4"),
                on_click=HomeState.clear_chat,
                title="Reset conversation",
                aria_label="Reset conversation",
                class_name="shrink-0 rounded-lg p-2 text-gray-400 hover:bg-[#DCEBDC]/50 hover:text-[#2E6B52] focus-visible:outline-2 focus-visible:outline-[#2E6B52]",
            ),
            class_name="flex items-center justify-between gap-2 px-5 pb-4 pt-5",
        ),
        rx.el.div(
            rx.el.span(
                class_name="h-1.5 w-1.5 shrink-0 rounded-full bg-[#2E6B52]"
            ),
            rx.el.p(
                "Demo · rule-based answers from sample records — not a live AI API",
                class_name="text-[10px] font-medium leading-4 text-[#2E6B52]",
            ),
            class_name="mx-5 flex items-center gap-2 rounded-lg bg-[#DCEBDC]/40 px-3 py-2",
        ),
        rx.el.div(
            rx.foreach(HomeState.messages, message_bubble),
            role="log",
            aria_live="polite",
            aria_label="Assistant conversation",
            tab_index=0,
            class_name="my-4 flex h-[220px] flex-col gap-3 overflow-y-auto bg-gray-50/70 px-5 py-4 focus-visible:outline-2 focus-visible:outline-[#2E6B52]",
        ),
        rx.el.div(
            rx.el.p(
                "A few things you can ask",
                class_name="mb-2 text-[10px] font-semibold uppercase tracking-wider text-gray-400",
            ),
            rx.el.div(
                rx.foreach(
                    SUGGESTED_QUESTIONS,
                    lambda question: rx.el.button(
                        question,
                        type="button",
                        on_click=lambda: HomeState.ask_question(question),
                        class_name="rounded-lg border border-gray-200 bg-white px-2.5 py-2 text-[11px] font-medium text-gray-600 transition-colors hover:border-[#2E6B52]/40 hover:bg-[#DCEBDC]/40 hover:text-[#2E6B52] focus-visible:outline-2 focus-visible:outline-[#2E6B52]",
                    ),
                ),
                class_name="flex flex-wrap gap-2",
            ),
            class_name="px-5 pb-4",
        ),
        rx.el.form(
            rx.el.label(
                "Ask the demo assistant",
                html_for="assistant-question",
                class_name="sr-only",
            ),
            rx.el.input(
                id="assistant-question",
                name="question",
                placeholder="Ask about the sample food…",
                required=True,
                max_length=400,
                auto_complete="off",
                class_name="min-w-0 flex-1 rounded-lg bg-transparent px-2 py-2.5 text-xs text-[#192D26] placeholder:text-gray-400 focus-visible:outline-2 focus-visible:outline-[#2E6B52]",
            ),
            rx.el.button(
                rx.icon("arrow-up", class_name="h-4 w-4"),
                type="submit",
                aria_label="Send question",
                class_name="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-[#2E6B52] text-white transition-colors hover:bg-[#24553F] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#2E6B52]",
            ),
            on_submit=HomeState.submit_question,
            reset_on_submit=True,
            class_name="mx-5 mb-5 flex items-center gap-2 rounded-xl border border-gray-200 bg-white p-1.5",
        ),
        id="assistant",
        aria_label="Canteenio demo assistant",
        class_name="w-full overflow-hidden rounded-2xl border border-gray-200 bg-white",
    )
