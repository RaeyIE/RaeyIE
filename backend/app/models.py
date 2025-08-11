from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field


class KeyResult(BaseModel):
    title: str = Field(..., description="Key Result title")
    metric: Optional[str] = Field(None, description="Metric being measured, e.g., conversion_rate")
    target: Optional[Union[float, int, str]] = Field(
        None, description="Target value for the metric, numeric or descriptive"
    )


class Objective(BaseModel):
    title: str
    description: Optional[str] = None
    key_results: List[KeyResult] = Field(default_factory=list)


class SuggestionRequest(BaseModel):
    org: Optional[str] = None
    team: Optional[str] = None
    role: Optional[str] = None
    period: Optional[str] = Field(None, description="e.g., Q1 2025")
    context: Optional[str] = Field(
        None, description="Freeform context about strategy, initiatives, or constraints"
    )
    previous_okrs: Optional[List[str]] = Field(
        None, description="Optional plain-text summaries of prior OKRs"
    )


class SuggestionResponse(BaseModel):
    objectives: List[Objective]


class ChatRequest(BaseModel):
    message: str
    metrics: Optional[Dict[str, Union[float, int, str]]] = None
    persona: Optional[str] = Field(
        None, description="e.g., 'coach', 'checker', 'nudger'"
    )


class ChatResponse(BaseModel):
    reply: str