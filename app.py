"""Compatibility entrypoint for `uvicorn app:app --reload` at repository root."""

from backend.app import app

__all__ = ["app"]
