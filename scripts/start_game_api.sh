#!/bin/bash

# Start the enhanced Minecraft Clicker API server
# This server handles both user authentication and game state persistence

echo "Starting Minecraft Clicker API Server..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if Flask is installed
if ! python3 -c "import flask" &> /dev/null; then
    echo "Installing Flask and dependencies..."
    pip3 install flask flask-cors
fi

# Change to the scripts directory
cd "$(dirname "$0")"

# Start the API server
echo "Starting API server on port 5002..."
python3 game_api.py
