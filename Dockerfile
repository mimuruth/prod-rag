# prod-rag API image for Azure Container Apps (or any container host).
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app/src \
    PYTHONUNBUFFERED=1

COPY pyproject.toml ./
COPY src ./src
COPY api.py ./
COPY prompts ./prompts
COPY config ./config
COPY docs ./docs

RUN pip install --no-cache-dir -e ".[serve]"

EXPOSE 8000

# Build indexes on first boot if absent, then serve. OPENAI_API_KEY is supplied at runtime.
CMD ["sh", "-c", "[ -d .chroma ] || python -m rag.ingest.loaders --source docs/; uvicorn api:app --host 0.0.0.0 --port 8000"]
