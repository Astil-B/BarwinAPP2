from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required

from app import queries as q
from app.forms import EventForm
from app.decorators import manager_required
from app.util import flash_errors

Events = Blueprint("Events", __name__)


@Events.route("/events")
@login_required
def index():
    return render_template("events.html", events=q.get_all_events(), form=EventForm())


@Events.route("/events", methods=["POST"])
@manager_required
def create():
    form = EventForm()
    if form.validate_on_submit():
        try:
            date = datetime.strptime(form.date.data, "%Y-%m-%d").date()
        except ValueError:
            flash("That calendar date does not exist.", "error")
            return render_template("events.html", events=q.get_all_events(), form=form)
        eid = q.insert_event(
            form.name.data, date, form.description.data or None, form.location.data or None
        )
        flash("Event created.", "success")
        return redirect(url_for("Events.detail", id=eid))
    flash_errors(form)
    return render_template("events.html", events=q.get_all_events(), form=form)


@Events.route("/events/<int:id>")
@login_required
def detail(id):
    event = q.get_event(id)
    if event is None:
        abort(404)
    return render_template(
        "event_detail.html",
        event=event,
        shifts=q.get_shifts_for_event(id),
        summary=q.get_sales_summary(id),
    )


@Events.route("/events/<int:id>/edit")
@manager_required
def edit(id):
    event = q.get_event(id)
    if event is None:
        abort(404)
    form = EventForm(data={
        "name": event.name,
        "date": str(event.date),
        "location": event.location,
        "description": event.description,
    })
    return render_template("event_edit.html", event=event, form=form)


@Events.route("/events/<int:id>/edit", methods=["POST"])
@manager_required
def update(id):
    event = q.get_event(id)
    if event is None:
        abort(404)
    form = EventForm()
    if form.validate_on_submit():
        try:
            date = datetime.strptime(form.date.data, "%Y-%m-%d").date()
        except ValueError:
            flash("That calendar date does not exist.", "error")
            return render_template("event_edit.html", event=event, form=form)
        q.update_event(
            id, form.name.data, date, form.description.data or None, form.location.data or None
        )
        flash("Event updated.", "success")
        return redirect(url_for("Events.detail", id=id))
    flash_errors(form)
    return render_template("event_edit.html", event=event, form=form)


@Events.route("/events/<int:id>/delete", methods=["POST"])
@manager_required
def delete(id):
    if q.get_event(id) is None:
        abort(404)
    q.delete_event(id)
    flash("Event deleted.", "success")
    return redirect(url_for("Events.index"))
