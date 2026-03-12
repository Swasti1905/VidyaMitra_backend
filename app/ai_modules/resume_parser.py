from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from pypdf import PdfReader

from app.ai_modules.datasets import load_role_skill_matrix

try:
    import spacy

    NLP = spacy.blank("en")
except Exception:
    NLP = None


SECTION_HEADERS = {
    "education": ["education", "academics", "qualifications"],
    "experience": ["experience", "work experience", "employment history"],
    "projects": ["projects", "project experience"],
    "certifications": ["certifications", "licenses"]
}

SOFT_SKILLS = {
    "communication",
    "leadership",
    "teamwork",
    "problem solving",
    "adaptability",
    "critical thinking",
    "time management",
    "presentation",
}


def extract_text(file_path: Path) -> str:
    if file_path.suffix.lower() == ".pdf":
        reader = PdfReader(str(file_path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if file_path.suffix.lower() == ".docx":
        document = Document(str(file_path))
        return "\n".join(paragraph.text for paragraph in document.paragraphs)
    raise ValueError("Unsupported resume format")


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _build_skill_lexicon() -> set[str]:
    lexicon = set(SOFT_SKILLS)
    for role_data in load_role_skill_matrix().values():
        lexicon.update(skill.lower() for skill in role_data["required_skills"])
    lexicon.update({"html", "css", "react", "fastapi", "sqlalchemy", "jwt", "statistics", "pandas"})
    return lexicon


def parse_sections(text: str) -> dict[str, list[str]]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    sections = {key: [] for key in SECTION_HEADERS}
    current_section = None

    for line in lines:
        lowered = line.lower()
        matched_section = next(
            (key for key, aliases in SECTION_HEADERS.items() if lowered in aliases or lowered.rstrip(":") in aliases),
            None,
        )
        if matched_section:
            current_section = matched_section
            continue
        if current_section:
            sections[current_section].append(line)

    return sections


def extract_skills(text: str) -> tuple[list[str], list[str]]:
    normalized = text.lower()
    lexicon = _build_skill_lexicon()
    detected = sorted({skill.title() if skill not in {"sql", "html", "css", "jwt"} else skill.upper() for skill in lexicon if skill in normalized})
    soft = sorted({skill.title() for skill in SOFT_SKILLS if skill in normalized})

    if NLP is not None:
        doc = NLP(_normalize_text(text))
        noun_chunks = {token.text.lower() for token in doc if token.pos_ in {"NOUN", "PROPN"}}
        for item in noun_chunks:
            if item in lexicon and item.title() not in detected:
                detected.append(item.title())

    detected = sorted(dict.fromkeys(detected))
    return detected, soft


def parse_resume(file_path: Path) -> dict:
    raw_text = extract_text(file_path)
    sections = parse_sections(raw_text)
    extracted_skills, soft_skills = extract_skills(raw_text)
    return {
        "raw_text": raw_text,
        "sections": sections,
        "extracted_skills": extracted_skills,
        "soft_skills": soft_skills,
    }
