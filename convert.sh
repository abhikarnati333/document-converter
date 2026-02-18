#!/bin/bash
# Convenience script to run the converter with the virtual environment

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
"${SCRIPT_DIR}/.venv/bin/python" "${SCRIPT_DIR}/backend/converter.py" "$@"
