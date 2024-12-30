#!/bin/bash

# Fetch environment variables from launchctl and export them
export OPENAI_API_KEY=$(launchctl getenv OPENAI_API_KEY)

# Run the Python script
python3 ~/Scripts/correcter/correcter.py "$@"
