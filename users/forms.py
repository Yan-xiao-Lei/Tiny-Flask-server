from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from flaskBlog.models import User


class RegForm(FlaskForm):
    username =  StringField('用户名', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('邮箱',validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    confirm_password = PasswordField('确认密码',validators=[DataRequired(), EqualTo('密码')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is taken, please choose another one')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is taken, please choose another one')

class LoginForm(FlaskForm):
    username =  StringField('用户名', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('密码', validators=[DataRequired()])
    isremember = BooleanField('记住我')
    submit = SubmitField('登录')


class UpdateAccountForm(FlaskForm):
    username =  StringField('用户名', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('邮箱',validators=[DataRequired()])
    submit = SubmitField('上传')
    picture = FileField('头像', validators=[FileAllowed(['jpg', 'png'])])

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('That username is taken, please choose another one')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email = email.data).first()
            if email:
                raise ValidationError('That email is taken, please choose another one')


class RequestResetForm(FlaskForm):
    email = StringField('邮箱',validators=[DataRequired()])

    submit = SubmitField('要求密码')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError('没有此账户')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password',validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('重置密码')


