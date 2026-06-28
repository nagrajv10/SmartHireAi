from .embedding_model import embedding_engine

def calculate_skill_match(candidate_skills: list[str], required_skills: list[str]) -> float:
    """Calculates the Jaccard similarity / overlap of skills."""
    if not required_skills:
        return 1.0 # If no specific skills required, match is 100%
    
    cand_set = set([s.lower() for s in candidate_skills])
    req_set = set([s.lower() for s in required_skills])
    
    overlap = len(cand_set.intersection(req_set))
    return overlap / len(req_set)

def calculate_experience_match(candidate_exp: float, required_exp: float) -> float:
    """Calculates an experience match score."""
    if required_exp <= 0:
        return 1.0
    if candidate_exp >= required_exp:
        return 1.0
    return candidate_exp / required_exp

def match_candidate_to_job(candidate_data: dict, job_data: dict) -> dict:
    """
    Computes a matching score based on multiple factors.
    candidate_data: {
        "skills": list[str],
        "experience_years": float,
        "clean_text": str
    }
    job_data: {
        "required_skills": list[str],
        "experience_years": float,
        "clean_text": str
    }
    """
    
    # 1. Semantic Similarity (50%)
    cand_text = candidate_data.get("clean_text", "")
    job_text = job_data.get("clean_text", "")
    semantic_score = embedding_engine.compute_similarity(cand_text, job_text) 
    # normalize relu
    semantic_score = max(0.0, semantic_score)
    
    # 2. Skill Match (30%)
    skill_score = calculate_skill_match(
        candidate_data.get("skills", []),
        job_data.get("required_skills", [])
    )
    
    # 3. Experience Match (20%)
    exp_score = calculate_experience_match(
        candidate_data.get("experience_years", 0.0),
        job_data.get("experience_years", 0.0)
    )
    
    # Final Formula
    final_score = (0.5 * semantic_score) + (0.3 * skill_score) + (0.2 * exp_score)
    
    return {
        "final_score": round(final_score, 4),
        "breakdown": {
            "semantic_score": round(semantic_score, 4),
            "skill_score": round(skill_score, 4),
            "experience_score": round(exp_score, 4)
        },
        "explanation": f"Matched {int(skill_score*100)}% of required skills, {'strong' if semantic_score > 0.6 else 'moderate' if semantic_score > 0.4 else 'weak'} semantic text match, and {int(exp_score*100)}% of required experience."
    }
