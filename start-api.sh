#!/bin/bash
# Start the Document Converter API server

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Starting Document Converter API..."
echo "API will be available at: http://localhost:8000"
echo "API docs will be available at: http://localhost:8000/docs"
echo ""

"${SCRIPT_DIR}/.venv/bin/uvicorn" backend.api:app --reload --host 0.0.0.0 --port 8000
