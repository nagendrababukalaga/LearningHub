#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip and install production dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files into STATIC_ROOT using WhiteNoise
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate --noinput

# Optional: Seed initial curriculum data if SEED_DATABASE is true
if [ "${SEED_DATABASE:-false}" = "true" ] || [ "${SEED_DATABASE:-false}" = "1" ]; then
    echo "[+] Seeding LearningHub curriculum and demo student..."
    python manage.py seed_learninghub
fi
