import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "devsecret")


def _connect():
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


conn = _connect()

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "Login.login"
login_manager.login_message_category = "info"

# Importing models registers the Flask-Login user_loader.
from app import models  

# Register blueprints.
from app.blueprints.Login.routes import Login  
from app.blueprints.Events.routes import Events  
from app.blueprints.Shifts.routes import Shifts  
from app.blueprints.Volunteers.routes import Volunteers  
from app.blueprints.Drinks.routes import Drinks 
from app.blueprints.Sales.routes import Sales  

app.register_blueprint(Login)
app.register_blueprint(Events)
app.register_blueprint(Shifts)
app.register_blueprint(Volunteers)
app.register_blueprint(Drinks)
app.register_blueprint(Sales)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500
