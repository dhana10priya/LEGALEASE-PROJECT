"""Central configuration for LegalEase."""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
# Spec model is gemini-1.5-pro. Google retires older models over time,
# so override via GEMINI_MODEL in .env if you get a "model not found" error.
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

LOGO_PATH = BASE_DIR / "Image" / "Logo.png"            # light bg (docx/pdf)
WEB_LOGO_PATH = BASE_DIR / "Image" / "inverseLogo.png"  # dark bg (web UI)
FOOTER_TEXT = "LegalEase Inc. | contact@legalease.com | All Rights Reserved."
