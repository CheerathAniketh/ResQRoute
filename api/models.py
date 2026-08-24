from pydantic import BaseModel
from typing import Optional

class CitizenRequest(BaseModel):
    id: str
    citizen_name: str
    zone: str
    message: str

class TriageResult(BaseModel):
    request_id: str
    citizen_name: str
    zone: str
    urgency_level: str  # P1_CRITICAL, P2_URGENT, P3_INFO
    category: str       # RESCUE, MEDICAL, RELIEF_SUPPLIES, GENERAL_INQUIRY
    reasoning: str

class ResourceAllocation(BaseModel):
    request_id: str
    urgency_level: str
    assigned_resource_id: Optional[str]
    resource_type: Optional[str]
    status: str