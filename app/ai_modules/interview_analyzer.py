from __future__ import annotations

from statistics import mean


QUESTION_BANK = {
    "Software Developer": [
        ("Explain a recent application you built and the tradeoffs you made.", "System thinking"),
        ("How do you design and test a REST API?", "Backend fundamentals"),
        ("Describe a time you debugged a complex issue.", "Problem solving"),
    ],
    "Data Analyst": [
        ("How do you validate data quality before analysis?", "Data quality"),
        ("Explain a dashboard you built and what decision it supported.", "Data storytelling"),
        ("When would you choose SQL over Python for analysis?", "Technical judgment"),
    ],
    "MBA Management Roles": [
        ("Describe a situation where you aligned multiple stakeholders.", "Leadership"),
        ("How do you prioritize initiatives with limited resources?", "Decision making"),
        ("What metrics would you monitor in a new business unit?", "Business acumen"),
    ],
}


def generate_questions(role: str) -> list[dict]:
    selected = QUESTION_BANK.get(role, QUESTION_BANK["Software Developer"])
    return [
        {"id": index + 1, "prompt": prompt, "focus_area": focus_area}
        for index, (prompt, focus_area) in enumerate(selected)
    ]


def analyze_answer(role: str, question: str, answer: str) -> dict:
    words = answer.split()
    answer_length = len(words)
    filler_words = {"um", "uh", "like", "basically", "actually"}
    filler_count = sum(1 for word in words if word.lower().strip(",.!?") in filler_words)
    role_keywords = {token.lower() for token in role.replace("/", " ").split()} | {token.lower() for token in question.split() if len(token) > 4}
    keyword_hits = sum(1 for keyword in role_keywords if keyword in answer.lower())

    confidence = min(100.0, round((answer_length / 80) * 100, 2))
    clarity = max(35.0, round(100 - filler_count * 8, 2))
    relevance = min(100.0, round((keyword_hits / max(len(role_keywords), 1)) * 150, 2))
    communication = round(mean([confidence, clarity, relevance]), 2)

    strengths = []
    weaknesses = []
    suggestions = []

    if answer_length >= 60:
        strengths.append("Your answer had enough detail to demonstrate experience.")
    else:
        weaknesses.append("Your answer is too brief to show depth and impact.")
        suggestions.append("Use the STAR structure and include outcome metrics.")

    if filler_count <= 1:
        strengths.append("Your response reads as composed and confident.")
    else:
        weaknesses.append("Filler words reduce clarity and executive presence.")
        suggestions.append("Pause between points instead of filling silence.")

    if relevance >= 55:
        strengths.append("You addressed the job context and question intent.")
    else:
        weaknesses.append("The response is not tightly aligned with the role requirements.")
        suggestions.append("Reference role-specific tools, decisions, and measurable outcomes.")

    return {
        "confidence": confidence,
        "clarity": clarity,
        "relevance": relevance,
        "communication": communication,
        "strengths": strengths or ["You maintained a usable baseline response."],
        "weaknesses": weaknesses or ["Continue sharpening examples with stronger metrics."],
        "improvement_suggestions": suggestions or ["Practice concise storytelling with quantified impact."],
    }
