"""
Configuration du service NOTIFICATION
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ==================== GMAIL EMAIL ====================
GMAIL_USER = os.getenv(
    "GMAIL_USER",
    ""
)

GMAIL_APP_PASSWORD = os.getenv(
    "GMAIL_APP_PASSWORD",
    ""
)

EMAIL_FROM_NAME = os.getenv(
    "EMAIL_FROM_NAME",
    "YOK Marketplace"
)

EMAIL_FROM = GMAIL_USER

# ==================== DATABASE ====================
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    ""
)

# ==================== JWT ====================
JWT_SECRET_KEY = os.getenv(
    "AUTH_JWT_SECRET_KEY",
    os.getenv("JWT_SECRET_KEY", "9f3d7c8a2e1b4f6d9c5e3a1b7f4d8c2e9a5b3f6e1d4c8a2f7b5e9c3a1d6f4")
)

JWT_ALGORITHM = os.getenv("AUTH_JWT_ALGORITHM", os.getenv("JWT_ALGORITHM", "HS256"))

# ==================== SERVICE CONFIG ====================
SERVICE_NAME = "NOTIFICATION"
SERVICE_PORT = 8004
SERVICE_HOST = "0.0.0.0"

# Log config
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
