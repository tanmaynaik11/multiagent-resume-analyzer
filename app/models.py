from pydantic import BaseModel
from typing import List, Optional
from dateutil.parser import parse

# ========================================
# Pydantic Schemas
# ========================================

class JobEntry(BaseModel):
    job_title: str
    organization: str
    start_date: Optional[str]
    end_date: Optional[str]
    description: Optional[str]

class ResumeSections(BaseModel):
    Professional_Experience: List[JobEntry] = []
    Education: List = []
    Certifications: List = []

class MatchingInput(BaseModel):
    resume_text: str
    jd_text: str

class OrchestratorState(BaseModel):
    resume_text: str
    jd_text: str
    resume_sections: ResumeSections = ResumeSections()
    resume_skills: List[str] = []
    jd_skills: List[str] = []
    normalized_resume_skills: List[str] = []
    normalized_jd_skills: List[str] = []
    total_experience_years: Optional[float] = None
    matching_score: Optional[float] = None
    skill_gap: List[str] = []
    recruiter_instructions: Optional[str] = ""

class ResumeEntry(BaseModel):
    filename: str
    text: str

class RecruiterMatchInput(BaseModel):
    jd_text: str
    resumes: List[ResumeEntry]
    instructions: Optional[str] = ""