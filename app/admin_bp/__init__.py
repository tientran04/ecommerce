from flask import Blueprint
from app import admin, db
from app.models import Customer, Product
from .models import CustomerView, ProductView, AdminIndex

bp = Blueprint("admin_bp", __name__)


admin.add_view(CustomerView(Customer, db.session))
admin.add_view(ProductView(Product, db.session))
