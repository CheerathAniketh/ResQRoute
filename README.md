# ResQRoute: AI-Assisted Disaster Resource Triage & Allocation
**Team Akaza | Theme: Crisis Management**

## The Problem: The Cognitive Bottleneck in Crisis Response
During severe disasters, emergency control rooms do not fail from a lack of compassion; they fail from data overload and cognitive bottlenecks.
* Emergency helplines receive hundreds of unranked distress messages simultaneously.
* Standard systems default to a dangerous First-In-First-Out (FIFO) routing model.
* Under severe resource scarcity, critical cases wait in line while non-urgent requests consume the final available rescue assets.

## The Solution: Intelligent Decision-Support Middleware
ResQRoute is a high-throughput, capacity-aware triage engine that sits between incoming distress signals and the dispatch control room.
* **Ingests:** Processes unstructured emergency requests rapidly.
* **Analyzes:** Triages every request by precise urgency (P1, P2, P3) and category.
* **Allocates:** Matches requests instantly to zone-specific, available inventory.
* **Empowers:** Generates a live, prioritized dashboard for human commanders to execute.

## The Core Innovation: Hybrid Triage Architecture
We deliberately avoided building a fragile end-to-end LLM wrapper to prevent hallucinations, API rate limits, and non-deterministic latency during a crisis.
* **Deterministic Safety Net:** Life-threatening emergencies (P1) and urgent needs (P2) are processed instantly via a hard-coded, zero-latency rules engine.
* **LLM as a Filter:** Google Gemini is strictly reserved to parse ambiguous messages and auto-resolve non-emergency general inquiries.
* **Fail-Safe Degradation:** If the AI API crashes or times out, the system catches the error, queues the request for manual review, and keeps dispatching P1s without dropping a single critical request.

## Scarcity & Capacity Management
ResQRoute mathematically handles real-world resource depletion without crashing or misassigning assets.
* **Strict Priority Sorting:** The algorithm enforces a rigid hierarchy of P1 Critical, P2 Urgent, and P3 Info.
* **Zone-Aware Matching:** Resources are locked to their geographic zones to account for flooded routes and impassable roads.
* **Smart Queuing:** When inventory hits zero, the system places critical requests at the top of the queue backlog, guaranteeing they receive the next available resource first.

## Human-in-the-Loop Philosophy
ResQRoute acts as a high-speed copilot, not a blind automation tool.
* **Suggestions, Not Actions:** The system outputs recommendations rather than autonomous deployments.
* **Absolute Accountability:** The system does not dispatch physical resources; a human operator always reviews the dashboard to make the final call.
* **Contextual Overrides:** Human commanders retain complete authority to override the algorithm based on live, on-the-ground intelligence.

---

## Developer Setup & Installation Guide

**Tech Stack**
* Backend: FastAPI (Python)
* Logic: Custom Hybrid Engine (Python + Google Gemini API)
* Frontend: Vanilla HTML/CSS/JS Dashboard
* Data: JSON/CSV in-memory state (Architected for PostGIS migration)

**Local Environment Setup**
1. Activate your virtual environment: `source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Export your API Key: `export GEMINI_API_KEY="your_api_key_here"`
4. Run the server: `uvicorn app:app --reload`
5. Access the dashboard at `http://127.0.0.1:8000/`

**Simulating Disaster Scarcity for Testing**
To trigger the capacity-aware queuing for demonstrations, run the following generators:
* `python generate_resources.py scarce`
* `python generate_requests.py 45`