from fastapi import APIRouter, Depends

from app.ai_modules.datasets import load_learning_resources
from app.ai_modules.skill_gap_detector import analyze_skill_gap
from app.deps import get_current_user
from app.models.user import User
from app.schemas.learning import LearningRecommendationResponse, LearningResource
from app.schemas.skills import SkillGapRequest


router = APIRouter(prefix="/learning", tags=["Learning"])


@router.post("/recommendations", response_model=LearningRecommendationResponse)
def get_learning_recommendations(payload: SkillGapRequest, current_user: User = Depends(get_current_user)):
    analysis = analyze_skill_gap(payload.role, payload.current_skills)
    missing_skills = {skill.lower() for skill in analysis["missing_skills"]}
    resources = []
    for resource in load_learning_resources():
        if missing_skills.intersection(skill.lower() for skill in resource["focus_skills"]):
            resources.append(LearningResource(**resource))

    if not resources:
        resources = [LearningResource(**resource) for resource in load_learning_resources()[:3]]

    return LearningRecommendationResponse(target_role=payload.role, resources=resources)
