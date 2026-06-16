import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from src.utils.json_parser import extract_json

logger = logging.getLogger(__name__)

class ResumeInfo(BaseModel):
    """Structured resume information extracted from text."""
    skills: List[str] = Field(default_factory=list, description="List of skills")
    projects: List[str] = Field(default_factory=list, description="List of project descriptions")
    education: List[str] = Field(default_factory=list, description="List of education details")
    experience: List[str] = Field(default_factory=list, description="List of work experiences")


class ResumeAgent:
    """Agent responsible for parsing resume text and extracting structured information."""
    
    def __init__(self, llm_client: Any = None):
        """
        Initialize the ResumeAgent.
        
        Args:
            llm_client: An LLM client instance (e.g., from LangChain) that supports 
                        with_structured_output for info extraction.
        """
        self.llm_client = llm_client

    def process(self, text: str) -> Dict[str, Any]:
        """
        Process the raw resume text and extract structured fields.
        
        Args:
            text: Raw resume text extracted from a file.
            
        Returns:
            A dictionary containing skills, projects, education, and experience lists.
        """
        if not text or not text.strip():
            logger.error("Empty text provided for resume extraction")
            raise ValueError("Resume text cannot be empty")

        if self.llm_client is None:
            logger.warning("No LLM client provided. Returning empty output.")
            return ResumeInfo().model_dump()
            
        try:
            logger.info("Extracting structured information from resume text via LLM.")
            # Assuming llm_client is a LangChain ChatModel supporting with_structured_output
            # structured_llm = self.llm_client.with_structured_output(ResumeInfo)
            
            # prompt = (
            #     "Extract the following resume text into structured fields: "
            #     "skills, projects, education, and experience. "
            #     "Ensure lists are returned for each category.\n\n"
            #     f"Resume Text:\n{text}"
            # )
            prompt = f"""
            你是专业HR。
            请分析简历。
            只返回JSON。
            格式：
            {{
                "技能": [],
                "项目经历": [],
                "教育经历": [],
                "实习经历": []
            }}
            简历内容：
            {text}
            """

            response = self.llm_client.invoke(prompt)

            return extract_json(response.content)
            # result: ResumeInfo = structured_llm.invoke(prompt)
            # return result.model_dump()
            
        except Exception as e:
            logger.error(f"Error during LLM extraction: {e}")
            raise
