import logging
from typing import List, Any
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class SkillList(BaseModel):
    skills: List[str] = Field(default_factory=list, description="Extracted list of skills")

class SkillExtractorTool:
    """Tool for extracting general skills from text using DeepSeek LLM."""
    
    def __init__(self, llm_client: Any):
        """
        Initialize the SkillExtractorTool.
        
        Args:
            llm_client: LLM client supporting structured output (e.g. connected to DeepSeek API).
        """
        self.llm_client = llm_client
        
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract a list of skills from arbitrary text.
        
        Args:
            text: Source text to extract skills from.
            
        Returns:
            List of skills.
        """
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty")
            
        try:
            logger.info("Extracting skills using SkillExtractorTool")
            structured_llm = self.llm_client.with_structured_output(SkillList)
            
            prompt = (
                "Extract all professional and technical skills mentioned in the following text. "
                "Return them as a list of strings.\n\n"
                f"Text:\n{text}"
            )
            
            result: SkillList = structured_llm.invoke(prompt)
            return result.skills
        except Exception as e:
            logger.error(f"Error extracting skills: {e}")
            raise
