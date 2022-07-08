from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    content = TextAreaField('简述', validators=[DataRequired()])
    body = TextAreaField('内容', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('提交')

