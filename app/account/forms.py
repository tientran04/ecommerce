from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app.models import Customer


class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()], 
                        render_kw={"placeholder": "Your Email Address"})
    password = PasswordField("Password", validators=[DataRequired()],
                            render_kw={"placeholder": "Your Password"})
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()], 
                            render_kw={"placeholder": "e.g. John"})
    last_name = StringField("Last Name", validators=[DataRequired()],
                            render_kw={"placeholder": "e.g. Smith"})
    email = StringField("Email Address", validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Your Email Address"})
    password = PasswordField("Password", validators=[DataRequired()], 
                            render_kw={"placeholder": "Your Password"})
    password2 = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")], 
                                render_kw={"placeholder": "Your Password"})
    submit = SubmitField("Register")

    def validate_email(self, email):
        user = Customer.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Please use a different email.")


class ForgotPasswordForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()], 
                        render_kw={"placeholder": "Your Email Address"})
    submit = SubmitField("Submit Details")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()], 
                            render_kw={"placeholder": "Your Password"})
    password2 = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", "Must be the same as Password")], 
                                render_kw={"placeholder": "Your Password"})
    submit = SubmitField("Submit")


class ActivationRequestForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()], 
                        render_kw={"placeholder": "Your Email Address"})
    submit = SubmitField("Send Request")


class EditDetailsForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()], 
                            render_kw={"placeholder": "e.g. John"})
    last_name = StringField("Last Name", validators=[DataRequired()],
                            render_kw={"placeholder": "e.g. Smith"})
    email = StringField("Email Address", validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Your Email Address"})
    mobile_number = StringField("Mobile Number")
    password = PasswordField("Password", validators=[DataRequired()], 
                            render_kw={"placeholder": "Your Password"})
    submit = SubmitField("Save Changes")

    def __init__(self, original_email, *args, **kwargs):
        super(EditDetailsForm, self).__init__(*args, **kwargs)
        self.original_email = original_email


    def validate_email(self, email):
        if email.data != self.original_email:
            user = Customer.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Please use a different email.")


class UpdatePasswordForm(FlaskForm):
    password = PasswordField("Current Password", validators=[DataRequired()], 
                            render_kw={"placeholder": "Your Current Password"})
    password2 = PasswordField("New Password", validators=[DataRequired()], 
                            render_kw={"placeholder": "Your New Password"})
    password3 = PasswordField("Repeat New Password", validators=[DataRequired(), EqualTo("password2", "Must be the same as New Password")], 
                                render_kw={"placeholder": "Your New Password"})
    submit = SubmitField("Submit")


class AddressForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    mobile_number = StringField("Mobile Number")
    submit = SubmitField("Save Address")