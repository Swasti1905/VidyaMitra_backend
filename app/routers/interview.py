from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.ai_modules.interview_analyzer import analyze_answer, generate_questions
from app.database import get_db
from app.deps import get_current_user
from app.models.interview import InterviewSession
from app.models.user import User
from app.schemas.interview import (
    InterviewAnswerRequest,
    InterviewFeedbackResponse,
    InterviewQuestion,
    InterviewStartRequest,
    InterviewStartResponse,
)


router = APIRouter(prefix="/interview", tags=["Interview"])


@router.post("/start", response_model=InterviewStartResponse)
def start_interview(payload: InterviewStartRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    questions = generate_questions(payload.role)
    session = InterviewSession(user_id=current_user.id, role=payload.role, questions=questions, answers=[], feedback={})
    db.add(session)
    db.commit()
    db.refresh(session)
    return InterviewStartResponse(
        session_id=session.id,
        role=session.role,
        questions=[InterviewQuestion(**question) for question in session.questions],
    )


@router.post("/submit-answer", response_model=InterviewFeedbackResponse)
def submit_answer(payload: InterviewAnswerRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = db.get(InterviewSession, payload.session_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")

    question = next((item for item in session.questions if item["id"] == payload.question_id), None)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found in this session")

    feedback = analyze_answer(session.role, question["prompt"], payload.answer)
    answers = session.answers or []
    answers.append({"question_id": payload.question_id, "answer": payload.answer})
    session.answers = answers
    session.feedback = feedback
    db.commit()
    db.refresh(session)
    return InterviewFeedbackResponse(session_id=session.id, **feedback)
