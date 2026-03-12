from fastapi import APIRouter, Depends

from app.ai_modules.career_recommender import recommend_careers
from app.deps import get_current_user
from app.models.user import User
from app.schemas.career import CareerRecommendationRequest, CareerRecommendationResponse


router = APIRouter(prefix="/career", tags=["Career"])


@router.post("/recommendation", response_model=CareerRecommendationResponse)
def get_career_recommendations(payload: CareerRecommendationRequest, current_user: User = Depends(get_current_user)):
    return recommend_careers(payload.skills, payload.interests)
