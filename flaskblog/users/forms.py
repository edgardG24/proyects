from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Correo',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este usuario ya ha sido tomado. Por favor elige otro.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este correo ya esta registrado. Por favor escoge otro diferente.')


class LoginForm(FlaskForm):
    email = StringField('Correo',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recuerdame')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Nombre de usuario',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Correo',
                        validators=[DataRequired(), Email()])
    picture = FileField('Actualizar imagen de perfil', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Actualizar')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Este usuario ya ha sido tomado. Por favor escoge otro diferente..')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Ese correo ya exite. Por favor elige otro.')


class RequestResetForm(FlaskForm):
    email = StringField('Correo',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Solicitud de cambiar contraseña')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No hay una cuenta con ese correo. Debes registrarte primero.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cambiar contraseña')