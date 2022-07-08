from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField

class PostsSearch(FlaskForm):
    c = StringField('', validators=[DataRequired()])
    submit = SubmitField('搜索')

