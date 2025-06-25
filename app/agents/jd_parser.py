from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.utils.common import extract_json, compute_experience_years
from app.models import OrchestratorState, ResumeSections
import redis, pickle
from app.utils.logger import get_logger

logger = get_logger("MainApp")
redis_client = redis.Redis(host="localhost", port=6379, db=0)
client_openai = OpenAI(api_key=OPENAI_API_KEY)

JD_PROMPT = """
You are a job description skill extraction agent.

Given the full job description text, extract ALL skills, technologies, tools, languages, frameworks, platforms, analytics, cloud services, and domain-specific techniques mentioned anywhere (not only Skills section).

Return JSON: {"skills": ["skill1", ...]}
"""

def jd_parser(state: OrchestratorState) -> OrchestratorState:
    logger.info("Parsing job description")
    response = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": JD_PROMPT},
            {"role": "user", "content": state.jd_text}
        ],
        temperature=0.0
    )
    content = response.choices[0].message.content.strip()
    extracted = extract_json(content)
    redis_client.set(f"jd:{state.jd_text[:30]}", pickle.dumps(extracted))
    return state.copy(update={"jd_skills": extracted["skills"]})