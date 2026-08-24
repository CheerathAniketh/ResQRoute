"""
Synthetic citizen request generator for ResQRoute demo.

Usage:
    python generate_requests.py                # 10 requests -> data/synthetic_requests.csv
    python generate_requests.py 25              # 25 requests
    python generate_requests.py 25 my_test.csv  # custom count + filename
"""

import csv
import random
import sys

NAMES = [
    "Lakshmi", "Farhan", "Meena", "Rahul", "Divya", "Arjun", "Kavya", "Imran",
    "Sneha", "Rohit", "Fatima", "Vijay", "Pooja", "Kiran", "Anand", "Nisha",
    "Sameer", "Deepa", "Manoj", "Ritu"
]

ZONES = ["Zone-A", "Zone-B"]

# Each template is tagged with the urgency/category it's designed to trigger,
# purely for our own reference — the agent re-derives category from the text.
RESCUE_MESSAGES = [
    "Water rising fast, whole family trapped on the roof!",
    "House collapsed, we are stuck under debris, please send help!",
    "Flood water entering ground floor rapidly, need boat immediately!",
    "Stranded on rooftop with two kids, water still rising!",
    "Trapped in car, water level above tires and climbing!",
]

MEDICAL_MESSAGES = [
    "Severe injury from falling debris, bleeding heavily.",
    "Elderly father having chest pain, needs urgent medical help.",
    "Deep cut from broken glass, won't stop bleeding.",
    "Pregnant woman in labor, need ambulance urgently.",
    "Someone collapsed and is unconscious, need medical help now.",
]

RELIEF_MESSAGES = [
    "Out of drinking water and food for 3 days now.",
    "Need food packets and clean water for elderly parents.",
    "No supplies left, six people in the house need relief kit.",
    "Running low on baby formula and clean water.",
    "Need blankets and food, house is flooded but we are safe.",
]

INFO_MESSAGES = [
    "Where is the nearest relief camp from here?",
    "Just checking if the shelter in our zone is still open.",
    "Is the water safe to drink right now?",
    "When will power be restored in our area?",
    "Just confirming our address is on the rescue list.",
]

CATEGORY_POOLS = [RESCUE_MESSAGES, MEDICAL_MESSAGES, RELIEF_MESSAGES, INFO_MESSAGES]
# Rough real-world-ish mix: more rescue/medical/relief than routine info queries
CATEGORY_WEIGHTS = [0.30, 0.20, 0.30, 0.20]


def generate_requests(n: int):
    rows = []
    used_names = random.sample(NAMES, min(n, len(NAMES)))
    for i in range(n):
        name = used_names[i] if i < len(used_names) else random.choice(NAMES)
        zone = random.choice(ZONES)
        pool = random.choices(CATEGORY_POOLS, weights=CATEGORY_WEIGHTS, k=1)[0]
        message = random.choice(pool)
        rows.append({
            "id": f"REQ-{200 + i}",
            "citizen_name": name,
            "zone": zone,
            "message": message,
        })
    return rows


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    out_path = sys.argv[2] if len(sys.argv) > 2 else "data/synthetic_requests.csv"

    rows = generate_requests(count)

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "citizen_name", "zone", "message"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {count} synthetic requests -> {out_path}")


if __name__ == "__main__":
    main()