from __future__ import annotations

from functools import lru_cache

from app.ai_modules.datasets import load_role_skill_matrix

try:
    from sentence_transformers import SentenceTransformer, util
except Exception:
    SentenceTransformer = None
    util = None


@lru_cache
def get_encoder():
    if SentenceTransformer is None:
        return None
    try:
        return SentenceTransformer("all-MiniLM-L6-v2")
    except Exception:
        return None


def rank_topics_with_semantics(role: str, missing_skills: list[str], learning_topics: list[str]) -> list[str]:
    encoder = get_encoder()
    if encoder is None or util is None or not learning_topics:
        return learning_topics

    reference_text = f"{role}: {' '.join(missing_skills)}"
    reference_embedding = encoder.encode(reference_text, convert_to_tensor=True)
    topic_embeddings = encoder.encode(learning_topics, convert_to_tensor=True)
    scores = util.cos_sim(reference_embedding, topic_embeddings)[0]
    ranked = sorted(zip(learning_topics, scores.tolist()), key=lambda item: item[1], reverse=True)
    return [topic for topic, _ in ranked]


def analyze_skill_gap(role: str, current_skills: list[str]) -> dict:
    role_matrix = load_role_skill_matrix()
    if role not in role_matrix:
        raise KeyError(f"Unknown role: {role}")

    current = {skill.strip().lower() for skill in current_skills}
    required_skills = role_matrix[role]["required_skills"]
    required_normalized = {skill.lower(): skill for skill in required_skills}

    matched = [original for normalized, original in required_normalized.items() if normalized in current]
    missing = [original for normalized, original in required_normalized.items() if normalized not in current]
    readiness_score = round((len(matched) / max(len(required_skills), 1)) * 100, 2)

    ranked_topics = rank_topics_with_semantics(role, missing, role_matrix[role]["learning_topics"])

    return {
        "role": role,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommended_topics": ranked_topics,
        "improvement_suggestions": [
            f"Build 1 project covering {topic.lower()}" for topic in ranked_topics[:2]
        ] + [
            "Document measurable impact in your resume",
            "Practice explaining your strongest projects with metrics",
        ],
        "readiness_score": readiness_score,
    }

