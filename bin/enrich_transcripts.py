#!/usr/bin/env python3
"""
enrich_transcripts.py - Pipeline Step 2B (Gemini Enrichment)
Reads raw transcript JSONL from stdin, enriches via Gemini with a strict
schema contract, and streams structured JSONL to stdout.
"""

import sys
import os
import json
import logging

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

logging.basicConfig(
    filename='logs/pipeline_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main():
    """Read raw transcript rows from stdin, enrich via Gemini, emit JSONL."""
    logging.info("Pipeline Step 2B (Gemini Enrichment) started.")

    #1: API Environment Validation and Client Initialization
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logging.critical("GEMINI_API_KEY not found in environment. Exiting.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    #2: Structured Output Response Schema Definition
    response_schema = {
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

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        #3: Inbound String Stream Deserialization
        try:
            record = json.loads(line)
            video_id = record["video_id"]
            raw_text = record["raw_text"]
        except (json.JSONDecodeError, KeyError) as exc:
            logging.error("Failed to parse incoming JSON payload row: %s", str(exc))
            continue

        logging.info("Orchestrating Gemini enrichment for video: %s", video_id)

        prompt = f"""
        You are an elite data engineer. Clean this transcript text for video_id '{video_id}'.
        1. Strip all timestamps and duration codes.
        2. Extract technical architecture terms and books.

        Transcript:
        {raw_text}
        """

        #4: Structured Model Invocation and Instant Stream Flushing
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=response_schema,
                ),
            )
            sys.stdout.write(response.text.strip() + "\n")
            sys.stdout.flush()

        except Exception as exc:  # pylint: disable=broad-except
            logging.error(
		"Failed processing video %s during LLM generation: %s", video_id, str(exc)
	    )

    logging.info("Pipeline Step 2B finished.")


if __name__ == '__main__':
    main()
