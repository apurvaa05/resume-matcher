import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sqlite3
from datetime import datetime

st.set_page_config(
    page_title="Resume Matcher Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    [data-testid="stSidebarNav"] { display: none; }
    .main { background-color: #0f1117; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #252a3d);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #2d3250;
        text-align: center;
    }
    .metric-value { font-size: 2.5rem; font-weight: 700; margin: 0; }
    .metric-label { font-size: 0.85rem; color: #8892b0; margin: 0; }
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ccd6f6;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid #2d3250;
    }
    .skill-chip {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 3px;
        font-weight: 500;
    }
    .matched { background: #1a3a2a; color: #64ffda; border: 1px solid #64ffda44; }
    .missing { background: #3a1a1a; color: #ff6b6b; border: 1px solid #ff6b6b44; }
    .extra   { background: #1a2a3a; color: #64b5f6; border: 1px solid #64b5f644; }
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
</style>
""", unsafe_allow_html=True)

def init_db():
    conn = sqlite3.connect("data/history.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            overall_score REAL,
            skill_match REAL,
            matched_skills TEXT,
            missing_skills TEXT,
            readability TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(overall, skill_match, matched, missing, readability):
    conn = sqlite3.connect("data/history.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO analyses (date, overall_score, skill_match, matched_skills, missing_skills, readability)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        overall, skill_match,
        ", ".join(matched),
        ", ".join(missing),
        readability
    ))
    conn.commit()
    conn.close()

def load_history():
    conn = sqlite3.connect("data/history.db")
    df = pd.read_sql_query("SELECT * FROM analyses ORDER BY id DESC", conn)
    conn.close()
    return df

def make_gauge(score, title):
    color = "#64ffda" if score >= 70 else "#ffd93d" if score >= 50 else "#ff6b6b"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": title, "font": {"color": "#ccd6f6", "size": 14}},
        number={"suffix": "%", "font": {"color": color, "size": 28}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#8892b0"},
            "bar": {"color": color},
            "bgcolor": "#1e2130",
            "bordercolor": "#2d3250",
            "steps": [
                {"range": [0, 50],   "color": "#3a1a1a"},
                {"range": [50, 70],  "color": "#3a3a1a"},
                {"range": [70, 100], "color": "#1a3a2a"},
            ],
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=200,
        margin=dict(t=40, b=10, l=20, r=20)
    )
    return fig

init_db()

with st.spinner("⚡ Loading AI model — one moment..."):
    from components.matcher import load_model
    from components.analyzer import load_nlp
    load_model()
    load_nlp()

with st.sidebar:
    st.markdown("Resume Matcher Pro")
    st.markdown("---")
    st.markdown("### Navigation")
    st.page_link("app.py",                label="Dashboard")
    st.page_link("pages/1_Analyzer.py",   label="Analyzer")
    st.page_link("pages/2_History.py",    label="History")
    st.page_link("pages/3_Improve_CV.py", label="Improve CV")
    st.page_link("pages/4_About.py",      label="About")
    st.markdown("---")
    st.markdown("<p style='color:#8892b0; font-size:0.8rem;'>Built with Python · spaCy · Transformers</p>", unsafe_allow_html=True)

if "analysis" not in st.session_state:
    st.markdown("Resume Matcher Pro")
<<<<<<< HEAD
    st.markdown("AI-powered resume analysis — find your match score instantly")
=======
    st.markdown("#### AI-powered resume analysis — find your match score instantly")
>>>>>>> 6e599cda512daa635d5f6c614ea8ecca991f8be2
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class='metric-card'>
            <p class='metric-value' style='color:#64ffda;'>AI</p>
            <p class='metric-label'>Powered matching engine</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='metric-card'>
            <p class='metric-value' style='color:#ffd93d;'>NLP</p>
            <p class='metric-label'>Deep text understanding</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class='metric-card'>
            <p class='metric-value' style='color:#ff6b6b;'>Live</p>
            <p class='metric-label'>Real-time skill gap analysis</p>
        </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("Go to **Analyzer** in the sidebar to upload your resume and start!")

else:
    a = st.session_state.analysis
    st.markdown("Dashboard")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        color = "#64ffda" if a["overall"] >= 70 else "#ffd93d" if a["overall"] >= 50 else "#ff6b6b"
        st.markdown(f"""<div class='metric-card'>
            <p class='metric-value' style='color:{color};'>{a["overall"]}%</p>
            <p class='metric-label'>Overall match score</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class='metric-card'>
            <p class='metric-value' style='color:#64b5f6;'>{a["skill_match"]}%</p>
            <p class='metric-label'>Skill match</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class='metric-card'>
            <p class='metric-value' style='color:#ffd93d;'>{len(a["matched"])}/{len(a["matched"])+len(a["missing"])}</p>
            <p class='metric-label'>Skills matched</p>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class='metric-card'>
            <p class='metric-value' style='color:#c792ea;'>{a["readability"]}</p>
            <p class='metric-label'>Readability grade</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(make_gauge(a["overall"], "Overall Match"), use_container_width=True)
    with col2:
        st.plotly_chart(make_gauge(a["skill_match"], "Skill Match"), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<p class='section-header'>Matched skills</p>", unsafe_allow_html=True)
        if a["matched"]:
            chips = "".join([f"<span class='skill-chip matched'>{s}</span>" for s in a["matched"]])
            st.markdown(chips, unsafe_allow_html=True)
        else:
            st.warning("No matching skills found.")

    with col2:
        st.markdown("<p class='section-header'>Missing skills — add these to your resume</p>", unsafe_allow_html=True)
        if a["missing"]:
            chips = "".join([f"<span class='skill-chip missing'>{s}</span>" for s in a["missing"]])
            st.markdown(chips, unsafe_allow_html=True)
        else:
            st.success("No missing skills!")

    if a["section_scores"]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p class='section-header'>Section breakdown</p>", unsafe_allow_html=True)
        labels = list(a["section_scores"].keys())
        values = list(a["section_scores"].values())
        fig = px.bar(
            x=values, y=labels, orientation="h",
            color=values, color_continuous_scale=["#ff6b6b","#ffd93d","#64ffda"],
            range_color=[0,100], text=[f"{v}%" for v in values]
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color":"#ccd6f6"},
            coloraxis_showscale=False,
            height=220,
            margin=dict(t=10, b=10, l=10, r=10),
            xaxis=dict(range=[0,100], gridcolor="#2d3250"),
            yaxis=dict(gridcolor="#2d3250")
        )
        fig.update_traces(textposition="outside", marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    save_to_db(a["overall"], a["skill_match"], a["matched"], a["missing"], a["readability"])
<<<<<<< HEAD
    st.success("Analysis saved to history!")
=======
    st.success("✅ Analysis saved to history!")
>>>>>>> 6e599cda512daa635d5f6c614ea8ecca991f8be2
