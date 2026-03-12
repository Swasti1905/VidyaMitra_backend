from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.ai_modules.skill_gap_detector import analyze_skill_gap
from app.database import get_db
from app.deps import get_current_user
from app.models.resume import Resume
from app.models.user import User
from app.schemas.skills import SkillGapRequest, SkillGapResponse


router = APIRouter(prefix="/skills", tags=["Skills"])


@router.post("/gap-analysis", response_model=SkillGapResponse)
def gap_analysis(payload: SkillGapRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    latest_resume = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
        .first()
    )
    skills = payload.current_skills or (latest_resume.extracted_skills if latest_resume else [])
    try:
        return analyze_skill_gap(payload.role, skills)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
