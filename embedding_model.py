from sklearn.feature_extraction.text import TfidfVectorizer


class EmbeddingModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),   # catches "machine learning" as a phrase, not just individual words
            stop_words="english",
            min_df=1,
        )

    def encode_all(self, job_desc, resume_texts):
        corpus = [job_desc] + resume_texts
        vectors = self.vectorizer.fit_transform(corpus).toarray()
        return vectors
