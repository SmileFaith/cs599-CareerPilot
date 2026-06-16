import pytest
from unittest.mock import MagicMock
from src.agents.gap_agent import GapAnalysisAgent, GapInfo

def test_gap_agent_empty_inputs():
    agent = GapAnalysisAgent()
    with pytest.raises(ValueError, match="Input info cannot be entirely empty"):
        agent.process({}, {})

def test_gap_agent_no_llm():
    agent = GapAnalysisAgent()
    res = agent.process({"skills": ["Python"]}, {"required_skills": ["Python"]})
    assert res == {
        "matched_skills": [],
        "missing_skills": [],
        "score": 0
    }

def test_gap_agent_with_llm():
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_result = GapInfo(
        matched_skills=["Python", "FastAPI"],
        missing_skills=["Docker"],
        score=85
    )
    mock_structured.invoke.return_value = mock_result
    mock_llm.with_structured_output.return_value = mock_structured
    
    agent = GapAnalysisAgent(llm_client=mock_llm)
    resume_info = {"skills": ["Python", "FastAPI", "SQL"]}
    job_info = {"required_skills": ["Python", "FastAPI", "Docker"]}
    
    res = agent.process(resume_info, job_info)
    
    assert res["matched_skills"] == ["Python", "FastAPI"]
    assert res["missing_skills"] == ["Docker"]
    assert res["score"] == 85
    mock_structured.invoke.assert_called_once()
