from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.utils.common import extract_json, compute_experience_years
from app.models import OrchestratorState, ResumeSections
import redis, pickle
from app.utils.logger import get_logger

logger = get_logger("MainApp")

redis_client = redis.Redis(host="localhost", port=6379, db=0)
client_openai = OpenAI(api_key=OPENAI_API_KEY)

RESUME_PROMPT = """
You are a resume parsing agent. Extract structured data in strict JSON format:

{
  "sections": {
    "Professional_Experience": [
      { "job_title": "", "organization": "", "start_date": "YYYY-MM", "end_date": "YYYY-MM", "description": "" }
    ],
    "Education": [], "Certifications": []
  }
}
"""

def resume_parser(state: OrchestratorState) -> OrchestratorState:
    logger.info("Parsing resume")
    response = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": RESUME_PROMPT},
            {"role": "user", "content": state.resume_text}
        ],
        temperature=0.0
    )
    content = response.choices[0].message.content.strip()
    extracted = extract_json(content)
    sections = ResumeSections(**extracted["sections"])
    total_experience_years = compute_experience_years(sections)
    redis_client.set(f"resume:{state.resume_text[:30]}", pickle.dumps(sections.dict()))
    return state.copy(update={
        "resume_sections": sections,
        "total_experience_years": total_experience_years
    })
