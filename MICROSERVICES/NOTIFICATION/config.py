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
    "JWT_SECRET_KEY",
    ""
)

JWT_ALGORITHM = "HS256"

# ==================== SERVICE CONFIG ====================
SERVICE_NAME = "NOTIFICATION"
SERVICE_PORT = 8004
SERVICE_HOST = "0.0.0.0"

# Log config
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
