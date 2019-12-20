from flask_wtf import FlaskForm
from wtforms import Form, ValidationError
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField, FloatField, RadioField, \
    IntegerField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Email, Regexp, Length, EqualTo, NumberRange, Required
import re


# class ContactForm(FlaskForm):
#     name = StringField("Name: ", validators=[DataRequired()])
#     email = StringField("Email: ", validators=[Email()])
#     message = TextAreaField("Message", validators=[DataRequired()])
#     submit = SubmitField()

# Custom validator
def password_edit_length(min_length=-1):
    message = "Пароль должен содержать не менее {} символов".format(min_length)

    def _password_edit_length(form, field):
        if len(field.data) != 0 and len(field.data) < min_length:
            raise ValidationError(message=message)

    return _password_edit_length


# Forms
class SearchServicesForm(FlaskForm):
    name_service = StringField("Название")
    min_cost = FloatField("Мин.цена", render_kw={'placeholder': 'Мин'})
    max_cost = FloatField("Макс.цена", render_kw={'placeholder': 'Макс'})
    accept = SubmitField("Применить")


class EditProfileForm(FlaskForm):
    username = StringField("Никнейм", validators=[DataRequired(), Regexp(r"[a-zA-Z_0-9]+",
                                                                         message="Используйте только латинские буквы, "
                                                                                 "цифры и '_'")])
    old_password = PasswordField("Старый пароль")
    password = PasswordField("Пароль", validators=[password_edit_length(min_length=4)])
    confirm_password = PasswordField("Потвердите пароль",
                                     validators=[EqualTo('password', message='Разные пароли!')])
    email = StringField("Email", validators=[Email(message="Неправильный Email"), DataRequired()])
    second_name = StringField("Фамилия", validators=[DataRequired()])
    first_name = StringField("Имя", validators=[DataRequired()])
    middle_name = StringField("Отчество", validators=[DataRequired()])
    phone = StringField("Телефон", validators=[DataRequired(), Regexp(r"\+?\d{11}", message="Неверный формат")])
    submit = SubmitField("Изменить")


class RegistrationForm(FlaskForm):
    username = StringField("Никнейм", validators=[DataRequired(), Regexp(r"[a-zA-Z_0-9]+",
                                                                         message="Используйте только латинские буквы, "
                                                                                 "цифры и '_'")])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=4,
                                                                          message="Пароль должен содержать "
                                                                                  "не менее 4 символов")])
    confirm_password = PasswordField("Потвердите пароль",
                                     validators=[DataRequired(), EqualTo('password', message='Разные пароли!')])
    email = StringField("Email", validators=[Email(message="Неправильный Email"), DataRequired()])
    second_name = StringField("Фамилия", validators=[DataRequired()])
    first_name = StringField("Имя", validators=[DataRequired()])
    middle_name = StringField("Отчество", validators=[DataRequired()])
    phone = StringField("Телефон", validators=[DataRequired(), Regexp(r"\+?\d{11}", message="Неверный формат")])
    submit = SubmitField("Зарегистрироваться")


class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember = BooleanField("Запомнить")
    submit = SubmitField("Войти")


class SendTicketForm(FlaskForm):
    id_employee = IntegerField("ID Ветеринара", validators=[DataRequired()])
    desired_date = StringField("Желаемая дата", validators=[Regexp(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}",
                                                                   message="Формат YYYY-MM-DD HH:MM")])
    submit = SubmitField("Отправить")
