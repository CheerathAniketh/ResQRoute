import httpx
import json

BASE_URL = "http://127.0.0.1:8000/api"

def run():
    print("\n--- [1] Checking Weather Threat Level ---")
    weather = httpx.get(f"{BASE_URL}/weather-risk?city=Hyderabad").json()
    print(f"City: {weather['city']} | Rainfall: {weather['rainfall_mm']} mm/h | Risk: {weather['risk_level']}")

    print("\n--- [2] Simulating Disaster Influx & Triage ---")
    demo = httpx.get(f"{BASE_URL}/demo-run").json()
    
    print("\n[TRIAGE & RANKING RESULTS]")
    for t in demo["triage_results"]:
        print(f"-> [{t['urgency_level']}] {t['citizen_name']} ({t['zone']}): {t['category']} - {t['reasoning']}")

    print("\n[RESOURCE DISPATCH PLAN]")
    for a in demo["resource_allocation"]:
        print(f"-> Req ID: {a['request_id']} | Priority: {a['urgency_level']} | Resource: {a['assigned_resource_id']} ({a['resource_type']}) | Status: {a['status']}")

if __name__ == "__main__":
    run()