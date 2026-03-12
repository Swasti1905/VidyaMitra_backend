from pydantic import BaseModel, Field


class CareerRecommendationRequest(BaseModel):
    skills: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)


class CareerPath(BaseModel):
    title: str
    confidence_score: float
    required_skills: list[str]
    recommended_certifications: list[str]
    learning_roadmap: list[str]


class CareerRecommendationResponse(BaseModel):
    paths: list[CareerPath]
