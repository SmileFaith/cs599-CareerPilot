# CareerPilot Architecture Design

## 1. System Overview

CareerPilot 是一个基于 Multi-Agent + LangGraph 的智能求职成长助手。

系统目标：

* 分析简历
* 分析目标岗位
* 识别能力差距
* 生成学习路线
* 模拟面试
* 记录长期成长

---

# 2. High-Level Architecture
<img width="652" height="632" alt="Career整体架构图 drawio" src="https://github.com/user-attachments/assets/7e229713-4158-4530-ad4f-02fd43d023eb" />

# 3. Agent Architecture

## Resume Agent

Purpose:

解析用户简历

Input:

* PDF
* DOCX

Output:

```json
{
  "skills": [],
  "projects": [],
  "education": [],
  "experience": []
}
```

Responsibilities:

* 文件读取
* 内容提取
* 技能识别

---

## Job Agent

Purpose:

分析目标岗位

Input:

Job Description

Output:

```json
{
  "required_skills": [],
  "preferred_skills": []
}
```

Responsibilities:

* 技能提取
* 岗位分类
* 经验要求识别

---

## Gap Analysis Agent

Purpose:

比较用户与岗位要求

Input:

ResumeInfo

JobInfo

Output:

```json
{
  "matched_skills": [],
  "missing_skills": [],
  "score": 0
}
```

Responsibilities:

* 技能匹配
* 缺失项分析
* 匹配度评分

---

## Learning Agent

Purpose:

生成成长路线

Input:

Gap Report

Output:

Learning Roadmap

Responsibilities:

* 技能学习排序
* 时间规划
* 项目推荐

---

## Interview Agent

Purpose:

模拟面试

Input:

Job Requirement

Output:

Questions

Feedback

Responsibilities:

* 生成问题
* 评价答案
* 给出建议

---

# 4. LangGraph State Design

```python
from typing import TypedDict

class CareerState(TypedDict):
    resume_text: str
    job_description: str

    resume_info: dict
    job_info: dict

    gap_report: dict

    learning_plan: dict

    interview_questions: list

    memory: dict
```

---

# 5. Workflow Design

START

↓

Resume Agent

↓

Job Agent

↓

Gap Analysis Agent

↓

Learning Agent

↓

Interview Agent

↓

Save Memory

↓

END

---

# 6. Tool Layer

## Resume Reader Tool

Input:

resume file

Output:

resume text

Libraries:

* pdfplumber
* python-docx

---

## Skill Extractor Tool

Input:

text

Output:

skill list

Method:

LLM Extraction

---

## Memory Tool

Input:

user state

Output:

saved state

Backend:

SQLite

---

## Evaluation Tool

Input:

agent output

Output:

score

Purpose:

Benchmark Testing

---

# 7. Memory Architecture

## Short-Term Memory

Current Session State

Stored In:

LangGraph State

---

## Long-Term Memory

Stored In:

SQLite

Tables:

users

user_progress

learning_history

interview_history

---

# 8. Database Design

users

| field      | type     |
| ---------- | -------- |
| id         | INTEGER  |
| name       | TEXT     |
| created_at | DATETIME |

user_progress

| field      | type    |
| ---------- | ------- |
| id         | INTEGER |
| user_id    | INTEGER |
| skill_name | TEXT    |
| status     | TEXT    |

interview_history

| field    | type    |
| -------- | ------- |
| id       | INTEGER |
| user_id  | INTEGER |
| score    | INTEGER |
| feedback | TEXT    |

---

# 9. Deployment Architecture

Frontend

Streamlit

↓

Backend

FastAPI

↓

LangGraph

↓

DeepSeek API

↓

SQLite

---

# 10. Future Extensions

V2:

* MCP Integration
* LinkedIn Job Import
* RAG Knowledge Base
* Multi-Model Support

V3:

* Personalized Recommendation
* Auto Resume Rewrite
* Job Market Analysis
