# PEaC Reproducibility Container
# Minimal Python environment for running functional and performance tests

FROM python:3.11-slim

LABEL maintainer="PEaC Development Team"
LABEL description="Reproducibility container for PEaC performance benchmarks"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set working directory
WORKDIR /peac

# Copy project files
COPY pyproject.toml poetry.lock ./
COPY peac/ ./peac/
COPY tests/ ./tests/
COPY examples/ ./examples/
COPY scripts/ ./scripts/
COPY Makefile ./

# Install dependencies (without dev dependencies for smaller image)
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Install test dependencies
RUN poetry install --only test --no-interaction --no-ansi

# Install psutil for performance benchmarking
RUN pip install psutil

# Create directory for benchmark results
RUN mkdir -p /peac/benchmark_results

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PEAC_HOME=/peac

# Default command: run functional tests
CMD ["poetry", "run", "pytest", "tests/", "-v", "--tb=short"]

# To run performance benchmarks:
# docker run peac-reproducibility poetry run pytest tests/test_performance.py -v -s

# To run all tests:
# docker run peac-reproducibility make test
