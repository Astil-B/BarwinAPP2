from flask_login import UserMixin
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

from app import conn, login_manager


@login_manager.user_loader
def load_user(user_id):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = sql.SQL("SELECT * FROM app_user WHERE {} = %s").format(sql.Identifier("id"))
    cur.execute(query, (int(user_id),))
    row = cur.fetchone()
    cur.close()
    return User(row) if row else None


class ModelMixin(dict):
    """Dict whose keys are also attributes (event.name)."""

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError as exc:
            raise AttributeError(item) from exc


class User(ModelMixin, UserMixin):
    def __init__(self, row):
        super().__init__(row)
        self.id = row["id"]
        self.username = row["username"]
        self.full_name = row["full_name"]
        self.password = row["password"]
        self.role = row["role"]

    def get_id(self):
        return str(self.id)


class Event(ModelMixin):
    pass


class Volunteer(ModelMixin):
    pass


class Shift(ModelMixin):
    pass


class ShiftSignup(ModelMixin):
    pass


class Drink(ModelMixin):
    pass


class Sale(ModelMixin):
    pass
