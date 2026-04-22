def find_missing_skills(resume_skills, job_skills):
    missing = [s for s in job_skills if s not in resume_skills]
    matched = [s for s in job_skills if s in resume_skills]
    score = round(len(matched) / len(job_skills) * 100, 1)
    return score, matched, missing

resume = ["Python", "SQL", "Pandas", "TensorFlow"]
job    = ["Python", "SQL", "Docker", "Kubernetes", "FastAPI", "TensorFlow"]

score, matched, missing = find_missing_skills(resume, job)

print("Match score  :", score, "%")
print("Matched      :", matched)
print("Missing      :", missing)