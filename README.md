# BarwinAPP2

A Flask + PostgreSQL web app for managing Friday bar events at Barwin.

## Run with Docker

```bash
docker compose up --build
```

App on http://localhost:5000 (schema + seed run automatically).

## Run locally

Requires Python 3.11+ and a running PostgreSQL.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # edit DB_USERNAME / DB_PASSWORD / DB_HOST to match your PostgreSQL

createdb barwin2                   # create the database
python app/init_db.py              # build schema + seed data (required)
python run.py                      # http://localhost:5000
```

## Logins

| username  | password | role      |
|-----------|----------|-----------|
| manager   | pass     | manager   |
| volunteer | pass     | volunteer |
</content>
