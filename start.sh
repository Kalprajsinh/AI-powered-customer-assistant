#!/bin/sh

redis-server --bind 127.0.0.1 --protected-mode yes &

sleep 1

exec python -m uvicorn app.server:app --host 0.0.0.0 --port ${PORT:-10000}