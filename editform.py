from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, validators
from wtforms.validators import DataRequired


class Edit(FlaskForm):
    rating = FloatField(label="Rating", validators=[DataRequired()])
    review = StringField(label="Review", validators=[DataRequired(), validators.Length(max=250)])
    submit = SubmitField(label="Done")
