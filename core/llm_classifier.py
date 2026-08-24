import json
import httpx
from core.config import GEMINI_API_KEY, GEMINI_MODEL
from api.models import CitizenRequest, TriageResult

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

PROMPT_TEMPLATE = """You are a disaster triage classifier. Classify the citizen request below.

Message: "{message}"

Respond with ONLY a JSON object, no markdown, no explanation, in exactly this shape:
{{"urgency_level": "P1_CRITICAL" | "P2_URGENT" | "P3_INFO", "category": "RESCUE" | "MEDICAL" | "RELIEF_SUPPLIES" | "GENERAL_INQUIRY", "reasoning": "<one short sentence>"}}
"""

VALID_URGENCY = {"P1_CRITICAL", "P2_URGENT", "P3_INFO"}
VALID_CATEGORY = {"RESCUE", "MEDICAL", "RELIEF_SUPPLIES", "GENERAL_INQUIRY"}


def _fallback_result(req: CitizenRequest, reason: str) -> TriageResult:
    """Safe default if Gemini is unavailable or returns something unusable —
    this is what keeps a flaky API from ever breaking the live demo."""
    return TriageResult(
        request_id=req.id,
        citizen_name=req.citizen_name,
        zone=req.zone,
        urgency_level="P2_URGENT",
        category="GENERAL_INQUIRY",
        reasoning=f"Needs manual review — {reason}",
    )


def classify_with_gemini(req: CitizenRequest, timeout: float = 4.0) -> TriageResult:
    if not GEMINI_API_KEY:
        return _fallback_result(req, "no Gemini API key configured")

    url = GEMINI_URL.format(model=GEMINI_MODEL)
    payload = {
        "contents": [{"parts": [{"text": PROMPT_TEMPLATE.format(message=req.message)}]}],
        "generationConfig": {"temperature": 0, "response_mime_type": "application/json"},
    }

    try:
        resp = httpx.post(url, params={"key": GEMINI_API_KEY}, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        parsed = json.loads(text)

        urgency = parsed.get("urgency_level")
        category = parsed.get("category")
        reasoning = parsed.get("reasoning", "Classified by Gemini.")

        if urgency not in VALID_URGENCY or category not in VALID_CATEGORY:
            return _fallback_result(req, "Gemini returned an unexpected label")

        return TriageResult(
            request_id=req.id,
            citizen_name=req.citizen_name,
            zone=req.zone,
            urgency_level=urgency,
            category=category,
            reasoning=f"[Gemini] {reasoning}",
        )

    except (httpx.HTTPError, KeyError, IndexError, json.JSONDecodeError, TypeError):
        return _fallback_result(req, "Gemini call failed or returned malformed output")