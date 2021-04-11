from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username aleady exists")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Email already in use")


class BuilderForm(FlaskForm):
    project_name = StringField("Project Name", validators=[DataRequired()])
    blockchain_type = SelectField("Blockchain Type", choices=[("corda", "Corda"), ("eth", "Ethereum")])
    submit = SubmitField("Plan")


class SecretForm(FlaskForm):
    secret_name = StringField("Secret Name", validators=[DataRequired()])
    secret_type = SelectField("Secret Type", choices=[("SSH", "SSH Keys"), ("PROJECT_JSON", "Project JSON")])
    secret_content = TextAreaField("Secret Content", validators=[DataRequired()])
    submit = SubmitField("Save")
