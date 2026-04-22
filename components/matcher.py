from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

def get_match_score(resume_text, jd_text):
    model = load_model()
    embeddings = model.encode([resume_text, jd_text])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return round(float(score) * 100, 1)

def get_section_scores(resume_text, jd_text):
    model = load_model()
    sections = {
        "Skills match":      jd_text[:len(jd_text)//3],
        "Experience match":  jd_text[len(jd_text)//3 : 2*len(jd_text)//3],
        "Overall relevance": jd_text
    }
    scores = {}
    for label, chunk in sections.items():
        emb = model.encode([resume_text, chunk])
        scores[label] = round(float(cosine_similarity([emb[0]], [emb[1]])[0][0]) * 100, 1)
    return scores