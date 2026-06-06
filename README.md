# BarwinAPP2

A Flask + PostgreSQL web app for managing Friday bar events at Barwin
(events, volunteer shifts with capacity-based waitlisting, drinks, and sales
with per-event revenue summaries).

Raw SQL via `psycopg2` (no ORM), Flask-Login + Flask-Bcrypt auth with two roles
(`manager`, `volunteer`), and Flask-WTF forms. The schema lives in `app/sql/`.

---

## Prerequisites

- **Python 3.11+**
- **PostgreSQL** running locally (the `psql` and `createdb` client tools on your PATH)
- Or, for the zero-setup path: **Docker** + **Docker Compose**

---

## Option A — Run with Docker (easiest; auto-initialises the database)

This is the only path that builds the schema and seeds data for you
automatically (`entrypoint.sh` runs `app/init_db.py` before starting Flask).

```bash
git clone <repo-url> BarwinAPP2
cd BarwinAPP2

docker compose up --build
```

App is served on http://localhost:5000. To stop it, press `Ctrl+C`
(or `docker compose down` from another terminal).

> Note: the container runs `init_db.py` on **every** start, which drops and
> re-seeds the domain tables. Data you enter does not survive a restart of the
> `web` container. (See the destructive-init note under [Notes](#notes).)

---

## Option B — Run locally (without Docker)

A fresh clone does **not** include `.venv/` or `.env` (both are git-ignored),
and **`python run.py` does not initialise the database** — you must create and
seed it yourself first. Follow every step below in order.

```bash
# 1. Clone and enter the project
git clone <repo-url> BarwinAPP2
cd BarwinAPP2

# 2. Create a virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Create the .env config from the template, then edit it (see below)
cp .env.example .env

# 4. Create the empty database (owned by the user you put in DB_USERNAME)
createdb barwin2                   # or: psql -c "CREATE DATABASE barwin2;"

# 5. Build the schema + seed data (REQUIRED — run.py will not do this)
python app/init_db.py

# 6. Start the app
python run.py                      # http://localhost:5000
```

### Configuring `.env`

The shipped `.env.example` holds the **Docker** defaults (`postgres` / `UIS` /
`localhost`); a stock local PostgreSQL install usually does **not** have a
`postgres` role with that password. After `cp .env.example .env`, edit the
values to match your own local PostgreSQL — and make sure `DB_USERNAME` matches
the user that owns the `barwin2` database from step 4:

| Variable      | Meaning                                | Example                    |
|---------------|----------------------------------------|----------------------------|
| `SECRET_KEY`  | Flask session secret                   | `devsecret`                |
| `DB_NAME`     | Database name                          | `barwin2`                  |
| `DB_USERNAME` | PostgreSQL user                        | `postgres` (or your login) |
| `DB_PASSWORD` | Password (leave blank for local trust/socket auth) | `UIS`          |
| `DB_HOST`     | Host (leave blank to use a Unix socket) | `localhost`               |

> Tip: on a typical local install where your OS user owns PostgreSQL, you can
> set `DB_USERNAME` to your own username and leave `DB_PASSWORD`/`DB_HOST` blank
> to connect over the Unix socket.

---

## Default logins (seeded)

| username  | password | role      |
|-----------|----------|-----------|
| manager   | pass     | manager   |
| volunteer | pass     | volunteer |

Managers get full CRUD; volunteers get read access plus shift signup.

---

## Notes

- **`run.py` never touches the schema.** It only starts the web server and
  opens the DB connection at import time — so if the database does not exist or
  has not been initialised, it will fail to start. Run `python app/init_db.py`
  first (or use the Docker path, which does this for you).
- **`app/init_db.py` is destructive for domain data.** It drops and recreates
  all domain tables (events, volunteers, shifts, drinks, sales) and re-seeds
  them, so re-running it wipes any data you have entered. The default users are
  inserted with `ON CONFLICT DO NOTHING`, so existing logins are preserved.
- **Editing `app/sql/*.sql` or `init_db.py` only changes the seed recipe.**
  Those files take effect only when `init_db.py` runs; they do not alter a
  database that has already been built. To change live data, use the app UI
  (as a manager) or `psql`.
- Event dates use `YYYY-MM-DD`. Shift datetimes use `DD-MM-YYYY HH:MM`
  (e.g. `25-12-2025 20:00`); the "Add shift" link from an event pre-fills the
  event's date.

---

## Stopping the app

- **Local:** press `Ctrl+C` in the terminal running `python run.py`.
  If it is running in the background: `pkill -f run.py`.
- **Docker:** `Ctrl+C`, or `docker compose down` from another terminal.
</content>
</invoke>
