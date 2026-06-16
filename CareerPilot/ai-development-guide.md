# AI Development Guide

## Project

CareerPilot

AI Career Development Assistant

---

# Development Principle

This project follows:

Specification Driven Development (SDD)

Implementation must strictly follow:

1. docs/requirements.md
2. docs/architecture.md
3. docs/tasks.md

If there is any conflict:

requirements.md > architecture.md > tasks.md

Do not invent features that are not defined in the specifications.

---

# Development Workflow

Before implementing any feature:

1. Read requirements.md
2. Read architecture.md
3. Read tasks.md
4. Identify the target task
5. Implement only the requested task

Do not implement unrelated features.

Do not modify completed modules unless explicitly requested.

---

# Technology Stack

Programming Language

Python 3.11

Backend

FastAPI

Frontend

Streamlit

Agent Framework

LangGraph

LLM

DeepSeek API

Database

SQLite

Vector Database

FAISS (Optional)

Deployment

Docker

Testing

pytest

---

# Directory Structure

All code must be placed under:

src/

Structure:

src/

agents/

api/

frontend/

graph/

memory/

tools/

models/

utils/

tests/

Do not create random directories.

Do not place business logic in the project root.

---

# Code Style

Follow:

PEP8

Use:

* Type Hints
* Dataclass when appropriate
* Clear naming

Example:

```python
def analyze_resume(
    resume_text: str
) -> dict:
    ...
```

Avoid:

```python
def run(x):
    ...
```

---

# File Size Rule

Single file should ideally remain under:

300 lines

Maximum:

500 lines

If a file becomes too large:

Split into modules.

---

# Documentation Rule

Every public class must include:

```python
class ResumeAgent:
    """
    Analyze user resumes and extract
    structured information.
    """
```

Every public function must include:

```python
def analyze_resume():
    """
    Analyze resume content.

    Returns:
        Structured resume data.
    """
```

---

# Logging Rule

Use logging.

Do not use print() for production logic.

Example:

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Resume parsed")
```

---

# Error Handling Rule

Every external operation must have exception handling.

Examples:

* API calls
* Database operations
* File reading

Example:

```python
try:
    text = read_pdf(path)
except Exception as e:
    logger.error(str(e))
```

Never silently ignore exceptions.

---

# Security Rule

Never hardcode:

* API Keys
* Passwords
* Secrets

Use:

.env

Example:

```python
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
```

---

# Configuration Rule

All configurable values must be stored in:

src/config/

Examples:

* API URLs
* Timeouts
* Database paths

Do not hardcode configuration values.

---

# Agent Design Rule

Each Agent must have:

Single Responsibility

Example:

ResumeAgent

Only:

* Resume parsing
* Resume analysis

Do not mix:

* Resume analysis
* Interview generation
* Memory management

in the same agent.

---

# LangGraph Rule

Workflow must be implemented through:

LangGraph

State object:

CareerState

All nodes must:

Receive state

Return updated state

Example:

```python
def resume_node(
    state: CareerState
) -> CareerState:
    ...
```

---

# Memory Rule

Memory implementation:

Short-Term Memory

LangGraph State

Long-Term Memory

SQLite

Do not store user memory in global variables.

---

# API Design Rule

Use REST APIs.

Response format:

```json
{
  "success": true,
  "data": {},
  "message": ""
}
```

Error format:

```json
{
  "success": false,
  "message": "error details"
}
```

Keep API responses consistent.

---

# Database Rule

Use SQLite.

Database access should be isolated in:

src/memory/

Do not write SQL queries inside agents.

Use repository pattern if possible.

---

# Frontend Rule

Use Streamlit.

Frontend responsibilities:

* File upload
* User input
* Result display

Do not place business logic in frontend.

---

# Testing Rule

Every module must include tests.

Location:

tests/

Examples:

tests/test_resume_agent.py

tests/test_job_agent.py

tests/test_memory.py

Coverage target:

60%+

---

# Evaluation Rule

All major features must be measurable.

Metrics:

* Resume Parse Accuracy
* Job Skill Extraction Accuracy
* Match Score Consistency
* Response Time

Evaluation results must be documented in:

docs/evaluation.md

---

# Docker Rule

Application must be deployable via:

Docker

Required files:

Dockerfile

docker-compose.yml

The project should run with:

docker compose up

---

# Git Rule

Commit frequently.

Recommended:

feat:

fix:

refactor:

docs:

test:

Examples:

feat: implement resume agent

fix: resolve sqlite connection issue

docs: update architecture

---

# AI Collaboration Rule

Before generating code:

Always read:

1. AI_DEVELOPMENT_GUIDE.md
2. docs/requirements.md
3. docs/architecture.md
4. docs/tasks.md

When implementing:

Only implement the requested task.

Do not rewrite unrelated modules.

Do not introduce new frameworks.

Do not change project architecture without approval.

---

# Output Requirement

When generating code:

Always provide:

1. File path
2. Complete code
3. Dependencies
4. Tests
5. Usage example

Never provide partial implementations unless explicitly requested.

---

# Definition of Done

A task is complete only when:

* Code compiles
* Type hints added
* Logging added
* Error handling added
* Tests added
* Documentation added

Only then can the task be marked as Done.
