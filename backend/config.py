"""Runtime configuration for the semantic retrieval MVP."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


BACKEND_DIR = Path(__file__).resolve().parent
# Keep local configuration beside the backend so the service works whether it
# is launched from the repository root or from ``backend``.
# Existing process environment variables deliberately take precedence.
load_dotenv(BACKEND_DIR / ".env", override=False)
DEFAULT_DATA_PATH = BACKEND_DIR / "data" / "tutor_turns.csv"


def _csv_env(name: str, default: tuple[str, ...]) -> list[str]:
    configured = os.getenv(name)
    if not configured:
        return list(default)
    return [value.strip() for value in configured.split(",") if value.strip()]


DATA_PATH = Path(os.getenv("VLEARN_DATA_PATH", DEFAULT_DATA_PATH))
CACHE_DIR = Path(os.getenv("VLEARN_CACHE_DIR", BACKEND_DIR / "cache"))
EMBEDDINGS_PATH = CACHE_DIR / "embeddings.npy"
CACHE_METADATA_PATH = CACHE_DIR / "embeddings.meta.json"

MODEL_NAME = os.getenv(
    "VLEARN_EMBEDDING_MODEL",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
)
TARGET_COHORT = os.getenv("VLEARN_TARGET_COHORT", "K4")
SIMILARITY_THRESHOLD = float(os.getenv("VLEARN_SIMILARITY_THRESHOLD", "0.60"))
DEFAULT_TOP_K = int(os.getenv("VLEARN_DEFAULT_TOP_K", "5"))
MAX_TOP_K = int(os.getenv("VLEARN_MAX_TOP_K", "10"))
CANDIDATE_MULTIPLIER = int(os.getenv("VLEARN_CANDIDATE_MULTIPLIER", "8"))

# The key itself is read only by the official OpenAI SDK from OPENAI_API_KEY.
# Keep it in backend/.env or the process environment; never expose it to the UI.
OPENAI_MODEL = os.getenv("VLEARN_AGENT_MODEL", "gpt-5.2")
AGENT_MIN_SCORE = float(os.getenv("VLEARN_AGENT_MIN_SCORE", "0.72"))

# Keep development origins explicit. In production this should be the deployed
# frontend origin, supplied by VLEARN_CORS_ORIGINS.
CORS_ORIGINS = _csv_env(
    "VLEARN_CORS_ORIGINS",
    (
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ),
)
