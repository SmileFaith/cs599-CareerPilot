from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict

from src.agents.resume_agent import ResumeAgent
from src.agents.job_agent import JobAgent
from src.agents.gap_agent import GapAnalysisAgent
from src.agents.learning_agent import LearningAgent
from src.agents.interview_agent import InterviewAgent
from src.llm.deepseek_client import llm

app = FastAPI(title="CareerPilot API")

resume_agent = ResumeAgent(llm)
job_agent = JobAgent(llm)
gap_agent = GapAnalysisAgent(llm)
learning_agent = LearningAgent(llm)
interview_agent = InterviewAgent(llm)

class StandardResponse(BaseModel):
    success: bool
    data: Dict[str, Any] = Field(default_factory=dict)
    message: str = ""

class ResumeRequest(BaseModel):
    text: str

class JobRequest(BaseModel):
    description: str

class GapRequest(BaseModel):
    resume_info: Dict[str, Any]
    job_info: Dict[str, Any]

class LearningPlanRequest(BaseModel):
    gap_report: Dict[str, Any]

class InterviewRequest(BaseModel):
    job_info: Dict[str, Any]

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/analyze-resume", response_model=StandardResponse)
def analyze_resume(req: ResumeRequest):
    try:
        data = resume_agent.process(req.text)
        return StandardResponse(success=True, data=data, message="Resume analyzed successfully.")
    except Exception as e:
        return StandardResponse(success=False, data={}, message=str(e))

@app.post("/analyze-job", response_model=StandardResponse)
def analyze_job(req: JobRequest):
    try:
        data = job_agent.process(req.description)
        return StandardResponse(success=True, data=data, message="Job description analyzed successfully.")
    except Exception as e:
        return StandardResponse(success=False, data={}, message=str(e))

@app.post("/gap-analysis", response_model=StandardResponse)
def gap_analysis(req: GapRequest):
    try:
        data = gap_agent.process(req.resume_info, req.job_info)
        return StandardResponse(success=True, data=data, message="Gap analysis completed successfully.")
    except Exception as e:
        return StandardResponse(success=False, data={}, message=str(e))

@app.post("/learning-plan", response_model=StandardResponse)
def learning_plan(req: LearningPlanRequest):
    try:
        data = learning_agent.process(req.gap_report)
        return StandardResponse(success=True, data=data, message="Learning plan generated successfully.")
    except Exception as e:
        return StandardResponse(success=False, data={}, message=str(e))

@app.post("/interview", response_model=StandardResponse)
def generate_interview(req: InterviewRequest):
    try:
        data = interview_agent.generate_questions(req.job_info)
        return StandardResponse(success=True, data=data, message="Interview questions generated successfully.")
    except Exception as e:
        return StandardResponse(success=False, data={}, message=str(e))
