FROM python:3.11 AS dev-deps

RUN pip install --upgrade pip

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.5.1

# System deps:
RUN pip install --upgrade --progress-bar off pip && pip install --progress-bar off "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /
COPY poetry.lock pyproject.toml /

# Project initialization:
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Dev stage
FROM dev-deps AS dev

COPY config.yaml alembic.ini /
COPY alembic /alembic
COPY app /app
COPY tests /tests

ENV PYTHONPATH=/

EXPOSE 8000
ENTRYPOINT ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000"]
