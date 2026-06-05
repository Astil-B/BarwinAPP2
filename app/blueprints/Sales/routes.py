from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required

from app import queries as q
from app.forms import SaleForm
from app.decorators import manager_required
from app.util import flash_errors

Sales = Blueprint("Sales", __name__)


def _populate(form):
    form.event_id.choices = [(e.id, f"{e.name} ({e.date})") for e in q.get_all_events()]
    form.drink_id.choices = [(d.id, f"{d.name} ({d.price_dkk} DKK)") for d in q.get_all_drinks()]
    form.volunteer_id.choices = [(v.id, v.name) for v in q.get_all_volunteers()]
    return form


def _render(form, event_id):
    return render_template(
        "sales.html",
        sales=q.get_all_sales(event_id),
        events=q.get_all_events(),
        form=form,
        selected_event_id=event_id,
        summary=q.get_sales_summary(event_id) if event_id else None,
    )


@Sales.route("/sales")
@login_required
def index():
    event_id = request.args.get("event_id", type=int)
    form = _populate(SaleForm())
    if event_id:
        form.event_id.data = event_id
    return _render(form, event_id)


@Sales.route("/sales", methods=["POST"])
@manager_required
def create():
    form = _populate(SaleForm())
    if form.validate_on_submit():
        q.insert_sale(form.event_id.data, form.drink_id.data, form.volunteer_id.data, form.quantity.data)
        flash("Sale recorded.", "success")
        return redirect(url_for("Sales.index", event_id=form.event_id.data))
    flash_errors(form)
    return _render(form, form.event_id.data if form.event_id.data else None)


@Sales.route("/sales/<int:id>/delete", methods=["POST"])
@manager_required
def delete(id):
    event_id = q.delete_sale(id)
    if event_id is None:
        abort(404)
    flash("Sale deleted.", "success")
    return redirect(url_for("Sales.index", event_id=event_id))


@Sales.route("/sales/summary/<int:event_id>")
@login_required
def summary(event_id):
    if q.get_event(event_id) is None:
        abort(404)
    form = _populate(SaleForm())
    form.event_id.data = event_id
    return _render(form, event_id)
