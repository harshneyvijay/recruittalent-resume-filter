import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    MAX_FILE_SIZE_MB = 10
    ALLOWED_EXTENSIONS = {".pdf", ".txt"}
    DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"