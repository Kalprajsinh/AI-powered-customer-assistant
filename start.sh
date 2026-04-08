#!/bin/sh

# Start Redis
redis-server --bind 127.0.0.1 --protected-mode yes &

sleep 1

# Start FastAPI
exec uvicorn app.server:app --host 0.0.0.0 --port ${PORT:-10000}