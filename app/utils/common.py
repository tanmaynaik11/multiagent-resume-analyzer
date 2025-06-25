# app/utils/common.py

import re
import json
from typing import List
from sentence_transformers import SentenceTransformer
from dateutil.parser import parse
from qdrant_client import QdrantClient
from app.models import ResumeSections

# Global clients
embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")
qdrant_client = QdrantClient(host="localhost", port=6333)
collection_name = "skills_graph_rag"

def extract_json(content: str):
    """Extracts JSON from LLM response using regex."""
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError("No valid JSON found in LLM output.")

def normalize_skills(skills: List[str]) -> List[str]:
    """Query Qdrant to normalize skill names to canonical form."""
    normalized = []
    for skill in skills:
        try:
            embedding = embedder.encode(skill)
            results = qdrant_client.search(
                collection_name=collection_name,
                query_vector=embedding.tolist(),
                limit=1
            )
            if results and results[0].payload and 'skill' in results[0].payload:
                normalized.append(results[0].payload['skill'])
            else:
                normalized.append(skill)
        except Exception as e:
            print(f"[Normalize Error] {e}")
            normalized.append(skill)
    return normalized

def compute_experience_years(sections: ResumeSections) -> float:
    """Computes total experience in years from parsed resume sections."""
    total_months = 0
    for job in sections.Professional_Experience:
        try:
            if job.start_date and job.end_date:
                start = parse(job.start_date)
                end = parse(job.end_date)
                months = (end.year - start.year) * 12 + (end.month - start.month)
                total_months += months
        except Exception as e:
            print(f"[Experience Parse Error] {e}")
            continue
    return round(total_months / 12, 1)

def compute_matching_score(resume_skills, jd_skills):
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)
    matched = len(resume_set.intersection(jd_set))
    total_required = len(jd_set)
    if total_required == 0:
        return 0.0
    return round(matched / total_required, 2)
