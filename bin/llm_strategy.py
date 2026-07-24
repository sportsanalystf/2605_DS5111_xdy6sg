#!/usr/bin/env python3
"""
llm_strategy.py - Abstract base class defining the enrichment contract
for Pipeline Step 2B. Concrete strategies (Gemini, OpenAI, etc.) must
implement this interface so main() can remain provider-agnostic.
"""

from abc import ABC, abstractmethod


class LLMStrategy(ABC):
    """
    Strict contract for a transcript-enrichment engine.

    Any concrete strategy must be able to (1) verify it is safe to run
    before the pipeline starts consuming stdin, and (2) turn a single
    raw transcript row into a dict matching the required schema:
    video_id, cleaned_text, tech_terms, book_names.
    """

    @abstractmethod
    def validate_environment(self) -> None:
        """
        Confirm this strategy is ready to use (e.g. required API keys
        are present, client can be constructed).

        Should raise an exception (or otherwise signal failure) if the
        strategy is not usable, so the caller can fail fast rather than
        discovering the problem mid-stream.
        """
        raise NotImplementedError

    @abstractmethod
    def enrich(self, video_id: str, raw_text: str) -> dict:
        """
        Given a video_id and its raw transcript text, return a dict with
        exactly these keys: video_id, cleaned_text, tech_terms, book_names.
        """
        raise NotImplementedError
