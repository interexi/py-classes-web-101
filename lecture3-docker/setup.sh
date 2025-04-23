#!/bin/bash

# Create necessary directories
mkdir -p templates static

# Copy Flask application files
cp ../lecture1-flask/app.py .
cp ../lecture1-flask/requirements.txt .
cp -r ../lecture1-flask/templates/* templates/
cp -r ../lecture1-flask/static/* static/

echo "Files copied successfully. You can now build the Docker image." 