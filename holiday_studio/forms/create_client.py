from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, TelField, EmailField
from wtforms.validators import DataRequired


class CreateClientForm(FlaskForm):
    full_name = StringField("Имя клиента", validators=[DataRequired()])
    age = IntegerField("Возраст", validators=[])
    phone = TelField("Номер телефона", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField("Создать")