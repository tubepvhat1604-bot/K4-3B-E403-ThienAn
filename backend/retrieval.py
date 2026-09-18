"""Embedding-based retrieval over anonymized VLearn tutor turns."""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# This MVP uses the PyTorch backend supplied with sentence-transformers. The
# host environment may also contain Keras 3, which older Transformers releases
# cannot import; disabling the unused TensorFlow integration keeps startup
# deterministic without adding a TensorFlow dependency.
os.environ.setdefault("USE_TF", "0")
from sentence_transformers import SentenceTransformer

try:  # Supports both package imports and `cd backend` CLI execution.
    from .config import (
        CACHE_METADATA_PATH,
        CANDIDATE_MULTIPLIER,
        DATA_PATH,
        EMBEDDINGS_PATH,
        MAX_TOP_K,
        MODEL_NAME,
        SIMILARITY_THRESHOLD,
        TARGET_COHORT,
    )
except ImportError:  # pragma: no cover - exercised by the documented CLI form.
    from config import (
        CACHE_METADATA_PATH,
        CANDIDATE_MULTIPLIER,
        DATA_PATH,
        EMBEDDINGS_PATH,
        MAX_TOP_K,
        MODEL_NAME,
        SIMILARITY_THRESHOLD,
        TARGET_COHORT,
    )


REQUIRED_COLUMNS = {
    "turn_id",
    "cohort_hint",
    "is_preset",
    "student_question",
    "tutor_reply",
    "lecture_title",
    "lecture_code",
    "course_id",
    "has_citation",
}
CACHE_SCHEMA_VERSION = 1


class RetrievalError(RuntimeError):
    """Raised when the local corpus or its semantic index cannot be used."""


@dataclass(frozen=True)
class SearchHit:
    rank: int
    course_id: str
    lecture_code: str
    lecture_title: str
    score: float
    matched_question: str
    excerpt: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "rank": self.rank,
            "course_id": self.course_id,
            "lecture_code": self.lecture_code,
            "lecture_title": self.lecture_title,
            "score": self.score,
            "matched_question": self.matched_question,
            "excerpt": self.excerpt,
        }


def normalize_text(value: object) -> str:
    """Normalize whitespace without interpreting corpus text as instructions."""
    return re.sub(r"\s+", " ", str(value or "")).strip()


def compact_excerpt(value: str, limit: int = 600) -> str:
    value = normalize_text(value)
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "…"


