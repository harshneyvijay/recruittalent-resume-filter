import re
import json
import os

_default_skills = {
    "python": ["python"],
    "javascript": ["javascript", "js"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "react": ["react", "reactjs"],
    "node": ["node", "nodejs"],
    "tensorflow": ["tensorflow"],
    "keras": ["keras"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "sql": ["sql"],
    "mongodb": ["mongodb"],
    "docker": ["docker"],
    "git": ["git"],
    "aws": ["aws", "amazon web services"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],
    "scikit-learn": ["sklearn", "scikit-learn"],
}

_skills_path = os.path.join(os.path.dirname(__file__), "skills.json")

if os.path.exists(_skills_path):
    with open(_skills_path) as f:
        SKILLS = json.load(f)
else:
    SKILLS = _default_skills


def extract_skills(text):
    text = text.lower()
    found = []

    for skill, variants in SKILLS.items():
        for variant in variants:
            if re.search(r'\b' + re.escape(variant) + r'\b', text):
                found.append(skill)
                break

    return list(set(found))


def extract_important_skills(job_description):
    jd = job_description.lower()
    important = []
    priority_words = ["must", "required", "mandatory", "need", "looking for", "essential"]

    for skill, variants in SKILLS.items():
        for variant in variants:
            for keyword in priority_words:
                if re.search(r'\b' + keyword + r'\s+' + re.escape(variant) + r'\b', jd):
                    important.append(skill)
                    break

    return list(set(important))


def extract_keywords(text):
    return set(re.findall(r'\b\w+\b', text.lower()))


def extract_experience(text):
    text = text.lower()

    matches = re.findall(r'(\d+)\s*\+?\s*(years|yrs|year)', text)
    if matches:
        return max(int(m[0]) for m in matches)

    if "fresher" in text or "no experience" in text:
        return 0

    return 0