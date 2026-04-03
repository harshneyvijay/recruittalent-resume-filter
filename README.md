# RecruitTalent - AI Resume Analyzer

An AI-powered resume screening tool that ranks candidates against a job description using semantic similarity, skill matching, experience extraction, and education scoring.

Built with Flask, scikit-learn, and a custom multi-factor scoring engine.

---

## What it does

Paste a job description, upload multiple resumes (PDF or TXT), and get an instant ranked leaderboard of candidates with a breakdown of why each one scored the way they did.

Each resume is evaluated across four dimensions:

| Factor | Weight | How |
|---|---|---|
| Semantic Similarity | 45% | TF-IDF vectors + cosine similarity |
| Skill Matching | 30% | Regex-based skill extraction with must-have penalty |
| Experience | 15% | Regex year extraction, normalized to 8yr benchmark |
| Education | 10% | Degree keyword detection |

---

## Tech stack

- **Backend** — Flask, scikit-learn, pypdf
- **Frontend** — Vanilla JS, Chart.js, jsPDF
- **Deployment** — Render (Gunicorn)

---

## Running locally
```bash
git clone https://github.com/harshneyvijay/recruittalent-resume-filter.git
cd resume-filter

python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

Create a `.env` file:
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=true

Generate a secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Run:
```bash
python app.py
```

Open `http://localhost:8000`

---

## Project structure
resume-filter/
├── api/
├── models/
│   └── embedding_model.py      # TF-IDF vectorizer
├── services/
│   └── similarity_service.py   # scoring engine
├── utils/
│   ├── pdf_extractor.py        # PDF + TXT parsing
│   └── skill_extractor.py      # skill + experience extraction
├── templates/
│   └── index.html
├── static/
│   ├── css/style.css
│   └── js/script.js
├── config.py
├── app.py
├── Procfile
├── render.yaml
└── requirements.txt

---

## Extending the skill database

Add skills to `utils/skills.json` (auto-loaded if present):
```json
{
    "rust": ["rust"],
    "kubernetes": ["kubernetes", "k8s"],
    "llm": ["llm", "large language model"]
}
```

---

## Deployment

Deployed on Render. Auto-deploys on every push to `main`.

Live: [https://recruittalent-resume-filter.onrender.com]



## License

MIT
