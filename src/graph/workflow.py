import logging
from typing import Any
from langgraph.graph import StateGraph, START, END

from src.graph.state import CareerState
from src.agents.resume_agent import ResumeAgent
from src.agents.job_agent import JobAgent
from src.agents.gap_agent import GapAnalysisAgent
from src.agents.learning_agent import LearningAgent
from src.agents.interview_agent import InterviewAgent
from src.memory.repository import MemoryRepository

logger = logging.getLogger(__name__)

def create_career_graph(llm_client: Any = None, db_path: str = "memory.db"):
    """
    Creates and compiles the LangGraph workflow for the CareerPilot system.
    
    Args:
        llm_client: LLM client (e.g. LangChain ChatModel) with structured output support.
        db_path: Path to the SQLite memory database.
        
    Returns:
        A compiled LangGraph application.
    """
    # 1. Initialize dependencies
    resume_agent = ResumeAgent(llm_client=llm_client)
    job_agent = JobAgent(llm_client=llm_client)
    gap_agent = GapAnalysisAgent(llm_client=llm_client)
    learning_agent = LearningAgent(llm_client=llm_client)
    interview_agent = InterviewAgent(llm_client=llm_client)
    
    repo = MemoryRepository(db_path=db_path)

    # 2. Define Node Functions
    def process_resume(state: CareerState):
        logger.info("Node: process_resume")
        resume_text = state.get("resume_text", "")
        # If no resume text, we pass empty text, but ResumeAgent expects something or fails, 
        # let's assume it's validated earlier, but fallback to " " to avoid error if perfectly empty.
        resume_info = resume_agent.process(resume_text if resume_text.strip() else "Empty Resume")
        return {"resume_info": resume_info}

    def process_job(state: CareerState):
        logger.info("Node: process_job")
        job_desc = state.get("job_description", "")
        job_info = job_agent.process(job_desc if job_desc.strip() else "Empty JD")
        return {"job_info": job_info}

    def analyze_gap(state: CareerState):
        logger.info("Node: analyze_gap")
        resume_info = state.get("resume_info", {})
        job_info = state.get("job_info", {})
        
        # Protect against completely empty info causing ValueError
        if not resume_info and not job_info:
            resume_info = {"skills": []}
            job_info = {"required_skills": []}
            
        gap_report = gap_agent.process(resume_info, job_info)
        return {"gap_report": gap_report}

    def generate_learning_plan(state: CareerState):
        logger.info("Node: generate_learning_plan")
        gap_report = state.get("gap_report", {})
        plan = learning_agent.process(gap_report)
        return {"learning_plan": plan}

    def generate_interview(state: CareerState):
        logger.info("Node: generate_interview")
        job_info = state.get("job_info", {})
        
        if not job_info:
            job_info = {"required_skills": []}
            
        questions = interview_agent.generate_questions(job_info)
        return {"interview_questions": questions}

    def save_memory(state: CareerState):
        logger.info("Node: save_memory")
        user_id = state.get("user_id")
        
        # If no user_id is provided, create a placeholder user session
        if not user_id:
            user_id = repo.create_user("Anonymous User")

        # Save missing skills as "pending" progress in the database
        gap_report = state.get("gap_report", {})
        missing_skills = gap_report.get("missing_skills", [])
        
        for skill in missing_skills:
            repo.save_user_progress(user_id, skill, "pending")
            
        score = gap_report.get("score", 0)
        
        return {
            "memory": {
                "status": "saved", 
                "user_id": user_id, 
                "saved_skills": missing_skills,
                "score_noted": score
            }
        }

    # 3. Build Graph
    workflow = StateGraph(CareerState)

    workflow.add_node("ResumeAgent", process_resume)
    workflow.add_node("JobAgent", process_job)
    workflow.add_node("GapAnalysisAgent", analyze_gap)
    workflow.add_node("LearningAgent", generate_learning_plan)
    workflow.add_node("InterviewAgent", generate_interview)
    workflow.add_node("SaveMemory", save_memory)

    # 4. Define Workflow Edges
    workflow.add_edge(START, "ResumeAgent")
    workflow.add_edge("ResumeAgent", "JobAgent")
    workflow.add_edge("JobAgent", "GapAnalysisAgent")
    workflow.add_edge("GapAnalysisAgent", "LearningAgent")
    workflow.add_edge("LearningAgent", "InterviewAgent")
    workflow.add_edge("InterviewAgent", "SaveMemory")
    workflow.add_edge("SaveMemory", END)

    return workflow.compile()
