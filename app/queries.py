from psycopg2.extras import RealDictCursor

from app import conn
from app.models import User, Event, Volunteer, Shift, ShiftSignup, Drink, Sale


def _cur():
    return conn.cursor(cursor_factory=RealDictCursor)



#Users / auth

def get_user_by_username(username):
    cur = _cur()
    cur.execute("SELECT * FROM app_user WHERE username = %s", (username,))
    row = cur.fetchone()
    cur.close()
    return User(row) if row else None


def insert_user(username, full_name, password_hash, role):
    cur = _cur()
    cur.execute(
        """INSERT INTO app_user (username, full_name, password, role)
           VALUES (%s, %s, %s, %s) RETURNING id""",
        (username, full_name, password_hash, role),
    )
    new_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    return new_id



#Events

def get_all_events():
    cur = _cur()
    cur.execute("SELECT * FROM event ORDER BY date DESC")
    rows = cur.fetchall()
    cur.close()
    return [Event(r) for r in rows]


def get_recent_events(limit=10):
    cur = _cur()
    cur.execute("SELECT * FROM event ORDER BY date DESC LIMIT %s", (limit,))
    rows = cur.fetchall()
    cur.close()
    return [Event(r) for r in rows]


def get_event(event_id):
    cur = _cur()
    cur.execute("SELECT * FROM event WHERE id = %s", (event_id,))
    row = cur.fetchone()
    cur.close()
    return Event(row) if row else None


def insert_event(name, date, description, location):
    cur = _cur()
    cur.execute(
        """INSERT INTO event (name, date, description, location)
           VALUES (%s, %s, %s, %s) RETURNING id""",
        (name, date, description, location),
    )
    new_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    return new_id


def update_event(event_id, name, date, description, location):
    cur = _cur()
    cur.execute(
        """UPDATE event SET name = %s, date = %s, description = %s, location = %s
           WHERE id = %s""",
        (name, date, description, location, event_id),
    )
    conn.commit()
    cur.close()


def delete_event(event_id):
    cur = _cur()
    cur.execute("DELETE FROM event WHERE id = %s", (event_id,))
    conn.commit()
    cur.close()



#Volunteers
def get_all_volunteers():
    cur = _cur()
    cur.execute("SELECT * FROM volunteer ORDER BY name")
    rows = cur.fetchall()
    cur.close()
    return [Volunteer(r) for r in rows]


def get_volunteer(volunteer_id):
    cur = _cur()
    cur.execute("SELECT * FROM volunteer WHERE id = %s", (volunteer_id,))
    row = cur.fetchone()
    cur.close()
    return Volunteer(row) if row else None


def insert_volunteer(name, email, phone):
    cur = _cur()
    cur.execute(
        "INSERT INTO volunteer (name, email, phone) VALUES (%s, %s, %s) RETURNING id",
        (name, email, phone),
    )
    new_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    return new_id


def update_volunteer(volunteer_id, name, email, phone):
    cur = _cur()
    cur.execute(
        "UPDATE volunteer SET name = %s, email = %s, phone = %s WHERE id = %s",
        (name, email, phone, volunteer_id),
    )
    conn.commit()
    cur.close()


def delete_volunteer(volunteer_id):
    cur = _cur()
    cur.execute("DELETE FROM volunteer WHERE id = %s", (volunteer_id,))
    conn.commit()
    cur.close()


def get_volunteer_signups(volunteer_id):
    """Signups for one volunteer, joined to shift role + event name."""
    cur = _cur()
    cur.execute(
        """SELECT su.id, su.status, sh.id AS shift_id, sh.role,
                  e.name AS event_name
           FROM shift_signup su
           JOIN shift sh ON sh.id = su.shift_id
           JOIN event e  ON e.id = sh.event_id
           WHERE su.volunteer_id = %s
           ORDER BY sh.start_time""",
        (volunteer_id,),
    )
    rows = cur.fetchall()
    cur.close()
    return rows


def get_volunteer_sales(volunteer_id):
    cur = _cur()
    cur.execute(
        """SELECT s.id, s.quantity, s.sold_at,
                  d.name AS drink_name, e.name AS event_name
           FROM sale s
           JOIN drink d ON d.id = s.drink_id
           JOIN event e ON e.id = s.event_id
           WHERE s.volunteer_id = %s
           ORDER BY s.sold_at DESC""",
        (volunteer_id,),
    )
    rows = cur.fetchall()
    cur.close()
    return rows



#Shifts
def get_all_shifts(event_id=None):
    """Shifts joined to their event name and the fill view."""
    cur = _cur()
    base = """
        SELECT sh.*, e.name AS event_name,
               f.confirmed_count, f.slots_left
        FROM shift sh
        JOIN event e        ON e.id = sh.event_id
        JOIN vw_shift_fill f ON f.shift_id = sh.id
    """
    if event_id:
        cur.execute(base + " WHERE sh.event_id = %s ORDER BY sh.start_time", (event_id,))
    else:
        cur.execute(base + " ORDER BY sh.start_time")
    rows = cur.fetchall()
    cur.close()
    return [Shift(r) for r in rows]


