from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt
from flask import current_app as app


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True, nullable=False)
    description = db.Column(db.String(140))
    gender = db.Column(db.String(1), index=True, nullable=False) # M - male, F - female, U - unisex, C - children
    size = db.Column(db.Float, index=True, nullable=False)
    color = db.Column(db.String(10), index=True, nullable=False)
    price = db.Column(db.Integer, index=True, nullable=False)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    cart_item = db.relationship("CartItem", backref="product", lazy="dynamic")
    

    def __repr__(self) -> str:
        return "<Product {}>".format(self.name)

    def update_price(self, price):
        self.price = price
    
    def get_price(self):
        return self.price


class Customer(db.Model, UserMixin):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), index=True, nullable=False)
    last_name = db.Column(db.String(128), index=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    mobile_number = db.Column(db.String(15))
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), index=True)
    status = db.Column(db.Boolean, nullable=False, default=False)
    addresses = db.relationship("Address", backref="customer", lazy="dynamic")
    orders = db.relationship("Order", backref="customer", lazy="dynamic")

    def __repr__(self) -> str:
        return "<Customer: {} {}>".format(self.first_name, self.last_name)

    def is_admin(self):
        return self.role=="Admin"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def activate(self):
        self.status = True
    
    def get_token(self, expires_in=600):
        activation_token = jwt.encode({"email": self.email, "exp": time() + expires_in},
                                        app.config["SECRET_KEY"], algorithm="HS256")
        return activation_token

    @staticmethod
    def verify_token(token):
        try:
            email = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])["email"]
        except:
            return 
        return email

@login_manager.user_loader
def load_user(id):
    return Customer.query.get(int(id))


class Address(db.Model):
    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), index=True)
    first_name = db.Column(db.String(128), index=True, nullable=False)
    last_name = db.Column(db.String(128), index=True, nullable=False)
    mobile_number = db.Column(db.String(15), index=True,)
    address = db.Column(db.String(256), nullable=False)

    
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), index=True, nullable=False)
    shipping_address_id = db.Column(db.Integer, db.ForeignKey("address.id"), index=True, nullable=False)
    billing_address_id = db.Column(db.Integer, db.ForeignKey("address.id"), index=True, nullable=False)
    total_items = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.today, index=True)
    status = db.Column(db.String(1), db.ForeignKey("order_status.id"), nullable=False, default="R")
    items = db.relationship("OrderDetails", backref="order", lazy="dynamic")

    def __repr__(self) -> str:
        return "<Order {}>".format(self.id)


class OrderDetails(db.Model):
    __tablename__ = "order_details"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), index=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), index=True, nullable=False)
    product_name = db.Column(db.String(60))
    product_price = db.Column(db.Integer, nullable=False)
    order_quantity = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.today, index=True)



class OrderStatus(db.Model):
    __tablename__ = "order_status"

    id = db.Column(db.String(1), primary_key=True)
    description = db.Column(db.String(128), nullable=False)

    def __repr__(self) -> str:
        return "<Order Status: {}>".format(self.id)


class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), index=True)
    items = db.relationship("CartItem", backref="cart", lazy="dynamic")


class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)




