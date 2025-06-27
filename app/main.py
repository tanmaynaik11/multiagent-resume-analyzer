from app.config import OPENAI_API_KEY, REDIS_HOST, REDIS_PORT, QDRANT_HOST, QDRANT_PORT
from app.utils.logger import get_logger
import redis
from openai import OpenAI
import qdrant_client
from fastapi import FastAPI
from app.models import MatchingInput, OrchestratorState, RecruiterMatchInput
from app.langgraph_flow import build_graph

# import mlflow
# mlflow.set_tracking_uri("file:///absolute/path/to/mlruns") 
# mlflow.set_experiment("Resume-JD Matching")

logger = get_logger("MainApp")

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
client_qdrant = qdrant_client.QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
client_openai = OpenAI(api_key=OPENAI_API_KEY)
app = FastAPI()
graph = build_graph()

# def log_matching_to_mlflow(state: OrchestratorState):
#     with mlflow.start_run():
#         mlflow.log_param("resume_text_snippet", state.resume_text[:100])
#         mlflow.log_param("jd_text_snippet", state.jd_text[:100])
#         mlflow.log_metric("matching_score", state.matching_score or 0)
#         mlflow.log_metric("experience_years", state.total_experience_years or 0)
#         mlflow.log_text(str(state.resume_skills), "resume_skills.txt")
#         mlflow.log_text(str(state.jd_skills), "jd_skills.txt")
#         mlflow.log_text(str(state.skill_gap), "skill_gap.txt")

@app.post("/multiagent_match/")
async def match_route(input: MatchingInput):
    logger.info("Received matching request")
    # log_matching_to_mlflow(final_state)
    state = OrchestratorState(resume_text=input.resume_text, jd_text=input.jd_text)
    output = graph.invoke(state)
    final = OrchestratorState(**output)
    return {
        "experience": [job.dict() for job in final.resume_sections.Professional_Experience],
        "skills": final.resume_skills,
        "jd_skills": final.jd_skills,
        "normalized_resume_skills": final.normalized_resume_skills,
        "normalized_jd_skills": final.normalized_jd_skills,
        "total_experience_years": final.total_experience_years,
        "matching_score": final.matching_score,
        "skill_gap": final.skill_gap
    }

@app.post("/recruiter_match/")
async def recruiter_match_route(payload: RecruiterMatchInput):
    logger.info(f"Received recruiter match request with {len(payload.resumes)} resumes")
    # log_matching_to_mlflow(final_state)
    results = []
    for resume in payload.resumes:
        try:
            state = OrchestratorState(resume_text=resume.text, jd_text=payload.jd_text, recruiter_instructions=payload.instructions)
            output = graph.invoke(state)
            final = OrchestratorState(**output)

            results.append({
                "Filename": resume.filename,
                "Matching Score (%)": round(final.matching_score * 100, 2),
                "Experience (Years)": final.total_experience_years,
                "Skill Gap": ", ".join(final.skill_gap)
            })

        except Exception as e:
            logger.error(f"Error processing resume {resume.filename}: {str(e)}")
            results.append({
                "Filename": resume.filename,
                "Matching Score (%)": "Error",
                "Experience (Years)": "Error",
                "Skill Gap": "Error"
            })

    return {"matches": results}
