from wtforms import Form, BooleanField, StringField, PasswordField, validators,\
    DateField, FloatField
from flask_wtf import Form
from wtforms.fields.html5 import DateField
from wtforms_components import DateRange
import datetime

today = lambda : datetime.date.today()

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

class NicknameForm(Form):
    nickname = StringField('Nickname',
                [validators.Length(min=4, max=25,
        message='Bitte wähle einen Nickname mit mindestens vier Zeichen!')])

class DonationForm(Form):
    date_donation = DateField('Spendendatum (JJJJ-MM-TT)', format='%Y-%m-%d',
                    validators=[DateRange(max=today(),
                        message='Bitte zuerst spenden, dann eintragen ;)')])
    amount_donation = FloatField('Spendenbetrag',
                [validators.NumberRange(min=1, max=None,
                    message='Wir akzeptieren nur positive Spenden :)')])
    published_name = StringField('Öffentlich aufscheinender Name (zum Verifizieren)')
        # ,[validators.DataRequired(message='Bitte gib einen Namen an!')])

class ConversationForm(Form):
    conversation_name = StringField('Wen hast du überzeugt? ')
    conversation_date = DateField('Datum', format='%Y-%m-%d',
                    validators=[DateRange(max=today(), message='Das Datum muss zwischen 2016-01-01 und Heute liegen.', min=datetime.date    (2016, 1, 1))
                                ])
    conversation_comment = StringField('Kommentar')

# see http://wtforms.simplecodes.com/docs/0.6/validators.html for documentation on validators
# and https://flask-wtf.readthedocs.io/en/latest/quickstart.html
