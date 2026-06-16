import logging
from typing import List, Dict, Any
from pydantic import BaseModel, Field
import json

logger = logging.getLogger(__name__)

class JobInfo(BaseModel):
    """Structured job information extracted from text."""
    required_skills: List[str] = Field(default_factory=list, description="List of strongly required skills")
    preferred_skills: List[str] = Field(default_factory=list, description="List of preferred, nice-to-have, or bonus skills")
    experience_level: str = Field(default="", description="Required experience level (e.g., '1-3 years', 'Senior', 'Entry level')")


class JobAgent:
    """Agent responsible for analyzing job descriptions and extracting requirements."""
    
    def __init__(self, llm_client: Any = None):
        """
        Initialize the JobAgent.
        
        Args:
            llm_client: An LLM client instance (e.g., LangChain ChatOpenAI configured for DeepSeek API)
                        that supports with_structured_output.
        """
        self.llm_client = llm_client

    def process(self, job_description: str) -> Dict[str, Any]:
        """
        Process the job description text and extract structured requirements.
        
        Args:
            job_description: Raw job description text.
            
        Returns:
            A dictionary containing required_skills, preferred_skills, and experience_level.
        """
        if not job_description or not job_description.strip():
            logger.error("Empty job description provided")
            raise ValueError("Job description cannot be empty")

        if self.llm_client is None:
            logger.warning("No LLM client provided. Returning empty output.")
            return JobInfo().model_dump()
            
        try:
            logger.info("Extracting structured information from JD via DeepSeek LLM.")
            # Note: The llm_client should be instantiated with DeepSeek API URL and Key beforehand

            # structured_llm = self.llm_client.with_structured_output(JobInfo)
            #
            prompt = (
                # "你是一位专业的HR和技术招聘专家。"
                # "请从下面岗位描述中提取信息。"
                # "只返回JSON，格式为："
                # "required_skills (list of strings), preferred_skills (list of strings), and experience_level (string). "
                # "Extract strictly based on the text.\n\n"
                # f"Job Description:\n{job_description}"
                f"""
            你是专业HR和技术招聘专家。
            请从下面岗位描述中提取信息。
            只返回JSON。
            格式：
            {{
                "必备技能": [],
                "加分技能": [],
                "经验要求": ""
            }}
            岗位描述：
            {job_description}
            """
            )
            #
            # result: JobInfo = structured_llm.invoke(prompt)
            # return result.model_dump()
            response = self.llm_client.invoke(prompt)
            data = json.loads(response.content)
            return data

            # print(response.content)

            # return {
            #     "required_skills": [response.content],
            #     "preferred_skills": [],
            #     "experience_level": ""
            # }
            
        except Exception as e:
            logger.error(f"Error during job analysis extraction: {e}")
            raise
