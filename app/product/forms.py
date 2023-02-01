from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired, NumberRange


class AddToBagForm(FlaskForm):
    product_id = HiddenField("Product ID", validators=[DataRequired()], render_kw={'readonly': True})
    quantity = IntegerField("", validators=[DataRequired(), NumberRange(1)], default=1)
    submit = SubmitField("Add to bag")