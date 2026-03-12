from __future__ import annotations

from app.ai_modules.datasets import load_role_skill_matrix


def recommend_careers(skills: list[str], interests: list[str]) -> dict:
    role_matrix = load_role_skill_matrix()
    normalized_skills = {skill.lower() for skill in skills}
    normalized_interests = {interest.lower() for interest in interests}
    paths = []

    for role, payload in role_matrix.items():
        required = payload["required_skills"]
        matched_skills = sum(1 for skill in required if skill.lower() in normalized_skills)
        interest_bonus = 1 if any(term in role.lower() for term in normalized_interests) else 0
        score = round(((matched_skills + interest_bonus) / max(len(required), 1)) * 100, 2)
        if matched_skills or interest_bonus:
            paths.append(
                {
                    "title": role,
                    "confidence_score": score,
                    "required_skills": required,
                    "recommended_certifications": payload["certifications"],
                    "learning_roadmap": payload["roadmap"],
                }
            )

    paths.sort(key=lambda item: item["confidence_score"], reverse=True)
    return {"paths": paths[:3] or [
        {
            "title": "Software Developer",
            "confidence_score": 35.0,
            "required_skills": role_matrix["Software Developer"]["required_skills"],
            "recommended_certifications": role_matrix["Software Developer"]["certifications"],
            "learning_roadmap": role_matrix["Software Developer"]["roadmap"],
        }
    ]}
