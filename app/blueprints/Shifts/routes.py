from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required
from psycopg2 import IntegrityError

from app import conn
from app import queries as q
from app.forms import ShiftForm, SignupActionForm
from app.decorators import manager_required
from app.util import flash_errors, parse_dt

Shifts = Blueprint("Shifts", __name__)


def _event_choices():
    return [(e.id, f"{e.name} ({e.date})") for e in q.get_all_events()]


@Shifts.route("/shifts")
@login_required
def index():
    event_id = request.args.get("event_id", type=int)
    form = ShiftForm()
    form.event_id.choices = _event_choices()
    default_date = None
    if event_id:
        event = q.get_event(event_id)
        if event:
            default_date = event.date.strftime("%d-%m-%Y")
            form.event_id.data = event_id
            form.start_time.data = f"{default_date} "
            form.end_time.data = f"{default_date} "
    return render_template(
        "shifts.html",
        shifts=q.get_all_shifts(event_id),
        form=form,
        selected_event_id=event_id,
    )


@Shifts.route("/shifts", methods=["POST"])
@manager_required
def create():
    form = ShiftForm()
    form.event_id.choices = _event_choices()
    if form.validate_on_submit():
        start, err = parse_dt(form.start_time.data)
        end, err2 = parse_dt(form.end_time.data)
        if err or err2:
            flash(err or err2, "error")
        elif end <= start:
            flash("End time must be after start time.", "error")
        elif q.get_event(form.event_id.data) is None:
            flash("Please select a valid event.", "error")
        else:
            sid = q.insert_shift(form.event_id.data, form.role.data, start, end, form.capacity.data)
            flash("Shift created.", "success")
            return redirect(url_for("Shifts.detail", id=sid))
    else:
        flash_errors(form)
    return render_template("shifts.html", shifts=q.get_all_shifts(), form=form, selected_event_id=None)


@Shifts.route("/shifts/<int:id>")
@login_required
def detail(id):
    shift = q.get_shift(id)
    if shift is None:
        abort(404)
    form = SignupActionForm()
    form.volunteer_id.choices = [(v.id, v.name) for v in q.get_all_volunteers()]
    return render_template(
        "shift_detail.html",
        shift=shift,
        signups=q.get_shift_signups(id),
        form=form,
    )


@Shifts.route("/shifts/<int:id>/signup", methods=["POST"])
@login_required
def signup(id):
    shift = q.get_shift(id)
    if shift is None:
        abort(404)
    form = SignupActionForm()
    form.volunteer_id.choices = [(v.id, v.name) for v in q.get_all_volunteers()]
    if not form.validate_on_submit():
        flash("Please select a valid volunteer.", "error")
        return redirect(url_for("Shifts.detail", id=id))

    volunteer = q.get_volunteer(form.volunteer_id.data)
    if volunteer is None:
        flash("Please select a valid volunteer.", "error")
        return redirect(url_for("Shifts.detail", id=id))

    confirmed = q.count_confirmed_signups(id)
    status = "confirmed" if confirmed < shift.capacity else "waitlisted"
    try:
        q.insert_signup(id, volunteer.id, status)
    except IntegrityError:
        conn.rollback()
        flash("Volunteer is already signed up for this shift.", "error")
        return redirect(url_for("Shifts.detail", id=id))

    if status == "confirmed":
        flash(f"{volunteer.name} signed up (confirmed).", "success")
    else:
        flash(f"{volunteer.name} added to the waitlist (shift is full).", "success")
    return redirect(url_for("Shifts.detail", id=id))


@Shifts.route("/shifts/<int:id>/edit")
@manager_required
def edit(id):
    shift = q.get_shift(id)
    if shift is None:
        abort(404)
    form = ShiftForm(data={
        "event_id": shift.event_id,
        "role": shift.role,
        "start_time": shift.start_time.strftime("%d-%m-%Y %H:%M"),
        "end_time": shift.end_time.strftime("%d-%m-%Y %H:%M"),
        "capacity": shift.capacity,
    })
    form.event_id.choices = _event_choices()
    return render_template("shift_edit.html", shift=shift, form=form)


@Shifts.route("/shifts/<int:id>/edit", methods=["POST"])
@manager_required
def update(id):
    shift = q.get_shift(id)
    if shift is None:
        abort(404)
    form = ShiftForm()
    form.event_id.choices = _event_choices()
    if form.validate_on_submit():
        start, err = parse_dt(form.start_time.data)
        end, err2 = parse_dt(form.end_time.data)
        if err or err2:
            flash(err or err2, "error")
        elif end <= start:
            flash("End time must be after start time.", "error")
        elif q.get_event(form.event_id.data) is None:
            flash("Please select a valid event.", "error")
        else:
            q.update_shift(id, form.event_id.data, form.role.data, start, end, form.capacity.data)
            flash("Shift updated.", "success")
            return redirect(url_for("Shifts.detail", id=id))
    else:
        flash_errors(form)
    return render_template("shift_edit.html", shift=shift, form=form)


@Shifts.route("/shifts/<int:id>/delete", methods=["POST"])
@manager_required
def delete(id):
    if q.get_shift(id) is None:
        abort(404)
    event_id = q.delete_shift(id)
    flash("Shift deleted.", "success")
    return redirect(url_for("Shifts.index", event_id=event_id))
