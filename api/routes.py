import json
from fastapi import APIRouter
from core.weather import check_flood_risk
from core.agent import triage_request
from core.allocator import allocate_resources
from api.models import CitizenRequest

router = APIRouter()

@router.get("/weather-risk")
def get_weather(city: str = "Hyderabad"):
    return check_flood_risk(city)

@router.post("/triage-and-allocate")
def process_requests(requests: list[CitizenRequest]):
    triaged = [triage_request(req) for req in requests]
    allocated = allocate_resources(triaged)
    return {
        "total_requests": len(requests),
        "triage_summary": triaged,
        "allocation_plan": allocated
    }

@router.get("/demo-run")
def demo_run():
    with open("data/sample_requests.json", "r") as f:
        data = json.load(f)
    requests = [CitizenRequest(**item) for item in data]
    triaged = [triage_request(req) for req in requests]
    allocated = allocate_resources(triaged)
    return {
        "status": "Success",
        "weather_state": check_flood_risk("Hyderabad"),
        "triage_results": triaged,
        "resource_allocation": allocated
    }