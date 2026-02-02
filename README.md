# Agentic AI Call Center Copilot  
*A reference architecture and working demo for production-ready agentic AI applications*

## Overview

This repository contains a **scenario-driven Agentic AI Copilot** designed for healthcare call center use cases, including coverage questions, eligibility checks, claim status explanations, and multi-intent orchestration.

The goal of this project is not to build a chatbot, but to demonstrate a **production-oriented agent architecture** where:

- Large Language Models (LLMs) focus on **synthesis and explanation**
- **Authority stays with systems of record** (policies, eligibility, claims)
- Tool calls and retrieval are **explicit, auditable, and governed**
- The system can scale from demo to enterprise deployment

Azure is used as the reference cloud, but the architecture is **cloud-agnostic** and portable.

---

## Key Principles

This solution is built around a few core design principles:

- **LLMs do not decide outcomes**  
  They explain, summarize, and contextualize results returned by authoritative systems.

- **Retrieval over hallucination**  
  Policy answers are grounded via Retrieval-Augmented Generation (RAG) with citations.

- **Clear separation of concerns**  
  Each layer (UI, orchestration, tools, models, data) has a defined responsibility.

- **Agent orchestration, not prompt engineering**  
  The system decomposes questions, routes tools, and combines results intentionally.

---

## Demo Scenarios

The demo is structured around four realistic healthcare call center scenarios.

### 1. Coverage & Prior Authorization (RAG + LLM)

**Question:**  
_Is outpatient physical therapy covered, and does it require prior authorization?_

**What happens:**
- Agent retrieves policy documents
- LLM summarizes coverage
- Citations are returned with policy IDs

**What this proves:**
- Retrieval-Augmented Generation
- Hallucination control
- Grounded LLM synthesis

---

### 2. Eligibility Check (Live Tool Call)

**Question:**  
_Is this member currently eligible?_

**What happens:**
- Agent calls a live eligibility tool
- Returns ACTIVE / INACTIVE status
- No policy retrieval required

**What this proves:**
- Real-time data access
- Tool routing
- Correct separation of concerns

---

### 3. Claim Denial Explanation (Tool + LLM)

**Question:**  
_Why was this claim denied and what are the next steps?_

**What happens:**
- Agent retrieves claim status via tool
- LLM explains the denial in plain language
- Structured, compliance-safe response

**What this proves:**
- Explainability
- LLMs as interpreters, not decision-makers
- Healthcare realism

---

### 4. Multi-Intent Orchestration

**Question:**  
_Is outpatient PT covered and is this member eligible?_

**What happens:**
- Agent decomposes the question
- Calls multiple tools (policy + eligibility)
- Synthesizes a single response

**What this proves:**
- True agent behavior
- Multi-tool reasoning
- Orchestration beyond chatbots

---

## Architecture Overview

At a high level, the solution consists of:

### Frontend
- Streamlit demo UI (scenario-driven)
- Copilot Studio / Teams (production front door)

### API & Orchestration
- FastAPI backend
- LangChain agent for routing and reasoning

### Tools
- Policy search (RAG)
- Eligibility lookup
- Claim status lookup
- CRM write-back

### Models
- OpenAI or Azure OpenAI (LLM)
- Embeddings for retrieval

### Data
- Policy documents (JSON / Blob Storage)
- Vector index (local or Azure AI Search)
- Simulated system-of-record APIs

### Platform
- Azure Container Apps
- Azure API Management
- Key Vault + Managed Identity
- Application Insights

---

## Repository Structure

call-center-ai-demo/
│
├── backend/
│ ├── app/
│ │ ├── main.py # FastAPI entrypoint
│ │ ├── langchain_agent.py # Agent definition + routing
│ │ ├── tools/ # Tool implementations
│ │ └── config.py # Environment & settings
│
├── frontend/
│ └── streamlit_app.py # Scenario-driven demo UI
│
├── data/
│ └── policies.jsonl # Sample policy documents
│
├── diagrams/
│ └── architecture.drawio # Conceptual & cloud diagrams
│
├── .env.example # Environment variable template
└── README.md


---

## Running the Demo Locally

### Prerequisites
- Python 3.10+
- OpenAI or Azure OpenAI API key
- `pip install -r requirements.txt`

### Backend
```bash
uvicorn app.main:app --reload --port 8000
Verify:

http://localhost:8000/docs

http://localhost:8000/openapi.json

Frontend
cd frontend
streamlit run streamlit_app.py
Environment Variables
Example .env:

OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
(For Azure OpenAI, additional endpoint and deployment variables are required.)

