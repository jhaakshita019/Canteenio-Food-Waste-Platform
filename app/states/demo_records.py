import reflex as rx
from typing import TypedDict
from faker import Faker


class FoodRecord(TypedDict):
    id: str
    name: str
    canteen: str
    portions: int
    collected: int
    weight_kg: float
    collection: str
    diet: str
    allergens: str
    image: str


class OrganizationRecord(TypedDict):
    id: str
    name: str
    city: str
    mission: str
    contact: str
    email: str
    contact_notes: str
    approved: bool


_fake = Faker("en_IN")
_fake.seed_instance(42)
DEMO_ORGANIZATIONS: tuple[OrganizationRecord, ...] = tuple(
    OrganizationRecord(
        id=f"NGO-{index + 1:02d}",
        name=f"Fictional · {_fake.unique.city()} Community Kitchen {index + 1}",
        city=_fake.city(),
        mission=f"Fictional program {index + 1}: {mission}. All activities described here are illustrative, not actual services.",
        contact=f"{_fake.name()} · fictional volunteer coordinator",
        email=f"ngo{index + 1}@example.invalid",
        contact_notes=f"Demo coordination desk · {_fake.day_of_week()} planning window. Contact details are non-operational; use only the local workspace chat.",
        approved=index % 3 != 2,
    )
    for index, mission in enumerate(
        (
            "neighborhood meal sharing for older residents",
            "after-school community nutrition",
            "supporting families through a sample pantry",
            "community kitchens for temporary housing",
            "inclusive meals for people with disabilities",
            "illustrative weekend meal distribution",
            "student-led neighborhood food recovery",
            "sample outreach for daily-wage households",
            "community dining for isolated residents",
            "fictional women-led nutrition circles",
            "food access near sample transit shelters",
            "illustrative family lunch programs",
            "community meals for migrant households",
            "sample youth volunteer food sharing",
            "neighborhood nutrition education and meals",
        )
    )
)
DEMO_FOOD: tuple[FoodRecord, ...] = (
    FoodRecord(
        id="F01",
        name="Garden vegetable bowls",
        canteen="Main campus canteen",
        portions=32,
        collected=18,
        weight_kg=12.8,
        collection="12:30–13:30",
        diet="Vegetarian",
        allergens="Sesame",
        image="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=800&q=85",
    ),
    FoodRecord(
        id="F02",
        name="Fresh seasonal salad",
        canteen="North block canteen",
        portions=24,
        collected=12,
        weight_kg=7.2,
        collection="13:00–14:00",
        diet="Vegan",
        allergens="Mustard",
        image="https://images.unsplash.com/photo-1511690743698-d9d85f2fbf38?auto=format&fit=crop&w=800&q=85",
    ),
    FoodRecord(
        id="F03",
        name="Rice & vegetable plates",
        canteen="Library café",
        portions=40,
        collected=25,
        weight_kg=16.0,
        collection="14:00–15:00",
        diet="Vegetarian",
        allergens="Soy",
        image="https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=800&q=85",
    ),
)

SUGGESTED_QUESTIONS: tuple[str, ...] = (
    "How much food is remaining today?",
    "How much food have we saved from wastage?",
    "Which verified NGOs are available for food collection?",
    "How much food is still remaining for distribution?",
    "Which dishes are most popular?",
    "How much food should we prepare tomorrow?",
)

WORKFLOW: tuple[dict[str, str], ...] = (
    {
        "number": "01",
        "icon": "clipboard-list",
        "title": "Plan with purpose",
        "description": "Use enrollment, attendance and break schedules to inform preparation.",
    },
    {
        "number": "02",
        "icon": "cooking-pot",
        "title": "Prepare & track",
        "description": "Record food prepared and keep canteen inventory organized.",
    },
    {
        "number": "03",
        "icon": "receipt-text",
        "title": "Record daily sales",
        "description": "Understand what was served and what remains after each break.",
    },
    {
        "number": "04",
        "icon": "leaf",
        "title": "List surplus food",
        "description": "Share portions, collection windows and food-handling details.",
    },
    {
        "number": "05",
        "icon": "badge-check",
        "title": "Connect with NGOs",
        "description": "Approved organizations discover food and request a collection.",
    },
    {
        "number": "06",
        "icon": "handshake",
        "title": "Coordinate collection",
        "description": "Confirm pickup details and record the handover together.",
    },
    {
        "number": "07",
        "icon": "chart-no-axes-combined",
        "title": "Learn & improve",
        "description": "Review recorded outcomes to make the next day's planning better.",
    },
)
CAPABILITIES: tuple[dict[str, str], ...] = (
    {
        "icon": "package",
        "title": "Food inventory",
        "description": "A clearer picture of preparation, sales and remaining portions.",
    },
    {
        "icon": "calendar-clock",
        "title": "Smarter break planning",
        "description": "Branch and year-wise schedules with attendance assumptions.",
    },
    {
        "icon": "sprout",
        "title": "Surplus management",
        "description": "Give good food a next destination instead of a bin.",
    },
    {
        "icon": "badge-check",
        "title": "NGO verification",
        "description": "An approval process that makes organization status explicit.",
    },
    {
        "icon": "truck",
        "title": "Collection requests",
        "description": "Organized requests and clear pickup windows.",
    },
    {
        "icon": "messages-square",
        "title": "Connected communication",
        "description": "Planned messaging between canteens and collection partners.",
    },
    {
        "icon": "bell",
        "title": "Useful notifications",
        "description": "Planned alerts for food availability and collection updates.",
    },
    {
        "icon": "chart-no-axes-combined",
        "title": "Meaningful analytics",
        "description": "Traceable totals, not unsupported impact estimates.",
    },
)
