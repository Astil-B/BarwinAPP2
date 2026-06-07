#!/bin/sh
set -e

echo "Initialising database schema..."
python app/init_db.py

echo "Starting Barwin web app..."
exec flask --app run run --host 0.0.0.0 --port 5000
