.PHONY: setup lint test ingest eval ask serve plot

setup: ## install package + dev tools
	pip install -e ".[dev]"

lint: ## ruff lint
	ruff check .

test: ## unit tests
	pytest

ingest: ## build vector + BM25 indexes from docs/
	python -m rag.ingest.loaders --source docs/

eval: ## run the Ragas eval gate
	python eval/run_ragas.py

ask: ## ask a question:  make ask Q="How do I ...?"
	python -m rag.generate.answer "$(Q)"

serve: ## run the FastAPI server locally
	uvicorn api:app --reload

plot: ## regenerate the results chart
	python scripts/plot_results.py
