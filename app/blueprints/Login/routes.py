from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app import bcrypt
from app import queries as q
from app.forms import LoginForm, SignupForm

Login = Blueprint("Login", __name__)


@Login.route("/")
@login_required
def home():
    return render_template("index.html", events=q.get_recent_events())


@Login.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("Login.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = q.get_user_by_username(form.username.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"Welcome back, {user.full_name}.", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("Login.home"))
        flash("Invalid username or password.", "error")
    return render_template("login.html", form=form)


@Login.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("Login.home"))
    form = SignupForm()
    if form.validate_on_submit():
        if q.get_user_by_username(form.username.data):
            flash("That username is already taken.", "error")
        else:
            pw_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            q.insert_user(form.username.data, form.full_name.data, pw_hash, form.user_type.data)
            flash("Account created — please log in.", "success")
            return redirect(url_for("Login.login"))
    return render_template("signup.html", form=form)


@Login.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("Login.login"))
