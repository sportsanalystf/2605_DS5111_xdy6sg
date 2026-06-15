#!/usr/bin/env python3
"""
extract_transcripts.py - Fetches raw YouTube transcripts from stdin video IDs.
Outputs JSONL to stdout. Logs errors to pipeline/logs/pipeline_audit.log.
"""

import sys
import os
import json
import logging

from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

load_dotenv()

logging.basicConfig(
    filename='pipeline/logs/pipeline_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main():
    """Read video IDs from stdin, fetch transcripts, emit JSONL to stdout."""
    logging.info("Pipeline Step 2A (Raw Extraction) started.")

    proxy_user = os.getenv("WEBSHARE_USER")
    proxy_pass = os.getenv("WEBSHARE_PASSWORD")

    if proxy_user and proxy_pass:
        logging.info("Proxy credentials detected. Routing via Webshare.")
        ytt_api = YouTubeTranscriptApi(
            proxy_config=WebshareProxyConfig(
                proxy_username=proxy_user,
                proxy_password=proxy_pass,
            )
        )
    else:
        logging.warning("No proxy credentials found. Using direct IP.")
        ytt_api = YouTubeTranscriptApi()

    for line in sys.stdin:
        video_id = line.strip()
        if not video_id:
            continue

        logging.info("Processing video: %s", video_id)

        try:
            fetched_transcript = ytt_api.fetch(video_id)
            transcript_list = fetched_transcript.to_raw_data()
            raw_text = " ".join(
                [f"[{item['start']}] {item['text']}" for item in transcript_list]
            )
            payload = {"video_id": video_id, "raw_text": raw_text}
            sys.stdout.write(json.dumps(payload) + "\n")
            sys.stdout.flush()

        except Exception as exc:  # pylint: disable=broad-except
            logging.error("Failed for %s: %s", video_id, str(exc))
            continue

    logging.info("Pipeline Step 2A finished.")


if __name__ == '__main__':
    main()
