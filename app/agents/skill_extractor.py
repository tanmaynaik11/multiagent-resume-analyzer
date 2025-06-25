from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.utils.common import extract_json, compute_experience_years
from app.models import OrchestratorState, ResumeSections
import redis, pickle
from app.utils.logger import get_logger

logger = get_logger("MainApp")

redis_client = redis.Redis(host="localhost", port=6379, db=0)
client_openai = OpenAI(api_key=OPENAI_API_KEY)

SKILL_EXTRACTION_PROMPT = """
You are a skill extraction agent.

Given this parsed resume structure, extract ALL technical, analytical, leadership, domain, software, management and cloud skills mentioned in Professional Experience, Education, Certifications or Projects.

Return distinct skills only, in JSON: {"skills": ["skill1", ...]}
"""

def resume_skill_extractor(state: OrchestratorState) -> OrchestratorState:
    logger.info("Extracting resume skills")
    resume_sections_json = state.resume_sections.json()
    response = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SKILL_EXTRACTION_PROMPT},
            {"role": "user", "content": resume_sections_json}
        ],
        temperature=0.0
    )
    content = response.choices[0].message.content.strip()
    extracted = extract_json(content)
    return state.copy(update={"resume_skills": extracted["skills"]})