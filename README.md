# 🚨 ResQRoute

**AI-assisted disaster resource triage & allocation**
Team **Akaza** — Ideathon Submission (Theme: Crisis Management)

---

## The Problem

When a disaster hits a city — a flood, earthquake, or war — citizens flood government
helplines with calls, SMS, and messages asking for help. A human operator has to
manually read every request, decide who needs help most, and figure out what
resource (boat, ambulance, food) to send where. Under real disaster load, this
breaks down: requests come in faster than they can be triaged, and there's no
guarantee the most critical cases get resources first.

**ResQRoute** is the missing layer between "citizen sent a request" and
"resource dispatched" — it takes structured requests (already logged by an
operator, via SMS/call-center/app — that intake layer is intentionally out of
scope) and a live resource inventory, and automatically:

1. **Triages** every request by urgency and category
2. **Allocates** available resources to the highest-priority requests first
3. **Shows** the result on a live dashboard — what got dispatched, what's still
   queued, and why

---

## Why No LLM / No Agent Framework

We deliberately built ResQRoute on **deterministic, rule-based logic** instead
of an LLM or LangGraph agent:

- **Explainable** — every triage decision has a plain-English reason a judge,
  operator, or auditor can verify instantly
- **Reliable** — no risk of hallucination or API failure during a live disaster
  or a live demo
- **Fast** — instant response, no inference latency

In a system that decides who gets a rescue boat first, predictability and
auditability matter more than novelty for novelty's sake.

---

## How It Works (Workflow)

```
┌─────────────────┐     ┌──────────────┐     ┌───────────────────┐     ┌───────────────┐
│  Citizen         │     │  Operator    │     │   ResQRoute        │     │   Dashboard    │
│  Requests        │────▶│  logs into   │────▶│                    │────▶│                │
│  (out of scope — │     │  CSV/JSON    │     │  1. Triage         │     │  Live table:   │
│  call/SMS/app)   │     │              │     │  2. Allocate       │     │  priority,     │
└─────────────────┘     └──────────────┘     │  3. Rank & Queue   │     │  status,       │
                                              └───────────────────┘     │  resource      │
                                                                          └───────────────┘
```

1. **Input**: Operator uploads a CSV of requests (`id, citizen_name, zone, message`)
   or triggers the built-in demo dataset.
2. **Weather check**: The system pulls current flood/rainfall risk for the city
   (`core/weather.py`) to contextualize the situation.
3. **Triage** (`core/agent.py`): Each request's free-text `message` is classified into:
   - **Category**: `RESCUE`, `MEDICAL`, `RELIEF_SUPPLIES`, or `GENERAL_INQUIRY`
   - **Urgency**: `P1_CRITICAL`, `P2_URGENT`, or `P3_INFO`
