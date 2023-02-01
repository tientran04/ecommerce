from . import bp
from flask import render_template, request, redirect, url_for
from app.models import CartItem
from app import db


@bp.route("/cart")
def shopping_cart():
    cart_id = request.cookies.get("cart")
    cart_items = CartItem.query.filter_by(cart_id=cart_id).all()
    return render_template("order/shopping_cart.html", title="Shopping Cart", items=cart_items)


@bp.route("/add-to-bag", methods=["POST"])
def add_to_bag():
    cart_id = request.cookies.get("cart")
    form = request.form
    product_id = form.get("product_id")
    quantity = form.get("quantity")
    cart_item = CartItem.query.filter_by(cart_id=cart_id, product_id=product_id).first()
    prev_url = request.referrer
    if not cart_item:
        cart_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    else:
        cart_item.quantity += int(quantity)
    db.session.commit()
    return redirect(prev_url)


@bp.route("/remove/<product_id>")
def remove_item(product_id):
    cart_id = request.cookies.get("cart")
    cart_item = CartItem.query.filter_by(cart_id=cart_id, product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return redirect(url_for("order.shopping_cart"))
    return redirect(url_for("order.shopping_cart"))


@bp.route("/checkout")
def checkout():
    return render_template("order/checkout.html", title="Checkout")
