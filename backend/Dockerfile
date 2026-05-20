# Stage 1: Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install system build dependencies required for compiling Python packages (like XGBoost/Prophet if built from source)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create and use a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Run stage
FROM python:3.11-slim as runner

WORKDIR /app

# Copy virtual environment and application code
COPY --from=builder /opt/venv /opt/venv
COPY . .

# Set environment path to use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
