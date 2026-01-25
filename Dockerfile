FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency metadata
COPY pyproject.toml .
COPY uv.lock ./

# Copy source code EARLY (required for packaging)
COPY src ./src

# Install dependencies + project
RUN uv sync --frozen

# Default command
EXPOSE 8000

CMD ["uv", "run", "uvicorn", "chatbot.main:app", "--host", "0.0.0.0", "--port", "8000"]


