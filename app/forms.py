from flask_wtf import FlaskForm

from flask_wtf.recaptcha import RecaptchaField
from wtforms import StringField, BooleanField, PasswordField, RadioField, IntegerField #normal form validators
from wtforms.fields.html5 import EmailField #html5 form validators

from wtforms.validators import DataRequired, Email, Length, EqualTo

class StudentLoginForm(FlaskForm):
    username = StringField('username', validators = [DataRequired(), Length(min = 3, max = 120)])
    password=PasswordField('password', validators = [DataRequired(), Length(min = 8, max = 120)])
    remember_me = BooleanField('remember_me', default = False)

class TherapistLoginForm(FlaskForm):
    username = StringField('username', validators = [DataRequired(), Length(min = 3, max = 120)])
    password=PasswordField('password', validators = [DataRequired(), Length(min = 8, max = 120)])
    remember_me = BooleanField('remember_me', default = False)

class StudentMatchForm(FlaskForm):
    age = IntegerField('age')
    gender = RadioField('gender', choices = [('M','Male'),('F','Female'), ('O', 'Other')])
    grade = RadioField('grade', choices = [('1','9th Grade (Freshman)'),('2','10th Grade (Sophomore)'), ('3', '11th Grade (Junior)'), ('4', '12th Grade (Senior)')])

class StudentCancelMatchForm(FlaskForm):
    confirm = RadioField('confirm', choices = [('Y','Yes'),('N','No')])
    reason = RadioField('confirm', choices = [('1','Unsatisfactory/Ineffective Counsellor'),('2','Lack Of Time'), ('3', 'Malpractice')])
    reason_text = StringField('username', validators = [Length(max = 500)])