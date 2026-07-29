#!/usr/bin/env python3
"""
gemini_strategy.py - Concrete LLMStrategy implementation wrapping the
Gemini SDK. Handles Gemini-specific auth, schema format, and invocation.
"""
import os
from google import genai
from bin.llm_strategy import LLMStrategy


class GeminiStrategy(LLMStrategy):
    """
    Concrete LLMStrategy that wraps Google's Gemini SDK, using structured
    output (response_schema) to enforce the required transcript schema.
    """

    RESPONSE_SCHEMA = {
        "type": "OBJECT",
        "properties": {
            "video_id": {"type": "STRING"},
            "cleaned_text": {"type": "STRING"},
            "tech_terms": {
                "type": "ARRAY",
                "items": {"type": "STRING"}
            },
            "book_names": {
                "type": "ARRAY",
                "items": {"type": "STRING"}
            },
        },
        "required": ["video_id", "cleaned_text", "tech_terms", "book_names"],
    }

    def __init__(self, api_key: str = None, model: str = "gemini-2.5-flash"):
        """
        Store configuration only. No client is constructed here — call
        validate_environment() before use so setup failures surface at a
        single, predictable point rather than mid-stream.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model
        self.client = None

    def validate_environment(self) -> None:
        """
        Confirm an API key is present and that a genai.Client can be
        constructed from it. Populates self.client on success.
        """
        if not self.api_key:
            raise EnvironmentError("GEMINI_API_KEY not found in environment.")
        self.client = genai.Client(api_key=self.api_key)

    def enrich(self, video_id: str, raw_text: str) -> dict:
        """To be implemented next: prompt construction, model invocation,
        and response parsing."""
        raise NotImplementedError
