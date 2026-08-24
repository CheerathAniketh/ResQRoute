import json
from typing import List
from api.models import TriageResult, ResourceAllocation

def load_resources():
    with open("data/mock_resources.json", "r") as f:
        return json.load(f)

def allocate_resources(triage_list: List[TriageResult]) -> List[ResourceAllocation]:
    resources = load_resources()
    for r in resources:
        r["remaining"] = r.get("capacity", 1)

    allocations = []
    priority_order = {"P1_CRITICAL": 0, "P2_URGENT": 1, "P3_INFO": 2}
    
    # Sort strictly by priority level (P1 -> P2 -> P3)
    sorted_triages = sorted(triage_list, key=lambda x: (priority_order.get(x.urgency_level, 3), x.request_id))

    category_to_type = {
        "RESCUE": "Rescue Boat",
        "MEDICAL": "Ambulance",
        "RELIEF_SUPPLIES": "Food/Water Kit"
    }

    for item in sorted_triages:
        assigned = None
        target_type = category_to_type.get(item.category)

        if target_type:
            # 1. Prefer resources within the same zone
            assigned = next(
                (r for r in resources if r["type"] == target_type and r.get("zone") == item.zone and r["remaining"] > 0),
                None
            )
            # 2. If ambulances or relief kits run out in-zone, check unzoned/cross-zone supply
            if not assigned and target_type in ["Ambulance", "Food/Water Kit"]:
                assigned = next(
                    (r for r in resources if r["type"] == target_type and r["remaining"] > 0),
                    None
                )

        if assigned:
            assigned["remaining"] -= 1
            allocations.append(ResourceAllocation(
                request_id=item.request_id,
                urgency_level=item.urgency_level,
                assigned_resource_id=assigned["id"],
                resource_type=assigned["type"],
                status="RECOMMENDED"  # Aligns with UI display
            ))
        else:
            allocations.append(ResourceAllocation(
                request_id=item.request_id,
                urgency_level=item.urgency_level,
                assigned_resource_id=None,
                resource_type=None,
                status="QUEUED" if item.urgency_level != "P3_INFO" else "RESOLVED_AUTO"
            ))

    return allocations