import logging
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from src.utils.json_parser import extract_json

logger = logging.getLogger(__name__)

class GapInfo(BaseModel):
    """Structured gap analysis between resume and job requirements."""
    matched_skills: List[str] = Field(default_factory=list, description="List of skills from the resume that match job requirements")
    missing_skills: List[str] = Field(default_factory=list, description="List of skills required by the job but missing from the resume")
    score: int = Field(default=0, ge=0, le=100, description="Match score from 0 to 100 based on the skillset match")


class GapAnalysisAgent:
    """Agent responsible for analyzing the gap between a candidate's resume and job requirements."""
    
    def __init__(self, llm_client: Any = None):
        """
        Initialize the GapAnalysisAgent.
        
        Args:
            llm_client: An LLM client instance supporting structured output.
        """
        self.llm_client = llm_client
        # print("llm_client =", self.llm_client)

    def process(self, resume_info: Dict[str, Any], job_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare resume information against job requirements.
        
        Args:
            resume_info: Extracted resume data (skills, projects, etc.).
            job_info: Extracted job requirements (required_skills, preferred_skills, etc.).
            
        Returns:
            A dictionary containing matched_skills, missing_skills, and a score (0-100).
        """
        if not resume_info and not job_info:
            logger.error("Both resume_info and job_info are empty")
            raise ValueError("Input info cannot be entirely empty")

        if self.llm_client is None:
            logger.warning("No LLM client provided. Returning default empty gap info.")
            return GapInfo().model_dump()
            
        try:
            logger.info("Performing gap analysis via LLM.")
            # structured_llm = self.llm_client.with_structured_output(GapInfo)
            
            # prompt = (
            #     "You are an expert technical recruiter and career coach. "
            #     "Compare the given resume information against the job requirements. "
            #     "Identify which required and preferred skills are present in the resume (matched_skills) "
            #     "and which ones are missing (missing_skills). "
            #     "Assign a match score from 0 to 100 representing how well the candidate fits the job skillset.\n\n"
            #     f"Resume Info:\n{resume_info}\n\n"
            #     f"Job Info:\n{job_info}"
            # )

            prompt = f"""
            你是资深技术招聘专家。
            将提供的简历信息与职位要求进行比对。
            识别出简历中具备的必备技能和优先技能（matched_skills），以及简历中缺失的技能（missing_skills）
            并给出一个0到100分的匹配度评分，代表候选人与职位技能要求的契合程度。
            只返回JSON。
            格式：
            {{
                "matched_skills": [],
                "missing_skills": [],
                "score": 0
            }}
            候选人：
            {resume_info}
            岗位要求：
            {job_info}
            """

            response = self.llm_client.invoke(prompt)
            result = extract_json(response.content)
            # print("====== GAP INPUT ======")
            # print(resume_info)
            #
            # print("====== JOB INPUT ======")
            # print(job_info)
            # 
            # print("====== GAP OUTPUT ======")
            # print(result)
            return result
            # result: GapInfo = structured_llm.invoke(prompt)
            # return result.model_dump()
            
        except Exception as e:
            logger.error(f"Error during gap analysis: {e}")
            raise
