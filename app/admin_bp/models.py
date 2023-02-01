from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_login import current_user
from flask import redirect, url_for


class AdminIndex(AdminIndexView):
    def is_accessible(self):
        return current_user.is_admin()
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("main.index"))


class CustomerView(ModelView):
    form_excluded_columns = ["addresses", "orders"]

    def is_accessible(self):
        return current_user.is_admin()
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("main.index"))


class ProductView(ModelView):
    form_excluded_columns = ["cart_item"]

    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("main.index"))