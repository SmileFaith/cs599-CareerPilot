import pytest
from unittest.mock import MagicMock
from src.agents.job_agent import JobAgent, JobInfo
from src.tools.skill_extractor import SkillExtractorTool, SkillList

def test_job_agent_empty_text():
    agent = JobAgent()
    with pytest.raises(ValueError, match="Job description cannot be empty"):
        agent.process("")

def test_job_agent_no_llm():
    agent = JobAgent()
    res = agent.process("Software Engineer at ExampleCorp")
    assert res == {
        "required_skills": [],
        "preferred_skills": [],
        "experience_level": ""
    }

def test_job_agent_with_llm():
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_result = JobInfo(
        required_skills=["Python", "FastAPI"],
        preferred_skills=["Docker", "Kubernetes"],
        experience_level="3-5 years"
    )
    mock_structured.invoke.return_value = mock_result
    mock_llm.with_structured_output.return_value = mock_structured
    
    agent = JobAgent(llm_client=mock_llm)
    jd = "We are looking for a Python dev with FastAPI experience. Docker is a plus. 3-5 years exp."
    res = agent.process(jd)
    
    assert res["required_skills"] == ["Python", "FastAPI"]
    assert res["preferred_skills"] == ["Docker", "Kubernetes"]
    assert res["experience_level"] == "3-5 years"
    mock_structured.invoke.assert_called_once()

def test_skill_extractor_empty_text():
    mock_llm = MagicMock()
    tool = SkillExtractorTool(llm_client=mock_llm)
    with pytest.raises(ValueError, match="Input text cannot be empty"):
        tool.extract_skills("  ")

def test_skill_extractor_success():
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_result = SkillList(skills=["Java", "Spring Boot"])
    
    mock_structured.invoke.return_value = mock_result
    mock_llm.with_structured_output.return_value = mock_structured
    
    tool = SkillExtractorTool(llm_client=mock_llm)
    skills = tool.extract_skills("I know Java and Spring Boot.")
    
    assert skills == ["Java", "Spring Boot"]
    mock_structured.invoke.assert_called_once()
