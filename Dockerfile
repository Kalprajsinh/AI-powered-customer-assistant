FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml .

# Install dependencies
RUN uv pip install --system -r pyproject.toml 2>/dev/null || \
    uv pip install --system \
    faiss-cpu \
    fastapi \
    groq \
    langchain \
    langchain-community \
    langchain-google-genai \
    langchain-groq \
    langchain-redis \
    pypdf \
    python-dotenv \
    redis \
    sentence-transformers \
    "uvicorn[standard]"

# Copy the entire project
COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.server:app --host 0.0.0.0 --port ${PORT:-8000}"]