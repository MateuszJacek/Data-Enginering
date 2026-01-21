FROM python:3.13.11-slim

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set working directory
WORKDIR /code

# Copy dependency files first (better layer caching)
COPY "pyproject.toml" "uv.lock" ".python-version" ./

RUN uv sync --locked

COPY pipeline_uv.py .

ENTRYPOINT [ "uv", "run", "python", "pipeline_uv.py"]