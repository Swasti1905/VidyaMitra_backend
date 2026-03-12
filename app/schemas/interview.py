from pydantic import BaseModel, Field


class InterviewStartRequest(BaseModel):
    role: str = Field(min_length=2, max_length=120)


class InterviewQuestion(BaseModel):
    id: int
    prompt: str
    focus_area: str


class InterviewStartResponse(BaseModel):
    session_id: int
    role: str
    questions: list[InterviewQuestion]


class InterviewAnswerRequest(BaseModel):
    session_id: int
    question_id: int
    answer: str = Field(min_length=20)


class InterviewFeedbackResponse(BaseModel):
    session_id: int
    confidence: float
    clarity: float
    relevance: float
    communication: float
    strengths: list[str]
    weaknesses: list[str]
    improvement_suggestions: list[str]
