import os
import logging
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from config import Config
from models.embedding_model import EmbeddingModel
from services.similarity_service import SimilarityService
from utils.pdf_extractor import extract_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

embedding_model = EmbeddingModel()
similarity_service = SimilarityService(embedding_model)


def allowed(filename):
    return Path(filename).suffix.lower() in app.config["ALLOWED_EXTENSIONS"]


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(429)
def rate_limited(e):
    return jsonify({"error": "Too many requests, slow down"}), 429

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Something went wrong"}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        job_description = request.form.get("job_description", "").strip()
        files = request.files.getlist("resumes")

        if not job_description:
            return jsonify({"error": "Job description is empty"}), 400

        if len(job_description) > 10000:
            return jsonify({"error": "Job description too long"}), 400

        if not files or files[0].filename == "":
            return jsonify({"error": "No resumes uploaded"}), 400

        resumes = []

        for file in files:
            if not allowed(file.filename):
                return jsonify({"error": f"{file.filename} is not supported"}), 400

            file.seek(0, 2)
            size_mb = file.tell() / (1024 * 1024)
            file.seek(0)

            if size_mb > app.config["MAX_FILE_SIZE_MB"]:
                return jsonify({"error": f"{file.filename} is too large"}), 400

            safe_name = secure_filename(file.filename)
            text = extract_text(file) or ""
            resumes.append({"name": safe_name, "text": text})

        ranked = similarity_service.rank_resumes(job_description, resumes)
        return jsonify(ranked)

    except Exception as e:
        logger.error("Analyze failed: %s", str(e), exc_info=True)
        return jsonify({"error": "Server failed"}), 500


if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    if os.environ.get("RENDER"):
        # on render, gunicorn handles this — this block won't run
        pass
    else:
        from waitress import serve
        serve(app, host="0.0.0.0", port=8000)