from app.account import bp
from flask import render_template, flash, redirect, url_for, request
from .forms import LoginForm, RegistrationForm, ForgotPasswordForm, ActivationRequestForm, \
    ResetPasswordForm, EditDetailsForm, UpdatePasswordForm, AddressForm
from app import db
from app.models import Customer, Address
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.email import send_activation_mail, send_forgot_password_mail


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()
        if not user or not user.verify_password(form.password.data):
            flash("Invalid email or password.")
            return redirect(url_for("account.login"))
        if user.status is False:
            flash("Your account is not activated. Please activate your account.")
            return redirect(url_for("account.login"))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template("account/login.html", form=form, title="Login")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = Customer(first_name=form.first_name.data, last_name=form.last_name.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        send_activation_mail(user)
        flash("Your account has been registered. Please follow the link in the email to activate your account.")
        return redirect(url_for("account.login"))
    return render_template("account/register.html", form=form, title="Register")


@bp.route("/activation/<token>")
def activation(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    email = Customer.verify_token(token)
    user = Customer.query.filter_by(email=email).first()
    if not user:
        flash("Activation link is expried. Please request a new activation link.")
        return redirect(url_for("account.activation_request"))
    user.activate()
    db.session.commit()
    flash("Your account has been activated.")
    return redirect(url_for("account.login"))


@bp.route("/activation-request", methods=["GET", "POST"])
def activation_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = ActivationRequestForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()
        if user.status is True:
            flash("Your account has been activated already.")
            return redirect(url_for("account.login"))
        send_activation_mail(user)
        flash("Please follow the link in the email to activate your account.")
        return redirect(url_for("account.login"))
    return render_template("account/activation_request.html", title="Activation Request", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()
        if user:
            send_forgot_password_mail(user)
        flash("Please check email for password reset.")
        return redirect(url_for("account.login"))
    return render_template("account/forgot_password.html", title="Forgot Password", form=form)


@bp.route("/forgot-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    email = Customer.verify_token(token)
    user = Customer.query.filter_by(email=email).first()
    if not user:
        flash("Reset password link is expried. Please request a new reset password link.")
        return redirect(url_for("account.forgot_password"))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset.")
        return redirect(url_for("account.login"))
    return render_template("account/reset_password.html", title="Reset Password", form=form)


@bp.route("/about")
@login_required
def about():
    return render_template("account/about.html", title="Account")


@bp.route("/edit-details", methods=["GET", "POST"])
@login_required
def edit_details():
    form = EditDetailsForm(current_user.email)
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.mobile_number = form.mobile_number.data
            current_user.email = form.email.data
            db.session.commit()
            flash("Your changes have been saved.")
            return redirect(url_for("account.about"))
        else:
            form.first_name.data = form.first_name.data
            form.last_name.data = form.last_name.data
            form.email.data = form.email.data
            form.mobile_number.data = form.mobile_number.data
            flash("Invalid password.")
    elif request.method=="GET":
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.mobile_number.data = current_user.mobile_number
    return render_template("account/edit_details.html", title="Account Details", form=form)


@bp.route("/update-password", methods=["GET", "POST"])
@login_required
def update_password():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.set_password(form.password2.data)
            db.session.commit()
            flash("Your password has been updated.")
            logout_user()
            return redirect(url_for("account.login"))
        flash("Invalid current password.")
    return render_template("account/update_password.html", title="Update Password", form=form)


@bp.route("/add-address", methods=["GET", "POST"])
@login_required
def add_address():
    form = AddressForm()
    if form.validate_on_submit():
        address = Address(customer_id=current_user.id, first_name=form.first_name.data, 
                            last_name=form.last_name.data, mobile_number=form.mobile_number.data, 
                            address=form.address.data)
        db.session.add(address)
        db.session.commit()
        flash("Your address has been added.")
        return redirect(url_for("account.about"))
    elif request.method=="GET":
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.mobile_number.data = current_user.mobile_number
    return render_template("address/add_address.html", title="Add Address", form=form)


@bp.route("/edit-address/<id>", methods=["GET", "POST"])
@login_required
def edit_address(id):
    form = AddressForm()
    address = Address.query.get(int(id))
    if form.validate_on_submit():
        address.first_name = form.first_name.data
        address.last_name = form.last_name.data
        address.mobile_number = form.mobile_number.data
        address.address = form.address.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("account.about"))
    elif request.method=="GET":
        form.first_name.data = address.first_name
        form.last_name.data = address.last_name
        form.mobile_number.data = address.mobile_number
        form.address.data = address.address
    return render_template("address/add_address.html", title="Edit Address", form=form)