4. **Allocation** (`core/allocator.py`): Requests are sorted P1 → P2 → P3. For
   each, the system looks for a matching, available, zone-appropriate resource
   (rescue boat, ambulance, food/water kit) and dispatches it. If nothing's
   available, the request is marked `QUEUED` (or `RESOLVED_AUTO` for routine
   info queries that don't need a physical resource).
5. **Output**: The dashboard shows every request, its priority, category,
   reasoning, assigned resource (if any), and final status — color-coded by
   urgency.

---

## Tech Stack

- **Backend**: FastAPI (Python)
- **Logic**: Plain Python — no ML model, no LangGraph, no external agent framework
- **Frontend**: Single-page vanilla HTML/JS dashboard (no build step, no framework)
- **Data**: JSON/CSV for requests and resources (swappable for a real DB later)

---

## Project Structure

```
Akaza/
├── api/
│   ├── models.py       # Pydantic schemas (CitizenRequest, TriageResult, ResourceAllocation)
│   └── routes.py       # /weather-risk, /triage-and-allocate, /demo-run, /upload-requests-csv
├── core/
│   ├── agent.py        # Triage logic — classifies urgency & category
│   ├── allocator.py     # Resource matching & dispatch logic
│   └── weather.py       # Flood/rainfall risk check
├── data/
│   ├── mock_resources.json     # Resource inventory
│   └── sample_requests.json    # Fixed demo dataset
├── static/
│   └── dashboard.html   # Live dashboard UI
├── generate_requests.py    # Synthetic request CSV generator
├── generate_resources.py   # Synthetic resource pool generator
├── app.py               # FastAPI app entrypoint
└── requirements.txt
```

---

## Setup & Run

```bash
# 1. Activate environment
cd Akaza
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
pip install python-multipart   # needed for CSV file uploads

# 3. Run the server
uvicorn app:app --reload
```

Open **http://127.0.0.1:8000/** — the dashboard loads there.

---

## Demo Script (2 Acts)

### Act 1 — Normal Load (proves the core loop works)

```bash
python generate_resources.py balanced
python generate_requests.py 10
```

Upload the generated CSV via the dashboard, or click **Run Live Demo** for the
fixed dataset. Expect most/all requests to be `DISPATCHED` cleanly.

**Say:** *"Here's a normal day — requests come in, get triaged, and get the
right resource, instantly."*

### Act 2 — Mass-Casualty Stress Test (proves it holds up under real disaster load)

```bash
python generate_resources.py scarce
python generate_requests.py 45
```

Upload the new CSV. Now resources are far outnumbered by requests — expect
many `QUEUED` results.

**Say:** *"This is what happens when a real disaster hits and resources are
overwhelmed. Watch — every P1 still stays ahead of every P2 and P3. Nothing
gets assigned out of order, nothing is random. This is the difference between
a helpline drowning in unsorted calls and one that knows exactly who to help
first."*

---

## Generating Fresh Demo Data

```bash
# Requests: change the count for a bigger/smaller wave
python generate_requests.py <count> [output_path]

# Resources: choose a scenario
python generate_resources.py scarce     # stress-test: 1 of each resource per zone
python generate_resources.py balanced   # normal load: 2-3 of each per zone
python generate_resources.py abundant   # well-funded city: 3-6 of each per zone
```

Both scripts randomize output, so re-running mid-pitch (e.g. if a judge asks
"show me with different data") produces a fresh, live result every time.

---

## API Endpoints

| Method | Endpoint                  | Description                                      |
|--------|---------------------------|---------------------------------------------------|
| GET    | `/api/weather-risk`       | Current flood/rainfall risk for a city             |
| GET    | `/api/demo-run`           | Runs triage + allocation on the fixed sample dataset |
| POST   | `/api/triage-and-allocate`| Accepts a JSON list of requests, returns results   |
| POST   | `/api/upload-requests-csv`| Accepts a CSV upload, returns triage + allocation  |
| GET    | `/`                       | Live dashboard UI                                  |

**CSV format** (`/api/upload-requests-csv`):
```csv
id,citizen_name,zone,message
REQ-201,Lakshmi,Zone-A,Roof collapsed, family of 3 trapped inside
```

---

## Impact & Scalability

- **Generalizes** to any city, any disaster type (flood, earthquake, fire, war) —
  only the weather-risk module is city-specific; triage/allocation logic is
  disaster-agnostic
- **Plugs into existing infrastructure** — designed to sit behind whatever
  intake channel a government already uses (100/emergency helplines, SMS
  gateways, disaster-relief apps) rather than replacing them
- **Scales resource types** — new categories (shelter beds, generators,
  medical teams) can be added to the allocator without touching the triage
  logic
- **Honest under scarcity** — rather than silently failing or randomly
  assigning, the system surfaces exactly which requests couldn't be served,
  giving authorities real signal on where to deploy more resources

---

## What's Explicitly Out of Scope (by design)

- How requests are collected from citizens (call center, SMS, app — assumed
  to already exist and feed into ResQRoute as structured data)
- Persistent database / multi-session state (kept in-memory for this demo;
  swappable for Postgres/Supabase in production)
- Authentication / multi-operator concurrency

These were deliberately scoped out to keep the core allocation problem — the
actual hard part — sharp and demonstrable within an ideathon timeline.

---

**Team Akaza**