from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError
from app.db.database import mysql
import MySQLdb

class RegisterForm(FlaskForm):

    auth_name = StringField("Full Name", validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])

    auth_email = StringField("Email", validators=[
        DataRequired(),
        Regexp(r'^[^@]+@agri\.com$', message="Use agri.com domain")
    ])

    auth_phone_no = StringField("Phone Number", validators=[
        DataRequired(),
        Length(min=10, max=15),
        Regexp(r'^\d{10,15}$')
    ])

    auth_pass = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=8)
    ])

    submit = SubmitField("Register")

    def validate_field(self, field, column_name, message):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(
            f"SELECT * FROM auths WHERE {column_name}=%s",
            (field.data,)
        )

        exists = cursor.fetchone()
        cursor.close()

        if exists:
            raise ValidationError(message)

    def validate_auth_email(self, field):
        self.validate_field(field,'auth_email','Email already exists')

    def validate_auth_phone_no(self, field):
        self.validate_field(field,'auth_phone_no','Phone already exists')

    def validate_auth_pass(self, field):
        if field.data != "AgridataNexus@123":
            raise ValidationError("Please enter correct password")


class LoginForm(FlaskForm):

    auth_email = StringField("Email", validators=[DataRequired()])
    auth_pass = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")