"""
Synthetic resource pool generator for ResQRoute demo.

Usage:
    python generate_resources.py                 # default balanced pool -> data/mock_resources.json
    python generate_resources.py scarce           # fewer resources, for a stress-test demo
    python generate_resources.py abundant         # more resources, for a "well-funded city" demo
    python generate_resources.py balanced my.json # custom scenario + filename
"""

import json
import sys

# Base per-zone counts for each scenario. Tune these to control how
# dramatic the QUEUED/scarcity story looks during the live demo.
SCENARIOS = {
    "scarce": {
        "Rescue Boat": 1,
        "Ambulance": 1,
        "Food/Water Kit": 1,
    },
    "balanced": {
        "Rescue Boat": 2,
        "Ambulance": 2,
        "Food/Water Kit": 3,
    },
    "abundant": {
        "Rescue Boat": 4,
        "Ambulance": 3,
        "Food/Water Kit": 6,
    },
}

CAPACITY_BY_TYPE = {
    "Rescue Boat": 6,
    "Ambulance": 2,
    "Food/Water Kit": 50,
}

ZONES = ["Zone-A", "Zone-B"]

TYPE_PREFIX = {
    "Rescue Boat": "BOAT",
    "Ambulance": "AMB",
    "Food/Water Kit": "FOOD",
}


def generate_resources(scenario: str):
    counts = SCENARIOS[scenario]
    resources = []
    counters = {t: 0 for t in counts}

    for res_type, per_zone_count in counts.items():
        for zone in ZONES:
            for _ in range(per_zone_count):
                counters[res_type] += 1
                idx = counters[res_type]
                resources.append({
                    "id": f"RES-{TYPE_PREFIX[res_type]}-{idx:02d}",
                    "type": res_type,
                    "zone": zone,
                    "capacity": CAPACITY_BY_TYPE[res_type],
                    "status": "AVAILABLE",
                })

    return resources


def main():
    scenario = sys.argv[1] if len(sys.argv) > 1 else "balanced"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "data/mock_resources.json"

    if scenario not in SCENARIOS:
        print(f"Unknown scenario '{scenario}'. Choose from: {list(SCENARIOS.keys())}")
        sys.exit(1)

    resources = generate_resources(scenario)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(resources, f, indent=2)

    print(f"Generated {len(resources)} resources ('{scenario}' scenario) -> {out_path}")


if __name__ == "__main__":
    main()