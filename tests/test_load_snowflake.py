"""
tests/test_load_snowflake.py
Offline mock tests for bin/load_snowflake.py
"""
import sys
import io
import json
import pytest
from unittest.mock import MagicMock
import snowflake.connector
from bin.load_snowflake import main


def test_load_snowflake_pipeline_ingestion_loop(monkeypatch):
    """
    Verifies that main() processes JSONL from stdin, creates the table,
    and executes safe parameterized inserts without real network calls.
    """
    mock_cursor = MagicMock()
    mock_context = MagicMock()
    mock_context.cursor.return_value = mock_cursor

    monkeypatch.setattr(snowflake.connector, "connect", lambda **kwargs: mock_context)
    monkeypatch.setenv("SF_USER", "test_user")
    monkeypatch.setenv("SF_PASSWORD", "test_password")
    monkeypatch.setenv("SF_ACCOUNT", "test_account")
    monkeypatch.setenv("SF_WAREHOUSE", "test_wh")
    monkeypatch.setenv("SF_DATABASE", "test_db")
    monkeypatch.setenv("SF_SCHEMA", "test_schema")
    monkeypatch.setenv("SF_ROLE", "test_role")

    mock_input_stream = io.StringIO(
        '{"video_id": "test_id_001", "source": "youtube", "raw_text": "Sample content text A."}\n'
        '{"video_id": "test_id_002", "source": "podcast", "raw_text": "Sample content text B."}\n'
    )
    monkeypatch.setattr(sys, "stdin", mock_input_stream)

    try:
        main()
    except UnboundLocalError:
        pytest.fail("Resource variables referenced before definition.")

    assert mock_cursor.execute.call_count >= 3

    executed_queries = [call[0][0] for call in mock_cursor.execute.call_args_list]
    executed_bindings = [
        call[0][1] for call in mock_cursor.execute.call_args_list if len(call[0]) > 1
    ]

    assert any("CREATE TABLE IF NOT EXISTS RAW_TRANSCRIPTS" in q for q in executed_queries)

    insert_queries = [q for q in executed_queries if "INSERT INTO RAW_TRANSCRIPTS" in q]
    assert len(insert_queries) == 2

    for query in insert_queries:
        assert "PARSE_JSON(%s)" in query

    assert len(executed_bindings) == 2
    parsed_payload = json.loads(executed_bindings[0][0])
    assert parsed_payload["video_id"] == "test_id_001"


def test_load_snowflake_missing_credentials_exits(monkeypatch):
    """Verifies main() exits with status 1 if SF credentials are missing."""
    monkeypatch.delenv("SF_USER", raising=False)
    monkeypatch.delenv("SF_PASSWORD", raising=False)
    monkeypatch.setattr(sys, "stdin", io.StringIO(""))

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1