def get_shift(shift_id):
    cur = _cur()
    cur.execute(
        """SELECT sh.*, e.name AS event_name,
                  f.confirmed_count, f.slots_left
           FROM shift sh
           JOIN event e         ON e.id = sh.event_id
           JOIN vw_shift_fill f ON f.shift_id = sh.id
           WHERE sh.id = %s""",
        (shift_id,),
    )
    row = cur.fetchone()
    cur.close()
    return Shift(row) if row else None


def get_shifts_for_event(event_id):
    return get_all_shifts(event_id=event_id)


def insert_shift(event_id, role, start_time, end_time, capacity):
    cur = _cur()
    cur.execute(
        """INSERT INTO shift (event_id, role, start_time, end_time, capacity)
           VALUES (%s, %s, %s, %s, %s) RETURNING id""",
        (event_id, role, start_time, end_time, capacity),
    )
    new_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    return new_id


def update_shift(shift_id, event_id, role, start_time, end_time, capacity):
    cur = _cur()
    cur.execute(
        """UPDATE shift SET event_id = %s, role = %s, start_time = %s,
                            end_time = %s, capacity = %s
           WHERE id = %s""",
        (event_id, role, start_time, end_time, capacity, shift_id),
    )
    conn.commit()
    cur.close()


def delete_shift(shift_id):
    cur = _cur()
    cur.execute("DELETE FROM shift WHERE id = %s RETURNING event_id", (shift_id,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    return row["event_id"] if row else None


def get_shift_signups(shift_id):
    cur = _cur()
    cur.execute(
        """SELECT su.id, su.status, v.id AS volunteer_id, v.name AS volunteer_name
           FROM shift_signup su
           JOIN volunteer v ON v.id = su.volunteer_id
           WHERE su.shift_id = %s
           ORDER BY su.id""",
        (shift_id,),
    )
    rows = cur.fetchall()
    cur.close()
    return rows


def count_confirmed_signups(shift_id):
    cur = _cur()
    cur.execute(
        "SELECT COUNT(*) AS n FROM shift_signup WHERE shift_id = %s AND status = 'confirmed'",
        (shift_id,),
    )
    n = cur.fetchone()["n"]
    cur.close()
    return n


def insert_signup(shift_id, volunteer_id, status):
    """Insert a signup. Raises psycopg2 IntegrityError on duplicate."""
    cur = _cur()
    cur.execute(
        "INSERT INTO shift_signup (shift_id, volunteer_id, status) VALUES (%s, %s, %s)",
        (shift_id, volunteer_id, status),
    )
    conn.commit()
    cur.close()



#Drinks

def get_all_drinks():
    cur = _cur()
    cur.execute("SELECT * FROM drink ORDER BY category, name")
    rows = cur.fetchall()
    cur.close()
    return [Drink(r) for r in rows]


def get_drink(drink_id):
    cur = _cur()
    cur.execute("SELECT * FROM drink WHERE id = %s", (drink_id,))
    row = cur.fetchone()
    cur.close()
    return Drink(row) if row else None


def insert_drink(name, category, price_dkk, unit):
    cur = _cur()
    cur.execute(
        "INSERT INTO drink (name, category, price_dkk, unit) VALUES (%s, %s, %s, %s) RETURNING id",
        (name, category, price_dkk, unit),
    )
    new_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    return new_id


def update_drink(drink_id, name, category, price_dkk, unit):
    cur = _cur()
    cur.execute(
        "UPDATE drink SET name = %s, category = %s, price_dkk = %s, unit = %s WHERE id = %s",
        (name, category, price_dkk, unit, drink_id),
    )
    conn.commit()
    cur.close()


def delete_drink(drink_id):
    cur = _cur()
    cur.execute("DELETE FROM drink WHERE id = %s", (drink_id,))
    conn.commit()
    cur.close()



#Sales

def get_all_sales(event_id=None):
    cur = _cur()
    base = """
        SELECT s.id, s.quantity, s.sold_at,
               d.name AS drink_name, e.name AS event_name, v.name AS volunteer_name,
               s.event_id
        FROM sale s
        JOIN drink d     ON d.id = s.drink_id
        JOIN event e     ON e.id = s.event_id
        JOIN volunteer v ON v.id = s.volunteer_id
    """
    if event_id:
        cur.execute(base + " WHERE s.event_id = %s ORDER BY s.sold_at DESC", (event_id,))
    else:
        cur.execute(base + " ORDER BY s.sold_at DESC")
    rows = cur.fetchall()
    cur.close()
    return rows


def insert_sale(event_id, drink_id, volunteer_id, quantity):
    cur = _cur()
    cur.execute(
        """INSERT INTO sale (event_id, drink_id, volunteer_id, quantity)
           VALUES (%s, %s, %s, %s)""",
        (event_id, drink_id, volunteer_id, quantity),
    )
    conn.commit()
    cur.close()


def delete_sale(sale_id):
    cur = _cur()
    cur.execute("DELETE FROM sale WHERE id = %s RETURNING event_id", (sale_id,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    return row["event_id"] if row else None


def get_sales_summary(event_id):
    """Per-drink totals for one event, straight from the reporting view."""
    cur = _cur()
    cur.execute(
        """SELECT drink_name, total_qty, total_revenue
           FROM vw_sales_summary
           WHERE event_id = %s
           ORDER BY drink_name""",
        (event_id,),
    )
    rows = cur.fetchall()
    cur.close()
    return rows
