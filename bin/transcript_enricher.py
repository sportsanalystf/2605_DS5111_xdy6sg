#!/usr/bin/env python3
"""
transcript_enricher.py - Pipeline Step 2B orchestrator.
Vendor-agnostic engine that drives a JSONL stream through any injected
LLMStrategy. Owns stdin/stdout handling, logging, and per-row error
isolation; knows nothing about Gemini, OpenAI, or any specific provider.
"""
import sys
import json
import logging
from llm_strategy import LLMStrategy


class TranscriptEnricher:
    """
    Strategy-pattern context object. Wraps a single injected LLMStrategy
    and drives it against a stream of raw transcript JSONL rows.
    """

    def __init__(self, strategy: LLMStrategy, input_stream=None, output_stream=None):
        """
        Args:
            strategy: any LLMStrategy implementation (Gemini, OpenAI, ...).
            input_stream: readable line iterator, defaults to sys.stdin.
            output_stream: writable stream, defaults to sys.stdout.
        """
        self.strategy = strategy
        self.input_stream = input_stream if input_stream is not None else sys.stdin
        self.output_stream = output_stream if output_stream is not None else sys.stdout

    def run(self) -> None:
        """
        Validate the injected strategy is usable, then stream rows from
        input_stream to output_stream, enriching each via the strategy.
        Exits with status 1 if the strategy fails environment validation.
        """
        logging.info("Pipeline Step 2B (Enrichment) started.")
        try:
            self.strategy.validate_environment()
        except Exception as exc:  # pylint: disable=broad-except
            logging.critical("Strategy failed environment validation: %s", str(exc))
            sys.exit(1)

        for line in self.input_stream:
            line = line.strip()
            if not line:
                continue

            try:
                record = json.loads(line)
                video_id = record["video_id"]
                raw_text = record["raw_text"]
            except (json.JSONDecodeError, KeyError) as exc:
                logging.error("Failed to parse incoming JSON payload row: %s", str(exc))
                continue

            logging.info("Orchestrating enrichment for video: %s", video_id)

            try:
                result = self.strategy.enrich(video_id, raw_text)
            except Exception as exc:  # pylint: disable=broad-except
                logging.error(
                    "Failed processing video %s during enrichment: %s", video_id, str(exc)
                )
                continue

            self.output_stream.write(json.dumps(result) + "\n")
            self.output_stream.flush()

        logging.info("Pipeline Step 2B finished.")
