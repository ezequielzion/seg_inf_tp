#!/bin/bash

# Load the environment variables from the .env file
source .env

# Build the Docker image
docker build -t flask_docker .

# Run the Docker container mapping the host port to the container port
docker run -p ${PORT}:${PORT} flask_docker