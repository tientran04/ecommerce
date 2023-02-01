from flask_mail import Message
from app import mail
from threading import Thread
from flask import current_app as app
from flask import render_template


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app._get_current_object(), msg)).start()


def send_activation_mail(user):
    activation_token = user.get_token()
    subject = "[eCommerce] Activate Account"
    sender = app.config["ADMINS"][0]
    recipients = [user.email]
    text_body = render_template("email/account_activation.txt", user=user, token=activation_token)
    html_body = render_template("email/account_activation.html", user=user, token=activation_token)
    send_email(subject, sender, recipients, text_body, html_body)


def send_forgot_password_mail(user):
    activation_token = user.get_token()
    subject = "[eCommerce] Password Reset"
    sender = app.config["ADMINS"][0]
    recipients = [user.email]
    text_body = render_template("email/forgot_password.txt", user=user, token=activation_token)
    html_body = render_template("email/forgot_password.html", user=user, token=activation_token)
    send_email(subject, sender, recipients, text_body, html_body)
    