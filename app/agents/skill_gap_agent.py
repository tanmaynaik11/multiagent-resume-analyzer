from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.utils.common import extract_json, compute_experience_years
from app.models import OrchestratorState, ResumeSections
import redis, pickle

redis_client = redis.Redis(host="localhost", port=6379, db=0)
client_openai = OpenAI(api_key=OPENAI_API_KEY)
def skill_gap_analyzer(state: OrchestratorState) -> OrchestratorState:
    resume_set = set(state.normalized_resume_skills)
    jd_set = set(state.normalized_jd_skills)
    gap = list(jd_set - resume_set)
    return state.copy(update={"skill_gap": gap})