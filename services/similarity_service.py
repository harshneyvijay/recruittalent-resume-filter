from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
from utils.skill_extractor import extract_skills, extract_important_skills, extract_experience

MAX_EXP_YEARS = 8

WEIGHTS = {
    "similarity": 0.45,
    "skills":     0.30,
    "experience": 0.15,
    "education":  0.10,
}

EDU_KEYWORDS = ["btech", "mtech", "bsc", "msc", "mba", "phd", "bachelor", "master", "degree"]


class SimilarityService:
    def __init__(self, embedding_model):
        self.model = embedding_model

    def rank_resumes(self, job_description, resumes):
        texts = [r["text"].strip() if r["text"].strip() else "empty" for r in resumes]

        vectors = self.model.encode_all(job_description, texts)
        jd_vec = normalize([vectors[0]])[0]
        resume_vecs = normalize(vectors[1:])

        jd_skills = extract_skills(job_description)
        must_have = extract_important_skills(job_description)

        results = []

        for i, resume in enumerate(resumes):
            text = resume["text"].lower() if resume["text"] else ""

            raw_sim = cosine_similarity([jd_vec], [resume_vecs[i]])[0][0]
            sim_score = round(max(0.0, min(raw_sim, 1.0)) * 100, 2)

            resume_skills = extract_skills(text)
            matched = list(set(jd_skills) & set(resume_skills))
            missing = list(set(jd_skills) - set(resume_skills))

            if jd_skills:
                skill_score = len(matched) / len(jd_skills) * 100
                missing_critical = [s for s in must_have if s not in resume_skills]
                skill_score = max(0, skill_score - len(missing_critical) * 10)
            else:
                skill_score = 0

            skill_score = round(min(skill_score, 100), 2)

            years = extract_experience(text)
            exp_score = round(min((years / MAX_EXP_YEARS) * 100, 100), 2)

            edu_hits = sum(1 for kw in EDU_KEYWORDS if kw in text)
            edu_score = round(min(edu_hits / len(EDU_KEYWORDS) * 100, 100), 2)

            final = (
                sim_score   * WEIGHTS["similarity"] +
                skill_score * WEIGHTS["skills"] +
                exp_score   * WEIGHTS["experience"] +
                edu_score   * WEIGHTS["education"]
            )

            results.append({
                "name": resume["name"],
                "score": round(min(final, 100), 2),
                "similarity": sim_score,
                "skills": skill_score,
                "experience": exp_score,
                "education": edu_score,
                "matched_skills": matched,
                "missing_skills": missing,
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results