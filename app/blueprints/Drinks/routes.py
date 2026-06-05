from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required

from app import queries as q
from app.forms import DrinkForm
from app.decorators import manager_required
from app.util import flash_errors

Drinks = Blueprint("Drinks", __name__)


def _grouped(drinks):
    grouped = {}
    for d in drinks:
        grouped.setdefault(d.category or "other", []).append(d)
    return grouped


@Drinks.route("/drinks")
@login_required
def index():
    return render_template("drinks.html", grouped=_grouped(q.get_all_drinks()), form=DrinkForm())


@Drinks.route("/drinks", methods=["POST"])
@manager_required
def create():
    form = DrinkForm()
    if form.validate_on_submit():
        q.insert_drink(form.name.data, form.category.data, form.price_dkk.data, form.unit.data or None)
        flash("Drink created.", "success")
        return redirect(url_for("Drinks.index"))
    flash_errors(form)
    return render_template("drinks.html", grouped=_grouped(q.get_all_drinks()), form=form)


@Drinks.route("/drinks/<int:id>/edit")
@manager_required
def edit(id):
    drink = q.get_drink(id)
    if drink is None:
        abort(404)
    form = DrinkForm(data={
        "name": drink.name,
        "category": drink.category,
        "price_dkk": drink.price_dkk,
        "unit": drink.unit,
    })
    return render_template("drink_edit.html", drink=drink, form=form)


@Drinks.route("/drinks/<int:id>/edit", methods=["POST"])
@manager_required
def update(id):
    drink = q.get_drink(id)
    if drink is None:
        abort(404)
    form = DrinkForm()
    if form.validate_on_submit():
        q.update_drink(id, form.name.data, form.category.data, form.price_dkk.data, form.unit.data or None)
        flash("Drink updated.", "success")
        return redirect(url_for("Drinks.index"))
    flash_errors(form)
    return render_template("drink_edit.html", drink=drink, form=form)


@Drinks.route("/drinks/<int:id>/delete", methods=["POST"])
@manager_required
def delete(id):
    if q.get_drink(id) is None:
        abort(404)
    q.delete_drink(id)
    flash("Drink deleted.", "success")
    return redirect(url_for("Drinks.index"))
