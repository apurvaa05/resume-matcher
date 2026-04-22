import streamlit as st

st.set_page_config(page_title="About · Resume Matcher Pro",layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebarNav"] { display: none; }
    .main { background-color: #0f1117; }
    div[data-testid="stSidebar"] { background: #0d1117; border-right: 1px solid #2d3250; }
    .tech-card {
        background: #1e2130;
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid #2d3250;
        margin-bottom: 10px;
    }
</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("Resume Matcher Pro")
    st.markdown("---")
    st.page_link("app.py",                label="Dashboard")
    st.page_link("pages/1_Analyzer.py",   label="Analyzer")
    st.page_link("pages/2_History.py",    label="History")
    st.page_link("pages/3_Improve_CV.py", label="Improve CV")
    st.page_link("pages/4_About.py",      label="About")

st.markdown("About Resume Matcher Pro")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("How it works")
    steps = [
        ("1. PDF Parsing", "PyMuPDF extracts raw text from your resume, cleans whitespace and special characters."),
        ("2. Skill Extraction", "spaCy NLP scans both texts and matches against 40+ known tech skills."),
        ("3. Semantic Matching", "Sentence-transformers converts both texts into high-dimensional vectors and measures cosine similarity."),
        ("4. Gap Analysis", "Skills present in the JD but absent in your resume are flagged as missing."),
        ("5. Score & Report", "All signals are combined into an overall match score with a full breakdown."),
    ]
    for title, desc in steps:
        st.markdown(f"""<div class='tech-card'>
            <strong style='color:#ccd6f6;'>{title}</strong><br>
            <span style='color:#8892b0; font-size:0.9rem;'>{desc}</span>
        </div>""", unsafe_allow_html=True)

with col2:
    st.markdown("Tech stack")
    stack = [
        ("Python 3.12",            "Core programming language"),
        ("Streamlit",              "Web UI framework"),
        ("sentence-transformers",  "ML model for semantic similarity"),
        ("spaCy",                  "NLP for skill extraction"),
        ("PyMuPDF",                "PDF text extraction"),
        ("Plotly",                 "Interactive charts"),
        ("SQLite + Pandas",        "History storage and data handling"),
    ]
    for tech, desc in stack:
        st.markdown(f"""<div class='tech-card'>
            <strong style='color:#64ffda;'>{tech}</strong><br>
            <span style='color:#8892b0; font-size:0.9rem;'>{desc}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("Built by Apurva Dighe")
    st.markdown(f"""<div style='background:#1e2130; border-radius:12px; padding:20px;
        border:1px solid #2d3250; text-align:center;'>
        <p style='font-size:1.2rem; font-weight:600; color:#ccd6f6; margin:0;'>Apurva Dighe</p>
        <p style='color:#8892b0; margin:4px 0 12px;'>AI / ML Developer</p>
        <a href='https://github.com' target='_blank'
            style='background:#667eea; color:white; padding:8px 20px;
            border-radius:8px; text-decoration:none; font-size:0.9rem;'>
            View on GitHub
        </a>
    </div>""", unsafe_allow_html=True)
