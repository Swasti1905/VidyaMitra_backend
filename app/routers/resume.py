from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models.resume import Resume
from app.models.user import User
from app.schemas.resume import ResumeAnalysisResponse, ResumeSectionData, ResumeTargetRoleUpdate
from app.services.resume_service import process_resume_upload


router = APIRouter(prefix="/resume", tags=["Resume"])


def _serialize_resume(resume: Resume) -> ResumeAnalysisResponse:
    return ResumeAnalysisResponse(
        resume_id=resume.id,
        filename=resume.filename,
        target_role=resume.target_role,
        extracted_skills=resume.extracted_skills,
        soft_skills=resume.soft_skills,
        sections=ResumeSectionData(**resume.sections),
        created_at=resume.created_at,
    )


@router.post("/upload", response_model=ResumeAnalysisResponse)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume = process_resume_upload(db, current_user, file)
    return _serialize_resume(resume)


@router.get("/analyze", response_model=ResumeAnalysisResponse)
def analyze_latest_resume(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    resume = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
        .first()
    )
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No resume found for this user")
    return _serialize_resume(resume)


@router.patch("/target-role", response_model=ResumeAnalysisResponse)
def update_target_role(
    payload: ResumeTargetRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
        .first()
    )
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No resume found for this user")
    resume.target_role = payload.target_role
    db.commit()
    db.refresh(resume)
    return _serialize_resume(resume)
