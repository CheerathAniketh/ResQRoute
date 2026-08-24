from api.models import CitizenRequest, TriageResult
from core.llm_classifier import classify_with_gemini

CRITICAL_KEYWORDS = ["trapped", "stuck", "chest", "drowning", "roof", "rising", "infant", "elderly"]
MEDICAL_KEYWORDS = ["bleeding", "fracture", "heart", "unconscious", "injury", "diabetic", "ambulance"]
RELIEF_KEYWORDS = ["food", "water", "ration", "kit", "drinking"]

def triage_request(req: CitizenRequest) -> TriageResult:
    """Agentic decision logic for urgency scoring and triage categorization."""
    msg = req.message.lower()

    # Rule 1: Life-threatening medical emergency
    if any(word in msg for word in MEDICAL_KEYWORDS):
        return TriageResult(
            request_id=req.id,
            citizen_name=req.citizen_name,
            zone=req.zone,
            urgency_level="P1_CRITICAL",
            category="MEDICAL",
            reasoning="Identified critical medical injury or acute condition."
        )

    # Rule 2: Water entrapment / rescue
    if any(word in msg for word in CRITICAL_KEYWORDS):
        return TriageResult(
            request_id=req.id,
            citizen_name=req.citizen_name,
            zone=req.zone,
            urgency_level="P1_CRITICAL",
            category="RESCUE",
            reasoning="Immediate physical danger / flood entrapment detected."
        )

    # Rule 3: Food / Water supplies
    if any(word in msg for word in RELIEF_KEYWORDS):
        return TriageResult(
            request_id=req.id,
            citizen_name=req.citizen_name,
            zone=req.zone,
            urgency_level="P2_URGENT",
            category="RELIEF_SUPPLIES",
            reasoning="Relief material required, non-immediate life threat."
        )

    # Fallback: no keyword matched — genuinely ambiguous, hand off to Gemini
    return classify_with_gemini(req)