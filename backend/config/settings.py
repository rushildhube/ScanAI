import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # App
    APP_NAME = "Dental Disease Classifier"
    SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key")
    ALGORITHM = "HS256"

    # Database
    MONGO_DB_URL = os.getenv("MONGO_DB_URL", "mongodb://localhost:27017/")
    MONGO_DB_NAME = "dental_app_db"

    # OAuth
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    FACEBOOK_CLIENT_ID = os.getenv("FACEBOOK_CLIENT_ID")
    FACEBOOK_CLIENT_SECRET = os.getenv("FACEBOOK_CLIENT_SECRET")

    # Email
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    # Paths
    UPLOADS_DIR = "uploads"
    REPORTS_DIR = "reports"
    MODEL_PATH = "D:/Teeth Disease Classification Dental/backend/model/final_model.pth"
    CLASSES_PATH = "D:/Teeth Disease Classification Dental/backend/model/class_names.json"

settings = Settings()