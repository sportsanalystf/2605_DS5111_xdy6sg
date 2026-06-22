"""
Tests for bin/extract_transcripts.py
"""

import sys
import io
import json
import pytest
from youtube_transcript_api import YouTubeTranscriptApi

from bin.extract_transcripts import main


class MockTranscriptContainer:
    """Mimics the YouTubeTranscriptApi .to_raw_data() return schema."""

    def to_raw_data(self):
        """Return a minimal fake transcript segment list."""
        return [
            {"start": 10.5, "text": "Automated container tracking loop text entry."}
        ]


def test_extract_transcripts_success(monkeypatch, capsys):
    """Valid video ID produces one JSONL row with correct fields."""

    def stubbed_fetch(self, video_id):  # pylint: disable=unused-argument
        return MockTranscriptContainer()

    monkeypatch.setattr(YouTubeTranscriptApi, "fetch", stubbed_fetch)
    monkeypatch.setattr(sys, "stdin", io.StringIO("fake_video_999\n"))

    main()

    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")

    assert len(lines) == 1
    parsed = json.loads(lines[0])
    assert parsed["video_id"] == "fake_video_999"
    assert "Automated container tracking" in parsed["raw_text"]


def test_extract_transcripts_bad_id_no_crash(monkeypatch, capsys):
    """Invalid video ID is skipped gracefully with no output and no crash."""

    def stubbed_fetch_error(self, video_id):  # pylint: disable=unused-argument
        raise ValueError(f"No transcript found for: {video_id}")

    monkeypatch.setattr(YouTubeTranscriptApi, "fetch", stubbed_fetch_error)
    monkeypatch.setattr(sys, "stdin", io.StringIO("bad_video_000\n"))

    main()

    captured = capsys.readouterr()
    assert captured.out.strip() == ""


def test_extract_transcripts_blank_lines_skipped(monkeypatch, capsys):
    """Blank lines in stdin produce no output and no crash."""
    monkeypatch.setattr(sys, "stdin", io.StringIO("\n\n\n"))

    main()

    captured = capsys.readouterr()
    assert captured.out.strip() == ""
