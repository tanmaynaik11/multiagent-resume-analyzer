from app.config import OPENAI_API_KEY, REDIS_HOST, REDIS_PORT, QDRANT_HOST, QDRANT_PORT
from app.utils.logger import get_logger
import redis
from openai import OpenAI
import qdrant_client
from fastapi import FastAPI
from app.models import MatchingInput, OrchestratorState
from app.langgraph_flow import build_graph

logger = get_logger("MainApp")

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
client_qdrant = qdrant_client.QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
client_openai = OpenAI(api_key=OPENAI_API_KEY)
app = FastAPI()
graph = build_graph()

@app.post("/multiagent_match/")
async def match_route(input: MatchingInput):
    logger.info("Received matching request")
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
