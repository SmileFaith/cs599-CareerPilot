import time
import json
from pathlib import Path
from typing import Any

from src.agents.resume_agent import ResumeAgent
from src.agents.job_agent import JobAgent
from src.agents.gap_agent import GapAnalysisAgent

def generate_dataset() -> dict:
    """Generate mock dataset for evaluation."""
    resumes = []
    for i in range(1, 11):
        resumes.append({
            "id": f"R{i}",
            "text": f"Experienced software engineer. Skills include Python, Docker, SQL. Developed project {i}.",
            "expected_skills": ["Python", "Docker", "SQL"]
        })
        
    jobs = []
    for i in range(1, 6):
        jobs.append({
            "id": f"J{i}",
            "description": f"Looking for backend dev. Required: Python, SQL. Nice to have: AWS.",
            "expected_required": ["Python", "SQL"],
            "expected_preferred": ["AWS"]
        })
        
    return {"resumes": resumes, "jobs": jobs}


class Evaluator:
    """Evaluation Module to benchmark and generate metrics."""
    
    def __init__(self, llm_client: Any = None):
        self.resume_agent = ResumeAgent(llm_client)
        self.job_agent = JobAgent(llm_client)
        self.gap_agent = GapAnalysisAgent(llm_client)
        
    def run_benchmark(self, dataset: dict):
        results = {
            "resume_metrics": [],
            "job_metrics": [],
            "gap_metrics": [],
            "response_times": []
        }
        
        # Evaluate Resumes
        for res in dataset["resumes"]:
            start_t = time.time()
            parsed = self.resume_agent.process(res["text"])
            end_t = time.time()
            
            elapsed = end_t - start_t
            results["response_times"].append(elapsed)
            
            extracted_skills = set([s.lower() for s in parsed.get("skills", [])])
            expected_skills = set([s.lower() for s in res["expected_skills"]])
            
            if expected_skills:
                accuracy = len(extracted_skills.intersection(expected_skills)) / len(expected_skills)
            else:
                accuracy = 1.0
                
            results["resume_metrics"].append(accuracy)
            
        # Evaluate Jobs
        for job in dataset["jobs"]:
            start_t = time.time()
            parsed = self.job_agent.process(job["description"])
            end_t = time.time()
            
            elapsed = end_t - start_t
            results["response_times"].append(elapsed)
            
            extracted_req = set([s.lower() for s in parsed.get("required_skills", [])])
            expected_req = set([s.lower() for s in job["expected_required"]])
            
            if expected_req:
                accuracy = len(extracted_req.intersection(expected_req)) / len(expected_req)
            else:
                accuracy = 1.0
                
            results["job_metrics"].append(accuracy)
            
        # Evaluate Gap Analysis
        for res in dataset["resumes"][:5]:
            for job in dataset["jobs"]:
                resume_info = {"skills": res["expected_skills"]}
                job_info = {"required_skills": job["expected_required"]}
                
                start_t = time.time()
                gap = self.gap_agent.process(resume_info, job_info)
                end_t = time.time()
                
                results["response_times"].append(end_t - start_t)
                results["gap_metrics"].append(gap.get("score", 0))
                
        return self._generate_report(results)
        
    def _generate_report(self, results: dict) -> str:
        avg_res_acc = sum(results["resume_metrics"]) / len(results["resume_metrics"]) if results["resume_metrics"] else 0
        avg_job_acc = sum(results["job_metrics"]) / len(results["job_metrics"]) if results["job_metrics"] else 0
        avg_resp_time = sum(results["response_times"]) / len(results["response_times"]) if results["response_times"] else 0
        
        # Match Score Consistency (Standard Deviation)
        scores = results["gap_metrics"]
        if len(scores) > 1:
            mean_score = sum(scores) / len(scores)
            variance = sum((x - mean_score) ** 2 for x in scores) / len(scores)
            std_dev = variance ** 0.5
        else:
            std_dev = 0.0
            
        md = f"""# CareerPilot Evaluation Report

## Benchmark Results

* **Resume Parse Accuracy**: {avg_res_acc * 100:.2f}%
* **Job Analysis Accuracy**: {avg_job_acc * 100:.2f}%
* **Match Score Consistency (Std Dev)**: {std_dev:.2f}
* **Average Response Time**: {avg_resp_time:.4f} seconds

## Methodology

* Evaluated on {len(results["resume_metrics"])} resumes.
* Evaluated on {len(results["job_metrics"])} job descriptions.
* Executed {len(results["gap_metrics"])} gap analyses.
"""
        return md


if __name__ == "__main__":
    dataset = generate_dataset()
    evaluator = Evaluator()
    report = evaluator.run_benchmark(dataset)
    
    # Task 24: Generate evaluation.md
    output_path = Path("evaluation.md")
    output_path.write_text(report, encoding="utf-8")
    print(f"Evaluation completed. Saved to {output_path.absolute()}")