class SemanticRetriever:
    """Loads K4 questions once and performs cosine similarity at request time."""

    def __init__(
        self,
        *,
        data_path: Path = DATA_PATH,
        embeddings_path: Path = EMBEDDINGS_PATH,
        metadata_path: Path = CACHE_METADATA_PATH,
        model_name: str = MODEL_NAME,
        target_cohort: str = TARGET_COHORT,
        similarity_threshold: float = SIMILARITY_THRESHOLD,
    ) -> None:
        if not 0 <= similarity_threshold <= 1:
            raise ValueError("similarity_threshold phải nằm trong khoảng 0 đến 1.")
        self.data_path = Path(data_path)
        self.embeddings_path = Path(embeddings_path)
        self.metadata_path = Path(metadata_path)
        self.model_name = model_name
        self.target_cohort = target_cohort
        self.similarity_threshold = similarity_threshold
        self.model: SentenceTransformer | None = None
        self.turns = pd.DataFrame()
        self.embeddings = np.empty((0, 0), dtype=np.float32)

    @property
    def document_count(self) -> int:
        return len(self.turns)

    @property
    def source_count(self) -> int:
        if self.turns.empty:
            return 0
        return int(self.turns[["course_id", "lecture_code"]].drop_duplicates().shape[0])

    def initialize(self) -> None:
        self.turns = self._load_turns()
        self.model = SentenceTransformer(self.model_name)
        self.embeddings = self._load_or_build_embeddings()

    def _load_turns(self) -> pd.DataFrame:
        if not self.data_path.is_file():
            raise RetrievalError(
                f"Không tìm thấy tutor_turns.csv tại {self.data_path}. "
                "Đặt file vào backend/data hoặc cấu hình VLEARN_DATA_PATH."
            )

        try:
            data = pd.read_csv(self.data_path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError, pd.errors.ParserError) as error:
            raise RetrievalError(f"Không thể đọc tutor_turns.csv: {error}") from error

        missing = sorted(REQUIRED_COLUMNS - set(data.columns))
        if missing:
            raise RetrievalError("CSV thiếu cột bắt buộc: " + ", ".join(missing))

        for column in data.columns:
            data[column] = data[column].map(normalize_text)

        is_preset = data["is_preset"].str.casefold().isin({"true", "1", "yes"})
        usable = data[
            (data["cohort_hint"] == self.target_cohort)
            & (~is_preset)
            & data["student_question"].ne("")
            & data["course_id"].ne("")
            & data["lecture_code"].ne("")
            & data["lecture_title"].ne("")
        ].copy()

        if usable.empty:
            raise RetrievalError(
                f"Không có lượt hỏi hợp lệ cho cohort {self.target_cohort} sau khi lọc preset."
            )
        return usable.reset_index(drop=True)

    def _cache_metadata(self) -> dict[str, Any]:
        stat = self.data_path.stat()
        turn_ids = "\n".join(self.turns["turn_id"].tolist()).encode("utf-8")
        return {
            "schema_version": CACHE_SCHEMA_VERSION,
            "model_name": self.model_name,
            "target_cohort": self.target_cohort,
            "source_path": str(self.data_path.resolve()),
            "source_size": stat.st_size,
            "source_mtime_ns": stat.st_mtime_ns,
            "document_count": self.document_count,
            "turn_id_digest": hashlib.sha256(turn_ids).hexdigest(),
        }

    def _cache_is_current(self, expected: dict[str, Any]) -> bool:
        if not self.embeddings_path.is_file() or not self.metadata_path.is_file():
            return False
        try:
            actual = json.loads(self.metadata_path.read_text(encoding="utf-8"))
            return actual == expected
        except (OSError, json.JSONDecodeError):
            return False

    def _load_or_build_embeddings(self) -> np.ndarray:
        expected = self._cache_metadata()
        if self._cache_is_current(expected):
            try:
                cached = np.load(self.embeddings_path, allow_pickle=False)
                if cached.ndim == 2 and cached.shape[0] == self.document_count:
                    return cached.astype(np.float32, copy=False)
            except (OSError, ValueError):
                pass

        if self.model is None:
            raise RetrievalError("Embedding model chưa được khởi tạo.")
        embeddings = self.model.encode(
            self.turns["student_question"].tolist(),
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        ).astype(np.float32, copy=False)
        self._write_cache(embeddings, expected)
        return embeddings

    def _write_cache(self, embeddings: np.ndarray, metadata: dict[str, Any]) -> None:
        self.embeddings_path.parent.mkdir(parents=True, exist_ok=True)
        self.metadata_path.parent.mkdir(parents=True, exist_ok=True)
        embeddings_tmp = self.embeddings_path.with_suffix(".tmp")
        metadata_tmp = self.metadata_path.with_suffix(".tmp")
        try:
            with embeddings_tmp.open("wb") as file:
                np.save(file, embeddings)
            metadata_tmp.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
            os.replace(embeddings_tmp, self.embeddings_path)
            os.replace(metadata_tmp, self.metadata_path)
        finally:
            embeddings_tmp.unlink(missing_ok=True)
            metadata_tmp.unlink(missing_ok=True)

    def search(self, query: str, top_k: int) -> list[SearchHit]:
        query = normalize_text(query)
        if not query:
            raise ValueError("query không được để trống.")
        if self.model is None or self.embeddings.size == 0:
            raise RetrievalError("Semantic index chưa sẵn sàng.")
        if not 1 <= top_k <= MAX_TOP_K:
            raise ValueError(f"top_k phải nằm trong khoảng 1–{MAX_TOP_K}.")

        query_embedding = self.model.encode(
            [query], convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False
        )[0].astype(np.float32, copy=False)
        similarities = self.embeddings @ query_embedding
        candidate_count = min(len(similarities), max(top_k * CANDIDATE_MULTIPLIER, top_k))
        candidate_indexes = np.argpartition(similarities, -candidate_count)[-candidate_count:]
        candidate_indexes = candidate_indexes[np.argsort(similarities[candidate_indexes])[::-1]]

        grouped: dict[tuple[str, str], list[tuple[float, int]]] = {}
        for index in candidate_indexes:
            similarity = float(similarities[index])
            if similarity < self.similarity_threshold:
                continue
            turn = self.turns.iloc[int(index)]
            source_key = (turn["course_id"], turn["lecture_code"])
            grouped.setdefault(source_key, []).append((similarity, int(index)))

        ranked_sources: list[tuple[float, float, int, tuple[str, str]]] = []
        for source_key, matches in grouped.items():
            matches.sort(key=lambda item: item[0], reverse=True)
            best_similarity = matches[0][0]
            support = min(len(matches), 3)
            # Multiple independent, similar questions pointing to the same source
            # increase confidence without allowing count to dominate semantic fit.
            aggregate_score = min(1.0, best_similarity * (1 + 0.04 * (support - 1)))
            ranked_sources.append((aggregate_score, best_similarity, matches[0][1], source_key))

        ranked_sources.sort(key=lambda item: (item[0], item[1]), reverse=True)
        hits: list[SearchHit] = []
        for rank, (score, _, best_index, _) in enumerate(ranked_sources[:top_k], start=1):
            turn = self.turns.iloc[best_index]
            hits.append(
                SearchHit(
                    rank=rank,
                    course_id=turn["course_id"],
                    lecture_code=turn["lecture_code"],
                    lecture_title=turn["lecture_title"],
                    score=round(float(score), 4),
                    matched_question=compact_excerpt(turn["student_question"], 420),
                    excerpt=compact_excerpt(turn["tutor_reply"]),
                )
            )
        return hits
