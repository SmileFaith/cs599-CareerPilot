from typing import TypedDict, Optional, Dict, Any

class CareerState(TypedDict, total=False):
    """
    State representing the CareerPilot workflow.
    total=False allows partial initialization of the state at START.
    """
    
    # Input
    resume_text: str
    job_description: str
    user_id: Optional[int]

    # Intermediate Results
    resume_info: dict
    job_info: dict
    gap_report: dict
    learning_plan: dict
    interview_questions: dict
    
    # Output / Memory Logging
    memory: dict
