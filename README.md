# BarwinAPP2

A Flask + PostgreSQL web app for managing Friday bar events at Barwin
(events, volunteer shifts with capacity-based waitlisting, drinks, and sales
with per-event revenue summaries).


## Run with Docker

```bash
docker compose up --build
# app on http://localhost:5000 ; schema + seed run automatically via entrypoint.sh
```

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # edit DB_NAME / DB_USERNAME / DB_PASSWORD / DB_HOST

# create the database, then build the schema + seed:
createdb barwin2                # or: psql -c "CREATE DATABASE barwin2 OWNER ..."
python app/init_db.py

python run.py                   # http://localhost:5000
```
