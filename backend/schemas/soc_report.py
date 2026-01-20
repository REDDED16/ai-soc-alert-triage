from pydantic import BaseModel
from typing import List, Literal


class SOCAlertReport(BaseModel):
    threat_type: str
    mitre_technique: str
    severity: Literal["Low", "Medium", "High", "Critical"]
    indicators: List[str]
    impact_summary: str
    mitigation_steps: List[str]
