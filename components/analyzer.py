import streamlit as st
import re

@st.cache_resource(show_spinner=False)
def load_nlp():
    import spacy
    return spacy.load("en_core_web_sm")

COMMON_TECH_SKILLS = [
    "python", "sql", "java", "javascript", "typescript", "c++", "c#", "r",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
    "docker", "kubernetes", "aws", "azure", "gcp", "git", "linux",
    "fastapi", "flask", "django", "react", "node", "mongodb", "postgresql",
    "spark", "hadoop", "tableau", "power bi", "excel", "mlflow",
    "data analysis", "data science", "statistics", "neural networks",
    "transformers", "bert", "llm", "api", "rest", "agile", "scrum"
]

def extract_skills(text):
    text_lower = text.lower()
    found = [skill for skill in COMMON_TECH_SKILLS if skill in text_lower]
    return list(set(found))

def get_skill_gap(resume_text, jd_text):
    resume_skills = extract_skills(resume_text)
    jd_skills     = extract_skills(jd_text)
    matched = [s for s in jd_skills if s in resume_skills]
    missing = [s for s in jd_skills if s not in resume_skills]
    extra   = [s for s in resume_skills if s not in jd_skills]
    match_pct = round(len(matched) / len(jd_skills) * 100, 1) if jd_skills else 0
    return {
        "matched":      matched,
        "missing":      missing,
        "extra":        extra,
        "match_pct":    match_pct,
        "total_jd":     len(jd_skills),
        "total_resume": len(resume_skills)
    }

def get_readability_grade(text):
    sentences = re.split(r'[.!?]', text)
    sentences = [s for s in sentences if len(s.strip()) > 10]
    if not sentences:
        return "N/A"
    avg_len = sum(len(s.split()) for s in sentences) / len(sentences)
    if avg_len < 15:   return "A"
    elif avg_len < 20: return "B+"
    elif avg_len < 25: return "B"
    elif avg_len < 30: return "C+"
    else:              return "C"