"""
Tests for bin/enrich_transcripts.py
"""

import sys
import io
import json
import pytest
from bin.enrich_transcripts import main


class MockGeminiResponse:
    """Mimics the Gemini SDK response object's .text attribute."""

    def __init__(self, text_payload):
        self.text = text_payload


def test_enrich_transcripts_streaming_pipeline(monkeypatch, capsys):
    """
    Verifies that main() reads mock lines from stdin, calls the Gemini client,
    and streams verified JSON objects to stdout without live API calls.
    """
    def mock_generate_content(self, model, contents, config=None):  # pylint: disable=unused-argument
        mock_data = {
            "video_id": "ds5111_v001",
            "cleaned_text": "Welcome to class. Today we are testing mock frameworks.",
            "tech_terms": ["mock frameworks"],
            "book_names": []
        }
        return MockGeminiResponse(json.dumps(mock_data))

    monkeypatch.setenv("GEMINI_API_KEY", "fake_test_key")

    from google.genai.models import Models
    monkeypatch.setattr(Models, "generate_content", mock_generate_content)

    mock_input_row = {
        "video_id": "ds5111_v001",
        "raw_text": "00:01 Welcome to class. Today we are testing mock frameworks."
    }
    mock_stdin = io.StringIO(json.dumps(mock_input_row) + "\n")
    monkeypatch.setattr(sys, "stdin", mock_stdin)

    main()

    captured = capsys.readouterr()
    stdout_lines = captured.out.strip().split("\n")

    assert len(stdout_lines) == 1
    parsed_output = json.loads(stdout_lines[0])
    assert parsed_output["video_id"] == "ds5111_v001"
    assert "mock frameworks" in parsed_output["tech_terms"]


def test_enrich_transcripts_malformed_json_skipped(monkeypatch, capsys):
    """
    Verifies that a malformed JSON line is logged and skipped without
    crashing the pipeline or producing output.
    """
    monkeypatch.setenv("GEMINI_API_KEY", "fake_test_key")
    monkeypatch.setattr(sys, "stdin", io.StringIO("{not valid json\n"))

    main()

    captured = capsys.readouterr()
    assert captured.out.strip() == ""


def test_enrich_transcripts_missing_api_key_exits(monkeypatch):
    """
    Verifies that main() exits with status 1 if GEMINI_API_KEY is missing.
    """
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setattr(sys, "stdin", io.StringIO(""))

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1
