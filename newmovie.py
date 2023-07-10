from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, validators, IntegerField, URLField
from wtforms.validators import DataRequired


class NewMovie(FlaskForm):
    movie_title = StringField(label="Title", validators=[DataRequired(), validators.Length(max=100)])
    # movie_year = IntegerField(label="Year", validators=[DataRequired()])
    # movie_description = StringField(label="Description", validators=[DataRequired(), validators.Length(max=350)])
    # movie_rating = FloatField(label="Rating", validators=[DataRequired()])
    # movie_ranking = IntegerField(label="Ranking", validators=[DataRequired()])
    # movie_review = StringField(label="Review", validators=[DataRequired(), validators.Length(max=250)])
    # movie_image_url = URLField(label="Image url", validators=[DataRequired()])
    Add = SubmitField(label="Add")


