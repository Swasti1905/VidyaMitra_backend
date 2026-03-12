from pydantic import BaseModel


class LearningResource(BaseModel):
    title: str
    difficulty: str
    estimated_learning_time: str
    provider: str
    focus_skills: list[str]


class LearningRecommendationResponse(BaseModel):
    target_role: str
    resources: list[LearningResource]
