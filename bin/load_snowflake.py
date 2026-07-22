#!/usr/bin/env python3
"""
load_snowflake.py - Pipeline Step 3: Snowflake Loader Node.
Reads enriched JSONL from stdin and loads into Snowflake VARIANT table.
"""
import sys
import os
import json
import logging
import snowflake.connector
from dotenv import load_dotenv

logging.basicConfig(
    filename='pipeline/logs/pipeline_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main():
    """Read enriched JSONL from stdin and load into Snowflake."""
    load_dotenv()
    logging.info("Pipeline Step 3 (Snowflake Loader Node) initialized.")

    sf_user = os.getenv('SF_USER')
    sf_password = os.getenv('SF_PASSWORD')

    if not sf_user or not sf_password:
        logging.critical("Missing critical Snowflake runtime credential bindings.")
        sys.exit(1)

    try:
        ctx = snowflake.connector.connect(
            user=sf_user,
            password=sf_password,
            account=os.getenv('SF_ACCOUNT'),
            warehouse=os.getenv('SF_WAREHOUSE'),
            database=os.getenv('SF_DATABASE'),
            schema=os.getenv('SF_SCHEMA'),
            role=os.getenv('SF_ROLE'),
        )
        cs = ctx.cursor()
    except Exception as exc:  # pylint: disable=broad-except
        logging.critical("Snowflake Authorization Context Handshake Failed: %s", str(exc))
        sys.exit(1)

    try:
        cs.execute("""
            CREATE TABLE IF NOT EXISTS RAW_TRANSCRIPTS (
                json_payload VARIANT,
                inserted_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
            )
        """)
    except Exception as exc:  # pylint: disable=broad-except
        logging.error("Failed to execute target structural validation DDL: %s", str(exc))
        cs.close()
        ctx.close()
        sys.exit(1)

    for line in sys.stdin:
        cleaned_line = line.strip()
        if not cleaned_line:
            continue

        try:
            json_data = json.loads(cleaned_line)
            cs.execute(
                "INSERT INTO RAW_TRANSCRIPTS (json_payload) SELECT PARSE_JSON(%s)",
                (json.dumps(json_data),)
            )
            logging.info(
                "Loaded entry token item target: [%s] safely to warehouse.",
                json_data.get('video_id', 'UNKNOWN')
            )
        except Exception as exc:  # pylint: disable=broad-except
            logging.error("Skipping corrupt pipeline payload stream element: %s", str(exc))

    cs.close()
    ctx.close()
    logging.info("Pipeline Step 3 finished execution cycles cleanly.")


if __name__ == '__main__':
    main()
