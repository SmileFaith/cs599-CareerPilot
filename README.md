# CareerPilot

## 项目简介

CareerPilot 是一个基于 Multi-Agent 架构的 AI 求职成长助手。

系统帮助求职者完成：

* 简历分析
* 岗位分析
* 技能差距识别
* 学习路线规划
* 模拟面试
* 长期成长记录

通过 Agent 协作和 LangGraph 工作流管理，实现从简历评估到能力提升的一体化求职辅助体验。

---

## 方向

方向一：Agentic AI 原生开发

---

## 技术栈

### AI IDE

* Trae CN

### LLM

* DeepSeek API

### Agent Framework

* LangGraph

### Backend

* FastAPI

### Frontend

* Streamlit

### Memory

* SQLite

### Deployment

* Docker

### Version Control

* GitHub

---

## 核心技术要素

* SDD（Specification Driven Development）
* Function Calling
* Multi-Agent Collaboration
* Memory Mechanism
* LangGraph State Management
* Evaluation & Benchmark

---

## 项目架构

User

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

Memory Layer

---

## 项目目录结构

```text
cs599-CareerPilot/

├── docs/
│   ├── requirements.md
│   ├── architecture.md
│   ├── tasks.md
│   └── CS599_大作业报告.pdf
│
├── src/
│   ├── agents/  存放各业务 Agent 的核心逻辑，实现简历解析、岗位分析、能力差距评估、学习规划和模拟面试等智能体功能。
│   ├── graph/  基于 LangGraph 构建 Agent 工作流，负责多步骤任务的状态管理与执行流程编排。
│   ├── memory/  实现用户长期记忆与数据持久化功能，负责用户信息、学习记录和面试历史的存储与读取。
│   ├── tools/  封装 Agent 调用的工具模块，包括简历文件解析、技能提取等外部能力。
│   ├── api/  基于 FastAPI 构建后端接口服务，为前端提供统一的 REST API 访问入口。
│   └── frontend/  基于 Streamlit 构建用户交互界面，负责简历上传、结果展示和用户操作流程管理。
│   └── evaluation/  实现系统测试与评估功能，包括功能验证、Benchmark 测试和 Agent 效果评估。
│   └── llm/  封装大模型调用逻辑，统一管理 DeepSeek API 配置、Prompt 调用和结果解析。
│   └── utils/  存放项目通用工具函数和辅助模块，为各业务组件提供公共支持功能。
│
├── tests/
│
├── ai-development-guide.md
├── Dockerfile
├── docker-compose.yml
├── README.md
├── requirements.txt
├── .env
└── LICENSE
```
## 测试用例
### 示例简历技能（可自行准备pdf/docx文件）
```text
Python、FastAPI、MySQL、Git、Linux、Docker

项目经历：
- 基于 FastAPI 开发在线管理系统
- 使用 Docker 完成项目部署
- 使用 LangChain 开发智能问答系统
```

### 示例岗位 JD
```text
岗位名称：Python后端开发工程师

岗位职责：
1. 负责后端系统开发与维护
2. 设计RESTful API
3. 与前端协作完成项目开发

任职要求：
1. 熟练掌握Python
2. 熟悉FastAPI或Django
3. 熟悉MySQL
4. 熟悉Docker
5. 熟悉Git
6. 本科以上学历
7. 1-3年开发经验

加分项：
1. 了解LangChain
2. 了解LLM应用开发
```
---

## 环境搭建

### 1. Clone Repository

```bash
git clone https://github.com/SmileFaith/cs599-CareerPilot.git
cd cs599-CareerPilot
```

### 2. Create Virtual Environment

```bash
python -m venv .your_venv
```

Windows:

```bash
.your_venv\Scripts\activate
```

Linux/macOS:

```bash
source .your_venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

.env
```env
DEEPSEEK_API_KEY=your_api_key
```

⚠ Do not hardcode API keys.

---

## Run Backend

```bash
uvicorn src.api.main:app --reload
```

---

## Run Frontend

```bash
streamlit run src/frontend/app.py
```

---

## Run Docker

```bash
docker compose up --build
```

---

## Evaluation

Evaluation Metrics:

* Resume Parse Success Rate
* Skill Matching Accuracy
* Interview Feedback Quality
* Average Response Time

Results stored in:

```text
docs/evaluation.md
```

---

## Project Status

* [x] Proposal
* [x] MVP
* [ ] Final

---

## Future Work

* MCP Integration
* LinkedIn Job Parsing
* RAG Knowledge Base
* Multi-Model Support
* Personalized Career Planning
* More Agents

---

## License

MIT License
