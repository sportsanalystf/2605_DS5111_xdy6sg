"""
Tests for bin/transcript_enricher.py
Uses a dummy MockLLMStrategy so the orchestrator's stream-processing
behavior can be verified without a live network call to any vendor.
"""
import io
import json
import pytest
from bin.llm_strategy import LLMStrategy
from bin.transcript_enricher import TranscriptEnricher


class MockLLMStrategy(LLMStrategy):
    """
    Dummy LLMStrategy for orchestrator tests. Returns a canned enrichment
    payload and lets validate_environment() succeed or fail on demand.
    """

    def __init__(self, should_validate: bool = True):
        self.should_validate = should_validate
        self.enrich_calls = []

    def validate_environment(self) -> None:
        """Raise if should_validate is False."""
        if not self.should_validate:
            raise EnvironmentError("Mock strategy is not configured.")

    def enrich(self, video_id: str, raw_text: str) -> dict:
        """Return canned enrichment payload."""
        self.enrich_calls.append((video_id, raw_text))
        return {
            "video_id": video_id,
            "cleaned_text": "Welcome to class. Today we are testing mock frameworks.",
            "tech_terms": ["mock frameworks"],
            "book_names": ["Clean Code"],
        }


def test_transcript_enricher_processes_stream():
    """Verifies run() reads JSONL, calls enrich(), and writes output."""
    mock_row = {
        "video_id": "ds5111_v001",
        "raw_text": "[0.0] Welcome to class. [2.5] Today we are testing mock "
                    "frameworks and discussing the book Clean Code."
    }
    input_stream = io.StringIO(json.dumps(mock_row) + "\n")
    output_stream = io.StringIO()
    strategy = MockLLMStrategy(should_validate=True)
    enricher = TranscriptEnricher(
        strategy=strategy,
        input_stream=input_stream,
        output_stream=output_stream,
    )
    enricher.run()
    output_lines = output_stream.getvalue().strip().split("\n")
    assert len(output_lines) == 1
    parsed_output = json.loads(output_lines[0])
    assert parsed_output["video_id"] == "ds5111_v001"
    assert "mock frameworks" in parsed_output["tech_terms"]
    assert "Clean Code" in parsed_output["book_names"]
    assert strategy.enrich_calls == [(mock_row["video_id"], mock_row["raw_text"])]


def test_transcript_enricher_skips_malformed_json():
    """Verifies a malformed JSON line is skipped without crashing."""
    input_stream = io.StringIO("{not valid json\n")
    output_stream = io.StringIO()
    strategy = MockLLMStrategy(should_validate=True)
    enricher = TranscriptEnricher(
        strategy=strategy,
        input_stream=input_stream,
        output_stream=output_stream,
    )
    enricher.run()
    assert output_stream.getvalue().strip() == ""
    assert strategy.enrich_calls == []


def test_transcript_enricher_exits_on_failed_validation():
    """Verifies run() exits with status 1 if validate_environment() raises."""
