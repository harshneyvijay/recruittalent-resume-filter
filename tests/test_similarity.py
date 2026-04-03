import unittest
from models.embedding_model import EmbeddingModel
from services.similarity_service import SimilarityService


class TestSimilarityService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.model = EmbeddingModel()
        cls.service = SimilarityService(cls.model)

    def test_scores_in_range(self):
        jd = "Looking for a Python developer with machine learning skills."
        resumes = [
            {"name": "good.pdf", "text": "Experienced Python developer skilled in ML and data science."},
            {"name": "bad.pdf",  "text": "Marketing specialist with SEO and branding experience."},
        ]
        for r in self.service.rank_resumes(jd, resumes):
            self.assertGreaterEqual(r["score"], 0)
            self.assertLessEqual(r["score"], 100)

    def test_ranking_order(self):
        jd = "Python machine learning engineer"
        resumes = [
            {"name": "good.pdf", "text": "Python ML engineer with AI experience"},
            {"name": "bad.pdf",  "text": "Graphic designer and illustrator"},
        ]
        results = self.service.rank_resumes(jd, resumes)
        self.assertEqual(results[0]["name"], "good.pdf")

    def test_empty_resume_text(self):
        jd = "Python developer"
        resumes = [
            {"name": "empty.pdf", "text": ""},
            {"name": "good.pdf",  "text": "Python developer with 3 years experience"},
        ]
        results = self.service.rank_resumes(jd, resumes)
        self.assertEqual(len(results), 2)
        good = next(r for r in results if r["name"] == "good.pdf")
        empty = next(r for r in results if r["name"] == "empty.pdf")
        self.assertGreater(good["score"], empty["score"])

    def test_no_skills_in_jd(self):
        jd = "We are looking for a hardworking and motivated individual."
        resumes = [{"name": "r.pdf", "text": "I am hardworking and motivated."}]
        results = self.service.rank_resumes(jd, resumes)
        self.assertEqual(len(results), 1)
        self.assertGreaterEqual(results[0]["score"], 0)

    def test_single_resume(self):
        jd = "Flask backend developer"
        resumes = [{"name": "only.pdf", "text": "Flask developer with REST API experience"}]
        results = self.service.rank_resumes(jd, resumes)
        self.assertEqual(len(results), 1)

    def test_result_keys_present(self):
        jd = "Python developer"
        resumes = [{"name": "r.pdf", "text": "Python and SQL developer"}]
        result = self.service.rank_resumes(jd, resumes)[0]
        for key in ["name", "score", "similarity", "skills", "experience", "education", "matched_skills", "missing_skills"]:
            self.assertIn(key, result)


if __name__ == "__main__":
    unittest.main()