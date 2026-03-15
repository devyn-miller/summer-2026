"""Seed data."""

MASTER_CALENDAR_ENTRIES = [
    ("Aquarium Date 🦆", "2026-06-20", "2026-06-20", "Planned"),
    ("Sunset Picnic 🫧", "2026-07-03", "2026-07-03", "Planned"),
    ("Downtown Disney 🦮", "2026-07-18", "2026-07-18", "Planned"),
]

ACTIVITIES_ENTRIES = [
    ("Aquarium 🦆", "Event", 3, 45, "Planned", "Low", "Any", ["You + BF"]),
    ("Discovery Cube 👽", "Event", 3, 35, "Planned", "Low", "Any", ["You + BF"]),
    ("Downtown Disney 🦮", "Event", 4, 60, "Planned", "Medium", "Cool evening", ["You + BF"]),
    ("Game Night 🔥", "Indoor", 3, 10, "Planned", "Low", "Any", ["You + BF", "Friends"]),
    ("Sunset Picnic + Playlist Swap 🫧", "Outdoor", 2, 20, "Planned", "Low", "Cool evening", ["You + BF"]),
    ("Movie Night (Theme) 4️⃣", "Indoor", 3, 15, "Planned", "Low", "Any", ["You + BF"]),
    ("Escape Room 🕓", "Event", 2, 50, "Planned", "Medium", "Any", ["You + BF", "Friends"]),
    ("Indoor Rock Climbing 🐶", "Indoor", 2, 40, "Planned", "High", "Any", ["You + BF"]),
]

AVAILABILITY_CONFLICTS_MAP = {
    (
        "Typical Week",
        "You",
    ): (
        "Work Monday-Friday until about 3:00pm or 4:00pm. BF availability still TBD.",
        ["Mon-Thu After Work", "Fri After Work", "Saturday", "Sunday"],
    ),
}

PLACES_ENTRIES = [
    ("Aquarium of the Pacific", "Long Beach, CA", "Other", 37, 45, "https://www.aquariumofpacific.org", 5),
    ("Discovery Cube", "Santa Ana, CA", "Other", 22, 35, "https://www.discoverycube.org", 4),
    ("Downtown Disney District", "Anaheim, CA", "City", 28, 30, "https://disneyland.disney.go.com/destinations/downtown-disney-district", 4),
    ("Huntington Library Botanical Gardens", "San Marino, CA", "Park", 52, 29, "https://huntington.org", 5),
]

BUCKET_LIST_ENTRIES = [
    ("Stargazing date night 🐶", "High", ["Chill", "Travel"], "Not Started", ["You + BF"]),
    ("PowerPoint night 👽", "Medium", ["Creative", "Social"], "Not Started", ["You + BF", "Friends"]),
    ("YouTube karaoke night 🔥", "Medium", ["Social"], "Not Started", ["You + BF", "Friends"]),
    ("DIY project night (lego / 3D print) 🫧", "High", ["Creative"], "Not Started", ["You + BF"]),
    ("Escape room challenge 🕓", "High", ["Adventure", "Social"], "Not Started", ["You + BF", "Friends"]),
    ("Botanical garden day 🦮", "Medium", ["Chill"], "Not Started", ["You + BF"]),
]

BUDGET_ENTRIES = [
    ("Total Summer Budget", "Other", 2000, 0, "General", "Free"),
    ("Aquarium tickets", "Tickets", 90, 0, "General", "$$"),
    ("Discovery Cube tickets", "Tickets", 70, 0, "General", "$$"),
    ("Downtown Disney food + parking", "Food", 80, 0, "General", "$$"),
    ("Game night snacks", "Food", 25, 0, "General", "$"),
]

HIGHLIGHTS_ENTRIES = [
    ("Aquarium date 🦆", "2026-06-20", ["You + BF"], "Long Beach, CA", 5, "Loved the jellyfish exhibits."),
    ("Sunset picnic 🫧", "2026-07-03", ["You + BF"], "Local park", 5, "Playlist swap was super cute."),
]

