#!/bin/bash
# Script to run FastAPI server

echo "Starting Knitty FastAPI server..."
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

