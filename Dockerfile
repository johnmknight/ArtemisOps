FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (layer cache)
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server and client
COPY server/ ./server/
COPY client/ ./client/

# Data directory for SQLite
RUN mkdir -p /app/data

EXPOSE 8085

# Run from server/ so bare imports (database, fetcher, etc.) resolve correctly
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8085", "--app-dir", "server"]
