import os

import psycopg2
from dotenv import load_dotenv
from flask_bcrypt import generate_password_hash

load_dotenv()

SQL_DIR = os.path.join(os.path.dirname(__file__), "sql")
SCRIPTS = ["schema_drop.sql", "schema.sql", "views.sql", "schema_ins.sql"]

#(username, full_name, plaintext, role)
DEFAULT_USERS = [
    ("manager", "Bar Manager", "pass", "manager"),
    ("volunteer", "Helpful Volunteer", "pass", "volunteer"),
]


def connect():
    params = {
        "dbname": os.getenv("DB_NAME", "barwin2"),
        "user": os.getenv("DB_USERNAME", "kian"),
    }
    host = os.getenv("DB_HOST")
    if host:
        params["host"] = host
    password = os.getenv("DB_PASSWORD")
    if password:
        params["password"] = password
    return psycopg2.connect(**params)


def main():
    conn = connect()
    with conn.cursor() as cur:
        for script in SCRIPTS:
            path = os.path.join(SQL_DIR, script)
            with open(path) as fh:
                cur.execute(fh.read())
            print(f"  ran {script}")

        for username, full_name, plaintext, role in DEFAULT_USERS:
            pw_hash = generate_password_hash(plaintext).decode("utf-8")
            cur.execute(
                """INSERT INTO app_user (username, full_name, password, role)
                   VALUES (%s, %s, %s, %s)
                   ON CONFLICT (username) DO NOTHING""",
                (username, full_name, pw_hash, role),
            )
            print(f"  seeded user {username!r} ({role})")

        conn.commit()
    conn.close()
    print("Database initialised.")


if __name__ == "__main__":
    main()
