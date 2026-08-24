# 🚨 ResQRoute

**AI-Assisted Disaster Resource Triage & Allocation**  
*Team Akaza — Ideathon Submission (Theme: Crisis Management)*

## The Problem
When a disaster hits, citizens flood government helplines with requests for help. A human operator has to manually read every request, decide who needs help most, and figure out what resource (boat, ambulance, food) to send where. Under real disaster load, this breaks down: requests come in faster than they can be triaged, and first-come-first-served (FIFO) dispatching means critical cases often wait while non-critical queries consume the last available resources.

## The Solution: A Hybrid Architecture
ResQRoute is the decision-support middleware between "citizen sent a request" and "resource dispatched." It takes structured requests and a live resource inventory, and automatically triages and allocates based on capacity.

We deliberately built ResQRoute on a **Hybrid Architecture (Deterministic Rules + LLM Fallback)**:
*   **Explainable & Fast:** Life-threatening P1 and urgent P2 requests are routed via a deterministic rules engine. Every triage decision has a plain-English reason a judge or auditor can verify instantly.
*   **LLM as a Filter:** Gemini is strictly used to parse ambiguous messages and auto-resolve P3 general inquiries, keeping emergency bandwidth clear.
*   **Fail-Safe:** If the LLM API rate-limits or times out during a crisis, the system gracefully degrades, flagging the request for manual review without crashing the critical P1 routing loop.

## How It Works (Workflow)
1. **Input:** Operator uploads a CSV of requests (id, citizen_name, zone, message) or triggers the live demo dataset.
2. **Weather Context:** The system pulls current flood/rainfall risk for the city to contextualize the situation.
3. **Hybrid Triage:** Each request is classified into:
   *   *Category:* RESCUE, MEDICAL, RELIEF_SUPPLIES, or GENERAL_INQUIRY
   *   *Urgency:* P1_CRITICAL, P2_URGENT, or P3_INFO
4. **Capacity-Aware Allocation:** Requests are sorted strictly P1 → P2 → P3. The system checks local zone inventory. If a match is found, it is marked **RECOMMENDED**. If inventory is depleted, it is marked **QUEUED**, preserving priority order.
5. **Output:** The live dashboard displays color-coded urgency, reasoning, and allocation status for the human operator to review and officially dispatch.

## Tech Stack
*   **Backend:** FastAPI (Python)
*   **Logic:** Custom Hybrid Engine (Python + Google Gemini API)
*   **Frontend:** Vanilla HTML/CSS/JS Dashboard (Zero-build, highly resilient)
*   **Data:** JSON/CSV for in-memory state (Designed for PostgreSQL/PostGIS migration)

## Setup & Run

```bash
# 1. Activate environment
cd Akaza
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
pip install python-multipart

# 3. Export API Key (Required for P3 fallback triage)
export GEMINI_API_KEY="your_api_key_here"

# 4. Run the server
uvicorn app:app --reload