import streamlit as st
from components.parser import extract_text_from_pdf, extract_text_from_input
from components.matcher import get_match_score, get_section_scores
from components.analyzer import get_skill_gap, get_readability_grade

st.set_page_config(
    page_title="Analyzer · Resume Matcher Pro",
    layout="wide"
)

st.markdown("""
<style>
    [data-testid="stSidebarNav"] { display: none; }
    .main { background-color: #0f1117; }
    .upload-box {
        background: #1e2130;
        border: 2px dashed #2d3250;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
    }
    .analyze-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ccd6f6;
        margin-bottom: 8px;
    }
    div[data-testid="stSidebar"] { background: #0d1117; border-right: 1px solid #2d3250; }
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        width: 100%;
    }
    .stButton > button:hover { opacity: 0.85; }
    .stTextArea textarea {
        background: #1e2130 !important;
        color: #ccd6f6 !important;
        border: 1px solid #2d3250 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("Resume Matcher Pro")
    st.markdown("---")
    st.page_link("app.py",                label="Dashboard")
    st.page_link("pages/1_Analyzer.py",   label="Analyzer")
    st.page_link("pages/2_History.py",    label="History")
    st.page_link("pages/3_Improve_CV.py", label="Improve CV")
    st.page_link("pages/4_About.py",      label="About")
    st.markdown("---")
    st.markdown("<p style='color:#8892b0; font-size:0.8rem;'>Built with Python · spaCy · Transformers</p>", unsafe_allow_html=True)

st.markdown("Resume Analyzer")
st.markdown("Upload your resume and paste the job description to get your match score")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("<p class='analyze-header'>Your Resume</p>", unsafe_allow_html=True)
    upload_method = st.radio("Input method", ["Upload PDF", "Paste text"], horizontal=True)

    resume_text = ""
    if upload_method == "Upload PDF":
        uploaded_file = st.file_uploader("Upload your resume", type=["pdf"], label_visibility="collapsed")
        if uploaded_file:
            with st.spinner("Reading PDF..."):
                resume_text = extract_text_from_pdf(uploaded_file)
            st.success(f"Resume loaded — {len(resume_text.split())} words extracted")
            with st.expander("Preview extracted text"):
                st.write(resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text)
    else:
        resume_text = st.text_area(
            "Paste your resume text here",
            height=300,
            placeholder="Copy and paste your full resume text here...",
            label_visibility="collapsed"
        )

with col2:
    st.markdown("<p class='analyze-header'>Job Description</p>", unsafe_allow_html=True)
    jd_text = st.text_area(
        "Paste the job description here",
        height=350,
        placeholder="Copy and paste the full job description here...",
        label_visibility="collapsed"
    )
    if jd_text:
        st.success(f"JD loaded — {len(jd_text.split())} words")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_btn = st.button("Analyze My Resume", use_container_width=True)

if analyze_btn:
    if not resume_text:
        st.error("Please upload or paste your resume first!")
    elif not jd_text:
        st.error("Please paste the job description!")
    elif len(resume_text.split()) < 20:
        st.error("Resume text is too short. Please add more content.")
    else:
        with st.spinner("Running AI analysis... this may take 20-30 seconds"):
            overall      = get_match_score(resume_text, jd_text)
            section_scores = get_section_scores(resume_text, jd_text)
            gap          = get_skill_gap(resume_text, jd_text)
            readability  = get_readability_grade(resume_text)

        st.session_state.analysis = {
            "overall":        overall,
            "skill_match":    gap["match_pct"],
            "matched":        gap["matched"],
            "missing":        gap["missing"],
            "extra":          gap["extra"],
            "section_scores": section_scores,
            "readability":    readability,
            "resume_text":    resume_text,
            "jd_text":        jd_text
        }

        st.success("Analysis complete!")
        st.balloons()

        col1, col2, col3 = st.columns(3)
        with col1:
            color = "#64ffda" if overall >= 70 else "#ffd93d" if overall >= 50 else "#ff6b6b"
            st.markdown(f"""
            <div style='background:#1e2130; border-radius:12px; padding:20px; text-align:center; border:1px solid #2d3250;'>
                <p style='font-size:2.5rem; font-weight:700; color:{color}; margin:0;'>{overall}%</p>
                <p style='color:#8892b0; margin:0;'>Overall match</p>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style='background:#1e2130; border-radius:12px; padding:20px; text-align:center; border:1px solid #2d3250;'>
                <p style='font-size:2.5rem; font-weight:700; color:#64b5f6; margin:0;'>{gap["match_pct"]}%</p>
                <p style='color:#8892b0; margin:0;'>Skill match</p>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style='background:#1e2130; border-radius:12px; padding:20px; text-align:center; border:1px solid #2d3250;'>
                <p style='font-size:2.5rem; font-weight:700; color:#c792ea; margin:0;'>{readability}</p>
                <p style='color:#8892b0; margin:0;'>Readability grade</p>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("Matched skills")
            if gap["matched"]:
                for skill in gap["matched"]:
                    st.markdown(f"""<span style='background:#1a3a2a; color:#64ffda; padding:4px 12px;
                        border-radius:20px; font-size:0.85rem; margin:3px; display:inline-block;
                        border:1px solid #64ffda44;'>{skill}</span>""", unsafe_allow_html=True)
            else:
                st.warning("No matching skills found")

        with col2:
            st.markdown("Missing skills")
            if gap["missing"]:
                for skill in gap["missing"]:
                    st.markdown(f"""<span style='background:#3a1a1a; color:#ff6b6b; padding:4px 12px;
                        border-radius:20px; font-size:0.85rem; margin:3px; display:inline-block;
                        border:1px solid #ff6b6b44;'>{skill}</span>""", unsafe_allow_html=True)
            else:
                st.success("No missing skills — great match!")

        st.markdown("<br>", unsafe_allow_html=True)
<<<<<<< HEAD
        st.info("Go to **Dashboard** to see the full breakdown with charts!")
=======
        st.info("Go to **Dashboard** to see the full breakdown with charts!")
>>>>>>> 6e599cda512daa635d5f6c614ea8ecca991f8be2
