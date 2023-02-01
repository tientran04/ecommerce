from flask import render_template, current_app, abort, request, g
from app.product import bp
from app.models import Product, Cart, CartItem
from datetime import datetime, timedelta
from flask_login import login_required, current_user
from app import db
from .forms import AddToBagForm


"""@bp.before_app_request
def clear_trailing():
    rp = request.path
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])"""


@bp.after_app_request
def set_cookie(response):
    cookie = request.cookies
    cart_id = cookie.get("cart")
    if not cart_id:
        if current_user.is_authenticated:
            cart = Cart(current_user.id)
        else:
            cart = Cart()
        db.session.add(cart)
        db.session.flush()
        response.set_cookie("cart", str(cart.id), samesite="Lax", max_age=2592000)
        db.session.commit()
    return response


@bp.before_app_request
def set_cart_count():
    cookie = request.cookies
    cart_id = cookie.get("cart")
    if cart_id:
        cart_count = CartItem.query.filter_by(cart_id=cart_id).count()
        g.cart_count = cart_count



@bp.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", title="Shoes Shop", products=products)


@bp.route("/collections/womens")
@login_required
def womens():
    products = Product.query.filter_by(gender="F").all()
    return render_template("index.html", title="Women's Shoes", products=products)


@bp.route("/collections/kids")
def kids():
    products = Product.query.filter_by(gender="C").all()
    return render_template("index.html", title="Kid's Shoes", products=products)


@bp.route("/collections/mens")
def mens():
    products = Product.query.filter_by(gender="M").all()
    return render_template("index.html", title="Men's Shoes", products=products)


@bp.route("/collections/womens-new-arrivals")
def womens_new_arrivals():
    to_day = datetime.utcnow()
    new_arrival_date = to_day - timedelta(days=current_app.config["NEW_ARRIVAL_DAYS"])
    products = Product.query.filter_by(gender="F").filter(Product.created_date >= new_arrival_date)
    return render_template("index.html", title="Women's New Arrivals", products=products)


@bp.route("/collections/kids-new-arrivals")
def kids_new_arrivals():
    to_day = datetime.utcnow()
    new_arrival_date = to_day - timedelta(days=current_app.config["NEW_ARRIVAL_DAYS"])
    products = Product.query.filter_by(gender="C").filter(Product.created_date >= new_arrival_date)
    return render_template("index.html", title="Kid's New Arrivals", products=products)


@bp.route("/collections/mens-new-arrivals")
def mens_new_arrivals():
    to_day = datetime.utcnow()
    new_arrival_date = to_day - timedelta(days=current_app.config["NEW_ARRIVAL_DAYS"])
    products = Product.query.filter_by(gender="M").filter(Product.created_date >= new_arrival_date)
    return render_template("index.html", title="Men's New Arrivals", products=products)


@bp.route("/product/<product_name>")
def product_detail(product_name):
    product=Product.query.filter_by(name=product_name).first()
    form = AddToBagForm()
    if not product:
        abort(404)
    form.product_id.data = product.id
    return render_template("product_detail.html", title=product_name, product=product, form=form)