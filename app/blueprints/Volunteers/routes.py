from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required
from psycopg2 import IntegrityError

from app import conn
from app import queries as q
from app.forms import VolunteerForm
from app.decorators import manager_required
from app.util import flash_errors

Volunteers = Blueprint("Volunteers", __name__)


@Volunteers.route("/volunteers")
@login_required
def index():
    return render_template("volunteers.html", volunteers=q.get_all_volunteers(), form=VolunteerForm())


@Volunteers.route("/volunteers", methods=["POST"])
@manager_required
def create():
    form = VolunteerForm()
    if form.validate_on_submit():
        try:
            vid = q.insert_volunteer(form.name.data, form.email.data, form.phone.data or None)
        except IntegrityError:
            conn.rollback()
            flash("A volunteer with that email already exists.", "error")
            return render_template("volunteers.html", volunteers=q.get_all_volunteers(), form=form)
        flash("Volunteer created.", "success")
        return redirect(url_for("Volunteers.detail", id=vid))
    flash_errors(form)
    return render_template("volunteers.html", volunteers=q.get_all_volunteers(), form=form)


@Volunteers.route("/volunteers/<int:id>")
@login_required
def detail(id):
    volunteer = q.get_volunteer(id)
    if volunteer is None:
        abort(404)
    return render_template(
        "volunteer_detail.html",
        volunteer=volunteer,
        signups=q.get_volunteer_signups(id),
        sales=q.get_volunteer_sales(id),
    )


@Volunteers.route("/volunteers/<int:id>/edit")
@manager_required
def edit(id):
    volunteer = q.get_volunteer(id)
    if volunteer is None:
        abort(404)
    form = VolunteerForm(data={
        "name": volunteer.name,
        "email": volunteer.email,
        "phone": volunteer.phone,
    })
    return render_template("volunteer_edit.html", volunteer=volunteer, form=form)


@Volunteers.route("/volunteers/<int:id>/edit", methods=["POST"])
@manager_required
def update(id):
    volunteer = q.get_volunteer(id)
    if volunteer is None:
        abort(404)
    form = VolunteerForm()
    if form.validate_on_submit():
        try:
            q.update_volunteer(id, form.name.data, form.email.data, form.phone.data or None)
        except IntegrityError:
            conn.rollback()
            flash("A volunteer with that email already exists.", "error")
            return render_template("volunteer_edit.html", volunteer=volunteer, form=form)
        flash("Volunteer updated.", "success")
        return redirect(url_for("Volunteers.detail", id=id))
    flash_errors(form)
    return render_template("volunteer_edit.html", volunteer=volunteer, form=form)


@Volunteers.route("/volunteers/<int:id>/delete", methods=["POST"])
@manager_required
def delete(id):
    if q.get_volunteer(id) is None:
        abort(404)
    q.delete_volunteer(id)
    flash("Volunteer deleted.", "success")
    return redirect(url_for("Volunteers.index"))
