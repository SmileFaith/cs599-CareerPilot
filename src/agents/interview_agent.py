import logging
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from src.utils.json_parser import extract_json

logger = logging.getLogger(__name__)

class InterviewQuestions(BaseModel):
    """Structured output for interview questions generation."""
    technical_questions: List[str] = Field(default_factory=list, description="List of technical interview questions")
    behavioral_questions: List[str] = Field(default_factory=list, description="List of behavioral interview questions")


class InterviewEvaluation(BaseModel):
    """Structured output for interview answer evaluation."""
    score: int = Field(default=0, ge=0, le=100, description="Evaluation score from 0 to 100")
    feedback: str = Field(default="", description="Constructive feedback based on the candidate's answer")


class InterviewAgent:
    """Agent responsible for generating interview questions and evaluating candidate answers."""
    
    def __init__(self, llm_client: Any = None):
        """
        Initialize the InterviewAgent.
        
        Args:
            llm_client: An LLM client instance supporting structured output.
        """
        self.llm_client = llm_client

    def generate_questions(self, job_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate technical and behavioral interview questions based on job requirements.
        
        Args:
            job_info: Dictionary containing extracted job requirements.
            
        Returns:
            A dictionary containing lists of technical and behavioral questions.
        """
        if not job_info:
            logger.error("Job info is empty")
            raise ValueError("Job info cannot be empty")
            
        if self.llm_client is None:
            logger.warning("No LLM client provided. Returning empty questions.")
            return InterviewQuestions().model_dump()
            
        try:
            logger.info("Generating interview questions via LLM.")
            # structured_llm = self.llm_client.with_structured_output(InterviewQuestions)
            
            # prompt = (
            #     "You are an expert technical interviewer. "
            #     "Based on the following job requirements, generate appropriate technical and behavioral "
            #     "interview questions for a candidate.\n\n"
            #     f"Job Info:\n{job_info}"
            # )
            prompt = f"""
            你是高级技术面试官。
            根据岗位要求生成面试题。
            只返回JSON。
            格式：
            {{
                "technical_questions": [],
                "behavioral_questions": []
            }}
            岗位信息：
            {job_info}
            """
            
            # result: InterviewQuestions = structured_llm.invoke(prompt)
            # return result.model_dump()
            response = self.llm_client.invoke(prompt)

            return extract_json(response.content)
            
        except Exception as e:
            logger.error(f"Error during question generation: {e}")
            raise

    def evaluate_answer(self, question: str, answer: str) -> Dict[str, Any]:
        """
        Evaluate a candidate's answer to an interview question.
        
        Args:
            question: The interview question asked.
            answer: The candidate's answer.
            
        Returns:
            A dictionary containing a score (0-100) and constructive feedback.
        """
        if not question or not answer:
            logger.error("Question or answer is missing")
            raise ValueError("Question and answer cannot be empty")
            
        if self.llm_client is None:
            logger.warning("No LLM client provided. Returning default evaluation.")
            return InterviewEvaluation().model_dump()
            
        try:
            logger.info("Evaluating interview answer via LLM.")
            # structured_llm = self.llm_client.with_structured_output(InterviewEvaluation)
            
            # prompt = (
            #     "You are an expert technical interviewer. "
            #     "Evaluate the candidate's answer to the interview question. "
            #     "Provide a match score from 0 to 100 representing how correct, comprehensive, and clear the answer is. "
            #     "Also provide constructive feedback on how to improve the answer.\n\n"
            #     f"Question:\n{question}\n\n"
            #     f"Candidate Answer:\n{answer}"
            # )
            prompt = f"""
            你是高级技术面试官。
            评估候选人回答。
            评分要求：
            1. 满分100分
            2. 最低0分
            3. 只允许返回整数
            4. 综合考虑：
               - 技术正确性（40分）
               - 完整性（30分）
               - 表达清晰度（20分）
               - 工程实践意识（10分）
            只返回JSON。
            格式：
            {{
                "score": 0,
                "feedback": ""
            }}
            问题：
            {question}
            回答：
            {answer}
            """

            # result: InterviewEvaluation = structured_llm.invoke(prompt)
            # return result.model_dump()
            response = self.llm_client.invoke(prompt)

            return extract_json(response.content)
            
        except Exception as e:
            logger.error(f"Error during answer evaluation: {e}")
            raise
