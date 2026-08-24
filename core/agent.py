import re
from api.models import CitizenRequest, TriageResult
from core.llm_classifier import classify_with_gemini

CRITICAL_KEYWORDS = {"trapped", "stuck", "chest", "drowning", "roof", "rising", "infant", "elderly"}
MEDICAL_KEYWORDS = {"bleeding", "fracture", "heart", "unconscious", "injury", "diabetic", "ambulance"}
RELIEF_KEYWORDS = {"food", "water", "ration", "kit", "drinking", "supplies"}

def has_keyword(msg_words: set, keywords: set) -> bool:
    return bool(msg_words.intersection(keywords))

def triage_request(req: CitizenRequest) -> TriageResult:
    """Hybrid triage: deterministic keyword checks with Gemini LLM fallback."""
    # Tokenize message into clean lowercase words
    msg_words = set(re.findall(r'\b\w+\b', req.message.lower()))

    # Rule 1: Medical Emergency
    if has_keyword(msg_words, MEDICAL_KEYWORDS):
        return TriageResult(
            request_id=req.id,
            citizen_name=req.citizen_name,
            zone=req.zone,
            urgency_level="P1_CRITICAL",
            category="MEDICAL",
            reasoning="Identified critical medical injury or acute condition."
        )

    # Rule 2: Entrapment / Immediate Rescue
    if has_keyword(msg_words, CRITICAL_KEYWORDS):
        return TriageResult(
            request_id=req.id,
            citizen_name=req.citizen_name,
            zone=req.zone,
            urgency_level="P1_CRITICAL",
            category="RESCUE",
            reasoning="Immediate physical danger / flood entrapment detected."
        )

    # Rule 3: Food / Water / Relief Supplies
    if has_keyword(msg_words, RELIEF_KEYWORDS):
        return TriageResult(
            request_id=req.id,
            citizen_name=req.citizen_name,
            zone=req.zone,
            urgency_level="P2_URGENT",
            category="RELIEF_SUPPLIES",
            reasoning="Relief material required, non-immediate life threat."
        )

    # Fallback: Ambiguous message handled by LLM with fail-safe error handling
    try:
        return classify_with_gemini(req)
    except Exception:
        return TriageResult(
            request_id=req.id,
            citizen_name=req.citizen_name,
            zone=req.zone,
            urgency_level="P3_INFO",
            category="GENERAL_INQUIRY",
            reasoning="Auto-triaged to standard queue due to classification timeout."
        )