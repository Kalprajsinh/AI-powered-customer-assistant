#!/bin/sh

# Start Redis in the background and then launch FastAPI
redis-server --save "" --appendonly no --protected-mode no &

# Give Redis a moment to start up
sleep 1

# Start FastAPI app
exec uv run uvicorn app.server:app --host 0.0.0.0 --port 8000
