import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

<<<<<<< HEAD
st.set_page_config(page_title="History · Resume Matcher Pro",layout="wide")
=======
st.set_page_config(page_title="History · Resume Matcher Pro", layout="wide")
>>>>>>> 6e599cda512daa635d5f6c614ea8ecca991f8be2

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
</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("Resume Matcher Pro")
    st.markdown("---")
    st.page_link("app.py",                label="Dashboard")
    st.page_link("pages/1_Analyzer.py",   label="Analyzer")
    st.page_link("pages/2_History.py",    label="History")
    st.page_link("pages/3_Improve_CV.py", label="Improve CV")
    st.page_link("pages/4_About.py",      label="About")

st.markdown("Analysis History")
<<<<<<< HEAD
st.markdown("#### Track how your resume score improves over time")
=======
st.markdown("Track how your resume score improves over time")
>>>>>>> 6e599cda512daa635d5f6c614ea8ecca991f8be2
st.markdown("---")

def load_history():
    try:
        conn = sqlite3.connect("data/history.db")
        df = pd.read_sql_query("SELECT * FROM analyses ORDER BY id DESC", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

df = load_history()

if df.empty:
    st.info("No analyses yet — go to the Analyzer page to get started!")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div style='background:#1e2130; border-radius:12px; padding:20px;
            text-align:center; border:1px solid #2d3250;'>
            <p style='font-size:2rem; font-weight:700; color:#64ffda; margin:0;'>{len(df)}</p>
            <p style='color:#8892b0; margin:0;'>Total analyses</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div style='background:#1e2130; border-radius:12px; padding:20px;
            text-align:center; border:1px solid #2d3250;'>
            <p style='font-size:2rem; font-weight:700; color:#ffd93d; margin:0;'>{round(df["overall_score"].mean(), 1)}%</p>
            <p style='color:#8892b0; margin:0;'>Average score</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div style='background:#1e2130; border-radius:12px; padding:20px;
            text-align:center; border:1px solid #2d3250;'>
            <p style='font-size:2rem; font-weight:700; color:#c792ea; margin:0;'>{round(df["overall_score"].max(), 1)}%</p>
            <p style='color:#8892b0; margin:0;'>Best score</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if len(df) > 1:
        st.markdown("Score trend over time")
        fig = px.line(
            df.iloc[::-1], x="date", y="overall_score",
            markers=True, line_shape="spline",
            color_discrete_sequence=["#64ffda"]
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#ccd6f6"},
            xaxis=dict(gridcolor="#2d3250", title=""),
            yaxis=dict(gridcolor="#2d3250", range=[0,100], title="Score %"),
            height=300, margin=dict(t=10, b=10)
        )
        fig.update_traces(line_width=2.5, marker_size=8)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("All analyses")
    for _, row in df.iterrows():
        with st.expander(f"{row['date']}  ·  Overall: {row['overall_score']}%  ·  Skills: {row['skill_match']}%"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Matched skills**")
                if row["matched_skills"]:
                    for s in row["matched_skills"].split(", "):
                        st.markdown(f"""<span style='background:#1a3a2a; color:#64ffda;
                            padding:3px 10px; border-radius:20px; font-size:0.8rem;
                            margin:2px; display:inline-block;'>{s}</span>""", unsafe_allow_html=True)
            with col2:
                st.markdown("**Missing skills**")
                if row["missing_skills"]:
                    for s in row["missing_skills"].split(", "):
                        st.markdown(f"""<span style='background:#3a1a1a; color:#ff6b6b;
                            padding:3px 10px; border-radius:20px; font-size:0.8rem;
                            margin:2px; display:inline-block;'>{s}</span>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Clear all history"):
        conn = sqlite3.connect("data/history.db")
        conn.execute("DELETE FROM analyses")
        conn.commit()
        conn.close()
        st.success("History cleared!")
        st.rerun()
