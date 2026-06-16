import pytest
from src.graph.workflow import create_career_graph


def test_workflow_execution():
    """
    Test compiling and executing the LangGraph structured workflow smoothly.
    With LLM client as None, agents will yield default dictionaries.
    """
    app = create_career_graph(llm_client=None, db_path=":memory:")
    
    initial_state = {
        "resume_text": "Python Developer with 5 years experience.",
        "job_description": "We need someone very good at Java.",
        "user_id": 100
    }
    
    final_state = app.invoke(initial_state)
    
    # Assert nodes populated the state
    assert "resume_info" in final_state
    assert "job_info" in final_state
    assert "gap_report" in final_state
    assert "learning_plan" in final_state
    assert "interview_questions" in final_state
    assert "memory" in final_state
    
    # Check memory output
    memory_result = final_state["memory"]
    assert memory_result["status"] == "saved"
    # Ensure it utilized the provided specific user_id
    assert memory_result["user_id"] == 100
