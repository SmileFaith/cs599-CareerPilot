import logging
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from src.utils.json_parser import extract_json


logger = logging.getLogger(__name__)

class LearningPlan(BaseModel):
    """Structured learning roadmap and plan."""
    learning_sequence: List[str] = Field(
        default_factory=list, 
        description="Logical sequence of skills to learn based on the gap report"
    )
    estimated_duration_weeks: int = Field(
        default=0,
        description="Estimated learning duration in weeks"
    )
    weekly_roadmap: Dict[str, List[str]] = Field(
        default_factory=dict, 
        description="Weekly roadmap mapping specific week identifiers (e.g., 'week1', 'week2') to a list of learning tasks or milestones"
    )
    recommended_projects: List[str] = Field(
        default_factory=list, 
        description="List of recommended practical projects to build hands-on experience with the missing skills"
    )


class LearningAgent:
    """Agent responsible for creating a personalized learning roadmap based on a gap analysis report."""
    
    def __init__(self, llm_client: Any = None):
        """
        Initialize the LearningAgent.
        
        Args:
            llm_client: An LLM client instance supporting structured output.
        """
        self.llm_client = llm_client

    def process(self, gap_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a learning plan based on the missing skills from a gap report.
        
        Args:
            gap_report: Dictionary containing the gap analysis results 
                        (e.g., 'matched_skills', 'missing_skills', 'score').
            
        Returns:
            A dictionary containing learning_sequence, weekly_roadmap, and recommended_projects.
        """
        if not gap_report or not isinstance(gap_report, dict):
            logger.error("Invalid or empty gap report provided")
            raise ValueError("Gap report must be a non-empty dictionary")

        missing_skills = gap_report.get("missing_skills", [])
        if not missing_skills:
            logger.info("No missing skills found. Returning an empty learning plan.")
            return LearningPlan().model_dump()

        if self.llm_client is None:
            logger.warning("No LLM client provided. Returning default empty learning plan.")
            return LearningPlan().model_dump()
            
        try:
            logger.info("Generating learning plan via LLM.")
            # structured_llm = self.llm_client.with_structured_output(LearningPlan)
            
            # prompt = (
            #     "You are an expert technical mentor and career coach. "
            #     "Based on the following gap analysis report, identify the candidate's missing skills "
            #     "and generate a comprehensive, structured learning plan. "
            #     "The plan must include:\n"
            #     "1. A logical learning sequence for acquiring these missing skills.\n"
            #     "2. A weekly roadmap breaking down the learning timeline (use keys like 'week1', 'week2', etc. mapping to task lists).\n"
            #     "3. Recommended practical projects to apply these new skills effectively.\n\n"
            #     f"Gap Report:\n{gap_report}"
            # )
            prompt = f"""
            你是一位资深职业规划导师。
            根据候选人与目标岗位的能力差距，生成个性化学习路线。
            要求：
            1. 根据缺失技能数量和难度估算学习周期
            2. 周期可以是2~16周
            3. 技能越多周期越长
            4. 按周拆分学习任务
            5. 输出JSON
            格式：
            {{
                "学习内容": [],
                "预计时长（周）": 0,
                "每周计划": {{
                    "week1": [],
                    "week2": []
                }},
                "推荐项目": []
            }}
            Gap Report:
            {gap_report}
            """
            
            # result: LearningPlan = structured_llm.invoke(prompt)
            # return result.model_dump()
            response = self.llm_client.invoke(prompt)

            return extract_json(response.content)
            
        except Exception as e:
            logger.error(f"Error during learning plan generation: {e}")
            raise
