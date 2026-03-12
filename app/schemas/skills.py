from pydantic import BaseModel, Field


class SkillGapRequest(BaseModel):
    role: str = Field(min_length=2, max_length=120)
    current_skills: list[str] = Field(default_factory=list)


class SkillGapResponse(BaseModel):
    role: str
    matched_skills: list[str]
    missing_skills: list[str]
    recommended_topics: list[str]
    improvement_suggestions: list[str]
    readiness_score: float
