import json
from typing import List
from api.models import TriageResult, ResourceAllocation

def load_resources():
    with open("data/mock_resources.json", "r") as f:
        return json.load(f)

def allocate_resources(triage_list: List[TriageResult]) -> List[ResourceAllocation]:
    resources = load_resources()
    allocations = []

    # Sort so P1_CRITICAL gets allocated first
    priority_order = {"P1_CRITICAL": 0, "P2_URGENT": 1, "P3_INFO": 2}
    sorted_triages = sorted(triage_list, key=lambda x: priority_order.get(x.urgency_level, 3))

    for item in sorted_triages:
        assigned = None
        
        # Resource matching logic
        if item.category == "RESCUE":
            assigned = next((r for r in resources if r["type"] == "Rescue Boat" and r["zone"] == item.zone and r["status"] == "AVAILABLE"), None)
        elif item.category == "MEDICAL":
            assigned = next((r for r in resources if r["type"] == "Ambulance" and r["status"] == "AVAILABLE"), None)
        elif item.category == "RELIEF_SUPPLIES":
            assigned = next((r for r in resources if r["type"] == "Food/Water Kit" and r["status"] == "AVAILABLE"), None)

        if assigned:
            assigned["status"] = "DISPATCHED"
            allocations.append(ResourceAllocation(
                request_id=item.request_id,
                urgency_level=item.urgency_level,
                assigned_resource_id=assigned["id"],
                resource_type=assigned["type"],
                status="DISPATCHED"
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