from datetime import datetime

from pydantic import BaseModel, Field


class ResumeSectionData(BaseModel):
    education: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)


class ResumeAnalysisResponse(BaseModel):
    resume_id: int
    filename: str
    target_role: str | None = None
    extracted_skills: list[str]
    soft_skills: list[str]
    sections: ResumeSectionData
    created_at: datetime


class ResumeTargetRoleUpdate(BaseModel):
    target_role: str = Field(min_length=2, max_length=120)
