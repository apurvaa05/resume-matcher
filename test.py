from components.parser import extract_text_from_input
from components.analyzer import get_skill_gap
from components.matcher import get_match_score

resume = """
Experienced Python developer with strong SQL and Pandas skills.
Built machine learning models using TensorFlow and scikit-learn.
Familiar with Git and Linux environments.
"""

jd = """
Looking for a Python developer with experience in SQL, Docker,
Kubernetes, TensorFlow, FastAPI and MLflow. AWS experience preferred.
"""

gap   = get_skill_gap(resume, jd)
score = get_match_score(resume, jd)

print("Overall score :", score, "%")
print("Skill match   :", gap["match_pct"], "%")
print("Matched       :", gap["matched"])
print("Missing       :", gap["missing"])