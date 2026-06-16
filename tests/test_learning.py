import pytest
from unittest.mock import MagicMock
from src.agents.learning_agent import LearningAgent, LearningPlan

def test_learning_agent_empty_inputs():
    agent = LearningAgent()
    with pytest.raises(ValueError, match="Gap report must be a non-empty dictionary"):
        agent.process({})

def test_learning_agent_no_missing_skills():
    agent = LearningAgent()
    # A dictionary with missing_skills empty should return early with empty plan
    res = agent.process({"missing_skills": [], "matched_skills": ["Python"], "score": 100})
    assert res == {
        "learning_sequence": [],
        "weekly_roadmap": {},
        "recommended_projects": []
    }

def test_learning_agent_no_llm():
    agent = LearningAgent()
    # When missing_skills are present but no LLM client is given, we just get the empty default template
    res = agent.process({"missing_skills": ["Docker", "Kubernetes"]})
    assert res == {
        "learning_sequence": [],
        "weekly_roadmap": {},
        "recommended_projects": []
    }

def test_learning_agent_with_llm():
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_result = LearningPlan(
        learning_sequence=["Docker basics", "Kubernetes basics"],
        weekly_roadmap={"week1": ["Learn Docker containers"], "week2": ["Learn K8s Pods"]},
        recommended_projects=["Build a containerized Python app deployments"]
    )
    mock_structured.invoke.return_value = mock_result
    mock_llm.with_structured_output.return_value = mock_structured
    
    agent = LearningAgent(llm_client=mock_llm)
    gap_report = {"missing_skills": ["Docker", "Kubernetes"], "score": 60}
    
    res = agent.process(gap_report)
    
    assert res["learning_sequence"] == ["Docker basics", "Kubernetes basics"]
    assert res["weekly_roadmap"] == {"week1": ["Learn Docker containers"], "week2": ["Learn K8s Pods"]}
    assert res["recommended_projects"] == ["Build a containerized Python app deployments"]
    mock_structured.invoke.assert_called_once()
