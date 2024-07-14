#!/bin/bash
# Load environment variables from .env file
source .env

# Authenticate ngrok
ngrok config add-authtoken $NGROK_AUTH_TOKEN

# Start the backend server in the background
python3 /app/src/backend.py &

# Start ngrok with env port variable
ngrok http $PORT