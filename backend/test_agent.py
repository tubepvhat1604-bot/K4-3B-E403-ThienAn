from types import SimpleNamespace
import unittest
from unittest.mock import Mock

try:
    from .app import NO_ANSWER, SearchRequest, ask_agent
    from .retrieval import SearchHit
except ImportError:  # Allows `python -m unittest test_agent.py` inside backend.
    from app import NO_ANSWER, SearchRequest, ask_agent
    from retrieval import SearchHit


class FakeRetriever:
    def __init__(self, hits):
        self.hits = hits

    def search(self, _query, _top_k):
        return self.hits


def request_with(hits, client=None):
    state = SimpleNamespace(retriever=FakeRetriever(hits), openai_client=client)
    return SimpleNamespace(app=SimpleNamespace(state=state))


def hit(score=0.91):
    return SearchHit(
        rank=1,
        course_id="K4P1",
        lecture_code="D03",
        lecture_title="AI Agent",
        score=score,
        matched_question="Khi nào agent cần gọi tool?",
        excerpt="Agent gọi tool khi cần dữ liệu hoặc hành động bên ngoài.",
    )


class AgentEndpointTests(unittest.TestCase):
    def test_refuses_without_sufficiently_relevant_source(self):
        response = ask_agent(SearchRequest(query="hello"), request_with([]))

        self.assertEqual(response.answer, NO_ANSWER)
        self.assertFalse(response.grounded)
        self.assertEqual(response.sources, [])

    def test_returns_configuration_message_without_api_key(self):
        response = ask_agent(SearchRequest(query="Tool Calling là gì?"), request_with([hit()]))

        self.assertFalse(response.grounded)
        self.assertIn("API key", response.answer)
        self.assertEqual(len(response.results), 1)

    def test_sends_only_grounded_sources_to_openai(self):
        create = Mock(return_value=SimpleNamespace(output_text="Agent gọi tool khi cần dữ liệu bên ngoài. [S1]"))
        client = SimpleNamespace(responses=SimpleNamespace(create=create))

        response = ask_agent(
            SearchRequest(query="Khi nào agent cần gọi tool?"), request_with([hit()], client)
        )

        self.assertTrue(response.grounded)
        self.assertEqual(response.answer, "Agent gọi tool khi cần dữ liệu bên ngoài. [S1]")
        self.assertEqual(len(response.sources), 1)
        self.assertEqual(create.call_args.kwargs["store"], False)
        self.assertIn("[S1] AI Agent", create.call_args.kwargs["input"])


if __name__ == "__main__":
    unittest.main()
