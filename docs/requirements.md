# CareerPilot - AI求职成长助手

## 项目概述

CareerPilot 是一个基于 Agent 架构的智能求职辅助系统。

系统帮助用户完成：

* 简历分析
* 岗位要求分析
* 技能差距识别
* 学习路线规划
* 模拟面试
* 求职成长记录

本项目采用 SDD（Specification Driven Development）方法开发。

---

# 一、项目目标

## 核心问题

求职者通常面临以下问题：

1. 不清楚目标岗位要求
2. 无法客观评估简历质量
3. 不知道自己缺少哪些技能
4. 不知道学习顺序
5. 缺乏面试练习
6. 无法持续跟踪成长过程

CareerPilot 应帮助用户解决以上问题。

---

# 二、用户角色

## 普通用户

输入：

* 简历
* 目标岗位

获得：

* 匹配度分析
* 技能差距分析
* 学习路线
* 模拟面试

---

# 三、系统功能需求

## F1 简历解析

用户上传：

* PDF
* DOCX

系统自动提取：

* 教育经历
* 技能
* 项目经历
* 实习经历

输出：

```json
{
  "education": "",
  "skills": [],
  "projects": [],
  "experience": []
}
```

---

## F2 岗位分析

输入：

岗位JD文本

例如：

后端开发工程师

要求：

* Java
* Spring Boot
* Redis
* Docker

输出：

```json
{
  "required_skills": [],
  "preferred_skills": [],
  "experience_level": ""
}
```

---

## F3 技能差距分析

比较：

Resume Skills

VS

Job Skills

输出：

```json
{
  "matched": [],
  "missing": [],
  "score": 0
}
```

评分范围：

0-100

---

## F4 学习路线规划

根据缺失技能生成：

* 学习顺序
* 时间规划
* 推荐项目

输出：

```json
{
  "week1": [],
  "week2": [],
  "week3": []
}
```

---

## F5 面试模拟

根据岗位要求生成：

* 技术面试题
* 项目面试题
* 行为面试题

用户回答后：

Agent进行评价

输出：

```json
{
  "score": 85,
  "feedback": ""
}
```

---

## F6 长期记忆

记录：

用户技能成长情况

例如：

```json
{
  "user_id":"001",
  "skills":[
    "Java",
    "Redis"
  ],
  "completed_courses":[]
}
```

支持跨会话读取。

---

# 四、Agent设计

系统采用多Agent架构。

---

## Agent 1 Resume Agent

职责：

解析简历

输入：

Resume File

输出：

Structured Resume

---

## Agent 2 Job Agent

职责：

分析岗位需求

输入：

Job Description

输出：

Job Requirement

---

## Agent 3 Gap Analysis Agent

职责：

识别技能差距

输入：

Resume + Job Requirement

输出：

Gap Report

---

## Agent 4 Learning Agent

职责：

制定学习路线

输入：

Gap Report

输出：

Learning Roadmap

---

## Agent 5 Interview Agent

职责：

模拟面试

输入：

Job Requirement

输出：

Questions + Feedback

---

# 五、LangGraph工作流

State：

```python
CareerState = {
    "resume_text": str,
    "job_description": str,
    "resume_info": dict,
    "job_info": dict,
    "gap_analysis": dict,
    "learning_plan": dict,
    "interview_questions": list,
    "memory": dict
}
```

流程：

START

↓

Resume Agent

↓

Job Agent

↓

Gap Agent

↓

Learning Agent

↓

Interview Agent

↓

END

---

# 六、工具设计

## Tool 1 Resume Reader

功能：

读取PDF/DOCX

输入：

file_path

输出：

resume_text

---

## Tool 2 Skill Extractor

功能：

提取技能关键词

输出：

skills list

---

## Tool 3 Memory Storage

功能：

保存用户状态

支持：

JSON

SQLite

FAISS

---

## Tool 4 Learning Resource Generator

功能：

生成学习建议

---

# 七、记忆机制

MVP阶段：

SQLite

表：

users

progress

skills

conversation_history

支持：

保存技能成长记录

查询历史学习进度

---

# 八、技术栈

Programming Language

Python 3.12

Frontend

Streamlit

Backend

FastAPI

Agent Framework

LangGraph

LLM

DeepSeek API

Memory

SQLite

Vector Store

FAISS

Deployment

Docker

Version Control

GitHub

---

# 九、目录结构

CareerPilot

docs/

src/

src/agents/

src/tools/

src/memory/

src/graph/

src/api/

src/frontend/

tests/

Dockerfile

docker-compose.yml

README.md

.env.example

---

# 十、API设计

POST /analyze-resume

输入：

resume file

输出：

resume analysis

---

POST /analyze-job

输入：

job description

输出：

job analysis

---

POST /gap-analysis

输出：

gap report

---

POST /learning-plan

输出：

roadmap

---

POST /interview

输出：

questions

---

# 十一、评估方案

测试集：

10份简历

5个岗位JD

共50次测试

指标：

Resume Parse Success Rate

Gap Analysis Accuracy

Response Time

User Satisfaction

记录：

evaluation.md

---

# 十二、非功能需求

响应时间：

小于30秒

支持：

Chrome

Edge

Firefox

代码覆盖率：

大于60%

支持Docker部署

API Key不允许硬编码

---

# 十三、MVP范围

必须完成：

√ 简历解析

√ 岗位分析

√ 技能差距分析

√ 学习路线生成

√ 基础记忆

可选扩展：

□ 面试模拟

□ 向量数据库

□ 多模型支持

□ MCP集成

---

# 十四、课程验收目标

覆盖课程要求：

√ SDD

√ Function Calling

√ Memory

√ LangGraph

√ Multi-Agent

√ Evaluation

最终产出：

1. GitHub仓库

2. Docker部署

3. 项目报告

4. 演示视频
