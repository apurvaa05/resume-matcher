import streamlit as st

st.set_page_config(page_title="Improve CV · Resume Matcher Pro", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebarNav"] { display: none; }
    .main { background-color: #0f1117; }
    div[data-testid="stSidebar"] { background: #0d1117; border-right: 1px solid #2d3250; }
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white; border: none; border-radius: 8px;
        padding: 10px 24px; font-weight: 600; width: 100%;
    }
    .tip-card {
        background: #1e2130;
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 3px solid #667eea;
        margin-bottom: 12px;
    }
    .stTextArea textarea {
        background: #1e2130 !important;
        color: #ccd6f6 !important;
        border: 1px solid #2d3250 !important;
        border-radius: 8px !important;
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

st.markdown("Improve Your CV")
<<<<<<< HEAD
st.markdown("Get specific suggestions to boost your match score")
=======
st.markdown("#### Get specific suggestions to boost your match score")
>>>>>>> 6e599cda512daa635d5f6c614ea8ecca991f8be2
st.markdown("---")

if "analysis" not in st.session_state:
    st.info("First go to **Analyzer**, upload your resume and run an analysis — then come back here!")
else:
    a = st.session_state.analysis
    missing = a["missing"]
    matched = a["matched"]

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("What to add to your resume")

        if missing:
            st.markdown("These skills appear in the job description but not in your resume. Add them where relevant:")
            for skill in missing:
                st.markdown(f"""<div class='tip-card'>
                    <strong style='color:#ccd6f6;'>Add: {skill.title()}</strong><br>
                    <span style='color:#8892b0; font-size:0.9rem;'>
                    Mention {skill} in your skills section or describe a project where you used it.
                    Even basic experience counts — be specific about what you built.
                    </span>
                </div>""", unsafe_allow_html=True)
        else:
            st.success("Your resume already covers all skills in the job description!")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("Rewrite a weak section")
        st.markdown("Paste any bullet point from your resume and we'll suggest an improved version:")

        original = st.text_area("Your original bullet point", height=100,
            placeholder="e.g. Worked on machine learning projects using Python...")

        if original and st.button("Improve this bullet point"):
            improved = original.strip()
            if not any(w in improved.lower() for w in ["built", "developed", "designed", "implemented", "created", "led"]):
                improved = "Developed and " + improved[0].lower() + improved[1:]
            if missing:
                improved += f", leveraging {missing[0]} for production deployment"
            if not any(c.isdigit() for c in improved):
                improved += " — improving efficiency by 30%"
            st.markdown("**Suggested rewrite:**")
            st.markdown(f"""<div style='background:#1a3a2a; border-radius:8px; padding:16px;
                border-left:3px solid #64ffda; color:#ccd6f6;'>
                {improved}
            </div>""", unsafe_allow_html=True)
            st.caption("Tip: Quantify your impact with real numbers from your experience for even better results.")

    with col2:
        st.markdown("Your strengths")
        st.markdown("You already have these covered:")
        if matched:
            for skill in matched:
                st.markdown(f"""<span style='background:#1a3a2a; color:#64ffda;
                    padding:4px 12px; border-radius:20px; font-size:0.85rem;
                    margin:3px; display:inline-block;
                    border:1px solid #64ffda44;'>{skill}</span>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 💡 General tips")
        tips = [
            "Use numbers — '30% faster' beats 'improved performance'",
            "Match the exact wording from the job description",
            "Put missing skills in a dedicated Skills section",
            "Keep bullet points under 2 lines each",
            "Lead every bullet with a strong action verb",
        ]
        for tip in tips:
            st.markdown(f"""<div style='background:#1e2130; border-radius:8px;
                padding:10px 14px; margin-bottom:8px; border:1px solid #2d3250;
                color:#8892b0; font-size:0.88rem;'>💡 {tip}</div>""", unsafe_allow_html=True)
