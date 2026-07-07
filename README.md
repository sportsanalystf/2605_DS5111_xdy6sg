# 2605_DS5111_xdy6sg

## Project Overview
A production-grade YouTube transcript data pipeline built for DS5111 Data Engineering at UVA. The pipeline extracts raw transcripts from YouTube videos, enriches them using the Google Gemini LLM, and validates the structured output against a strict JSON schema contract. All steps are designed as Unix-style stream processors (stdin → stdout) that can be chained together.

## Pipeline Architecture
cat video_ids.txt
  | python bin/extract_transcripts.py   # Fetches raw transcripts → JSONL
  | python bin/enrich_transcripts.py    # Enriches via Gemini → structured JSONL
  | python bin/validate_schema.py       # Validates output contract

## Repository Structure
bin/                       # Executable pipeline scripts
  clean_ids.py             # Validates YouTube ID format from stdin
  extract_transcripts.py   # Fetches raw transcripts via YouTube Transcript API
  enrich_transcripts.py    # Enriches transcripts via Google Gemini LLM
  validate_schema.py       # Validates JSONL output against schema contract
tests/                     # Pytest test suite
  test_extract_transcripts.py
  test_enrich_transcripts.py
  test_environment.py
mock_transcripts.jsonl     # Sample input for local pipeline testing
requirements.txt           # Python dependencies
makefile                   # Automation targets
.github/workflows/         # GitHub Actions CI configuration

## Environment Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| GEMINI_API_KEY | Yes | Google Gemini API key for LLM enrichment |
| WEBSHARE_USER | No | Webshare proxy username (required on AWS EC2) |
| WEBSHARE_PASSWORD | No | Webshare proxy password (required on AWS EC2) |

Store all credentials in a .env file at the repo root.
This file is gitignored and must never be committed.

Example .env contents:
GEMINI_API_KEY=your_key_here
WEBSHARE_USER=your_proxy_user
WEBSHARE_PASSWORD=your_proxy_password

## Bootstrapping Instructions

Step 1 - Clone the repository
git clone git@github.com:sportsanalystf/2605_DS5111_xdy6sg.git
cd 2605_DS5111_xdy6sg

Step 2 - Create the virtual environment
make env

Step 3 - Install dependencies
make update

Step 4 - Configure credentials
nano .env
Add GEMINI_API_KEY, WEBSHARE_USER, WEBSHARE_PASSWORD

Step 5 - Create required runtime directories
mkdir -p logs

## Verification Steps

Run linter:
make lint
Expected: Your code has been rated at 10.00/10

Run tests:
make test
Expected: 15 passed, 1 skipped, 1 xfailed

Run end-to-end pipeline smoke test:
make test_enrich
Expected: All 1 records match the required data contract!

Run full pipeline:
cat video_ids.txt | python bin/extract_transcripts.py | python bin/enrich_transcripts.py
