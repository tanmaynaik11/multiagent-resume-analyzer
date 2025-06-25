from langgraph.graph import StateGraph
from app.models import OrchestratorState
from app.agents.resume_parser import resume_parser
from app.agents.jd_parser import jd_parser
from app.agents.skill_extractor import resume_skill_extractor
from app.agents.scoring_agent import scoring_agent
from app.agents.skill_gap_agent import skill_gap_analyzer

def build_graph():
    graph = StateGraph(state_schema=OrchestratorState)
    graph.add_node("ResumeParser", resume_parser)
    graph.add_node("ResumeSkillExtractor", resume_skill_extractor)
    graph.add_node("JDParser", jd_parser)
    graph.add_node("ScoringAgent", scoring_agent)
    graph.add_node("SkillGapAnalyzer", skill_gap_analyzer)
    graph.set_entry_point("ResumeParser")
    graph.add_edge("ResumeParser", "ResumeSkillExtractor")
    graph.add_edge("ResumeSkillExtractor", "JDParser")
    graph.add_edge("JDParser", "ScoringAgent")
    graph.add_edge("ScoringAgent", "SkillGapAnalyzer")
    graph.set_finish_point("SkillGapAnalyzer")
    return graph.compile()
