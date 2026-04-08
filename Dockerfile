FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY . ./

RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]
