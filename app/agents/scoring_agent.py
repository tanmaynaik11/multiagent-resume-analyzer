from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.utils.common import normalize_skills, compute_matching_score
from app.models import OrchestratorState, ResumeSections
import redis, pickle

redis_client = redis.Redis(host="localhost", port=6379, db=0)
client_openai = OpenAI(api_key=OPENAI_API_KEY)

def scoring_agent(state: OrchestratorState) -> OrchestratorState:
    norm_resume = normalize_skills(state.resume_skills)
    norm_jd = normalize_skills(state.jd_skills)
    score = compute_matching_score(norm_resume, norm_jd)
    return state.copy(update={
        "normalized_resume_skills": norm_resume,
        "normalized_jd_skills": norm_jd,
        "matching_score": score
    })