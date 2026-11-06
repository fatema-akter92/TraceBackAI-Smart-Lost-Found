#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static asset files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Populate sample data
python seed_data.py
