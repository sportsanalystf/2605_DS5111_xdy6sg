ENV = env
PYTHON = $(ENV)/bin/python3
PIP = $(ENV)/bin/pip


default:
	@cat makefile

env:
	python3 -m venv $(ENV); $(PIP) install --upgrade pip

update:
	$(PIP) install -r requirements.txt

lint:
	$(PYTHON) -m  pylint bin/ tests/

test:
	$(PYTHON) -m pytest -vv tests/

run:
	@echo "Usage: cat <video_ids_file> | $(PYTHON) bin/extract_transcripts.py | $(PYTHON) bin/enrich_transcripts.py"

test_enrich:
	@cat mock_transcripts.jsonl | $(PYTHON) -u bin/enrich_transcripts.py | $(PYTHON) bin/validate_schema.py
