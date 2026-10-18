"""
Central configuration for GuestSphere.
Reads all sensitive values from environment variables (.env file).
Never hardcode secrets here.
"""
import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-me")

    # Database: prefer MySQL if DATABASE_URL is provided, else fall back to
    # a local SQLite file so the project runs out of the box for demos.
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "guestsphere.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    APP_NAME = os.environ.get("APP_NAME", "GuestSphere")

    UPLOAD_FOLDER = os.path.join(BASE_DIR, os.environ.get("UPLOAD_FOLDER", "uploads"))
    FACE_DATA_FOLDER = os.path.join(BASE_DIR, os.environ.get("FACE_DATA_FOLDER", "face_data"))
    MODELS_DATA_FOLDER = os.path.join(BASE_DIR, os.environ.get("MODELS_DATA_FOLDER", "models_data"))

    FACE_RECOGNITION_CONFIDENCE_THRESHOLD = float(
        os.environ.get("FACE_RECOGNITION_CONFIDENCE_THRESHOLD", 70)
    )

    QR_SECRET_SALT = os.environ.get("QR_SECRET_SALT", "dev-salt-change-me")

    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8MB max upload
