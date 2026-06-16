import pytest
from unittest.mock import MagicMock
from src.agents.interview_agent import InterviewAgent, InterviewQuestions, InterviewEvaluation

def test_generate_questions_empty():
    agent = InterviewAgent()
    with pytest.raises(ValueError, match="Job info cannot be empty"):
        agent.generate_questions({})

def test_evaluate_answer_empty():
    agent = InterviewAgent()
    with pytest.raises(ValueError, match="Question and answer cannot be empty"):
        agent.evaluate_answer("", "An answer")
    with pytest.raises(ValueError, match="Question and answer cannot be empty"):
        agent.evaluate_answer("A question", "")

def test_generate_questions_no_llm():
    agent = InterviewAgent()
    res = agent.generate_questions({"required_skills": ["Python"]})
    assert res == {
        "technical_questions": [],
        "behavioral_questions": []
    }

def test_evaluate_answer_no_llm():
    agent = InterviewAgent()
    res = agent.evaluate_answer("What is Python?", "A programming language.")
    assert res == {
        "score": 0,
        "feedback": ""
    }

def test_generate_questions_with_llm():
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_result = InterviewQuestions(
        technical_questions=["Explain decorators."],
        behavioral_questions=["Tell me about a time you failed."]
    )
    mock_structured.invoke.return_value = mock_result
    mock_llm.with_structured_output.return_value = mock_structured
    
    agent = InterviewAgent(llm_client=mock_llm)
    res = agent.generate_questions({"required_skills": ["Python"]})
    
    assert res["technical_questions"] == ["Explain decorators."]
    assert res["behavioral_questions"] == ["Tell me about a time you failed."]
    mock_structured.invoke.assert_called_once()

def test_evaluate_answer_with_llm():
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_result = InterviewEvaluation(
        score=85,
        feedback="Good answer, but try to provide more real-world context."
    )
    mock_structured.invoke.return_value = mock_result
    mock_llm.with_structured_output.return_value = mock_structured
    
    agent = InterviewAgent(llm_client=mock_llm)
    res = agent.evaluate_answer("What is Python?", "A programming language.")
    
    assert res["score"] == 85
    assert res["feedback"] == "Good answer, but try to provide more real-world context."
    mock_structured.invoke.assert_called_once()
