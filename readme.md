# 🤖 Multi-Agent Resume-JD Skill Matching System

An intelligent, production-ready AI system that leverages **LangGraph**, **Qdrant**, **SentenceTransformers**, and **FastAPI** to perform accurate and explainable skill matching between a candidate's resume and job descriptions. Also includes a Streamlit-based frontend for easy interaction.

---

## 🚀 Features

- ✅ **Resume Parsing Agent** — Extracts structured sections from raw resume text or PDFs.
- ✅ **Skill Extraction Agents** — Parses both resume and job description (JD) to extract relevant skills using LLMs.
- ✅ **Graph-Structured RAG** — Normalizes skills using vector-based semantic similarity over a hierarchical skill graph (Qdrant).
- ✅ **Matching Score Computation** — Calculates overlap and gap between JD skills and candidate resume.
- ✅ **LangGraph Orchestration** — Each step is modular and orchestrated with state-based execution flow.
- ✅ **Streamlit Frontend** — Upload resume PDFs and input JD text to view results interactively.

---

## 📁 Project Structure

multiagent_resume_analyzer/
│
├── app/
│ ├── agents/ # LLM agent functions (resume_parser, jd_parser, etc.)
│ ├── utils/ # Utility modules (logger, Redis, common methods)
│ ├── schemas.py # Pydantic schemas for state and inputs
│ ├── config.py # Environment variable configuration
│
├── streamlit_app.py # Streamlit frontend UI
├── main.py # FastAPI backend with LangGraph orchestration
├── rag_data.py # Qdrant skill graph loader
├── .env # (excluded) Environment variables
├── .gitignore
└── requirements.txt

## Install Dependencies

pip install -r requirements.txt

## Set Environment Variables
Create a .env file like:
OPENAI_API_KEY=your_openai_key
REDIS_HOST=localhost
REDIS_PORT=6379
QDRANT_HOST=localhost
QDRANT_PORT=6333

## Load Skill Graph to Qdrant
python rag_data.py
This will create and populate a vector database in Qdrant using predefined skill-subskill hierarchy.

## Start Backend API (FastAPI + LangGraph)
uvicorn app.main:app --reload

## Start Frontend (Streamlit)
streamlit run streamlit_app.py

## How It Works
Resume Upload → Extracts experience and skills.

JD Input → Extracts skills from job description.

Qdrant Matching → Normalizes both to canonical skill graph.

Score & Gap → Computes overlap and missing skills.

Output → JSON + Streamlit UI.

## Example Output
{
  "total_experience_years": 3.8,
  "matching_score": 0.76,
  "normalized_resume_skills": [...],
  "normalized_jd_skills": [...],
  "skill_gap": ["AWS Lambda", "RAG Pipelines"]
}
