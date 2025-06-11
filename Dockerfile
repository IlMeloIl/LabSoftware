FROM python:3.13.4-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml .
COPY uv.lock .

ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
RUN uv sync --locked --no-dev

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]