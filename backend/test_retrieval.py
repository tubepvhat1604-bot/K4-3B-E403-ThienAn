import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

try:
    from .retrieval import SemanticRetriever
except ImportError:  # Allows `python -m unittest test_retrieval.py` inside backend.
    from retrieval import SemanticRetriever


MODEL_PATCH_TARGET = f"{SemanticRetriever.__module__}.SentenceTransformer"


CSV_FIELDS = [
    "turn_id", "cohort_hint", "is_preset", "student_question", "tutor_reply",
    "lecture_title", "lecture_code", "course_id", "has_citation",
]


class FakeSentenceTransformer:
    """Deterministic vectors that test grouping without downloading a model."""

    def __init__(self, model_name):
        self.model_name = model_name

    def encode(self, values, **_kwargs):
        vectors = []
        for value in values:
            text = value.lower()
            if "tool" in text or "agent" in text:
                vectors.append([1.0, 0.0, 0.0])
            elif "llm" in text:
                vectors.append([0.0, 1.0, 0.0])
            else:
                vectors.append([0.0, 0.0, 1.0])
        return np.asarray(vectors, dtype=np.float32)


def turn(**updates):
    values = {
        "turn_id": "T00001",
        "cohort_hint": "K4",
        "is_preset": "False",
        "student_question": "Khi nào agent cần gọi tool?",
        "tutor_reply": "Agent gọi tool khi cần dữ liệu bên ngoài.",
        "lecture_title": "AI Agent",
        "lecture_code": "D03",
        "course_id": "K4P1",
        "has_citation": "True",
    }
    values.update(updates)
    return values


class SemanticRetrieverTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        self.data_path = root / "tutor_turns.csv"
        self.embeddings_path = root / "cache" / "embeddings.npy"
        self.metadata_path = root / "cache" / "embeddings.meta.json"
        with self.data_path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(
                [
                    turn(),
                    turn(
                        turn_id="T00002",
                        student_question="Tool Calling giúp agent làm gì?",
                    ),
                    turn(
                        turn_id="T00003",
                        lecture_title="LLM Foundation",
                        lecture_code="D01",
                        student_question="LLM là gì?",
                    ),
                    turn(turn_id="T00004", cohort_hint="K3"),
                    turn(turn_id="T00005", is_preset="True"),
                    turn(turn_id="T00006", student_question=""),
                ]
            )

    def tearDown(self):
        self.temp_dir.cleanup()

    def retriever(self):
        return SemanticRetriever(
            data_path=self.data_path,
            embeddings_path=self.embeddings_path,
            metadata_path=self.metadata_path,
            model_name="fake-model",
            similarity_threshold=0.5,
        )

    @patch(MODEL_PATCH_TARGET, FakeSentenceTransformer)
    def test_filters_k4_and_groups_sources(self):
        retriever = self.retriever()
        retriever.initialize()

        self.assertEqual(retriever.document_count, 3)
        self.assertEqual(retriever.source_count, 2)
        hits = retriever.search("Tool Calling là gì?", top_k=2)

        self.assertEqual(hits[0].course_id, "K4P1")
        self.assertEqual(hits[0].lecture_code, "D03")
        self.assertEqual(hits[0].lecture_title, "AI Agent")
        self.assertIn(
            hits[0].matched_question,
            {"Khi nào agent cần gọi tool?", "Tool Calling giúp agent làm gì?"},
        )
        self.assertEqual(hits[0].rank, 1)

    @patch(MODEL_PATCH_TARGET, FakeSentenceTransformer)
    def test_low_confidence_returns_no_source_and_cache_is_created(self):
        retriever = self.retriever()
        retriever.initialize()
        self.assertTrue(self.embeddings_path.exists())
        self.assertTrue(self.metadata_path.exists())
        self.assertEqual(retriever.search("Blockchain là gì?", top_k=2), [])


if __name__ == "__main__":
    unittest.main()
