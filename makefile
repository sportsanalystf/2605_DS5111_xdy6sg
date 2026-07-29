default:
	@cat makefile

env:
	python3 -m venv env; . env/bin/activate; pip install --upgrade pip

update: env
	. env/bin/activate; pip install -r requirements.txt

lint:
	. env/bin/activate && pylint bin/

test: lint
	. env/bin/activate && pytest -vv tests/

test_enrich:
	@. env/bin/activate && cat mock_transcripts.jsonl | python -u bin/enrich_transcripts.py | python bin/validate_schema.py

build:
	docker build -t khansaamaa/ds5111-pipeline:latest .

push:
	docker push khansaamaa/ds5111-pipeline:latest

run:
	cat data/youtube_ids.txt | docker run -i --env-file .env khansaamaa/ds5111-pipeline:latest

load:
	@echo "Initiating Cloud Data Warehouse Synchronizer Node..."
	@cat data/enriched_transcripts.jsonl | $(PYTHON) bin/load_snowflake.py
