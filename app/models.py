from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from flask_login import UserMixin

class Student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    active = db.Column(db.Boolean())

    matches = db.relationship('Match', backref='user', lazy='dynamic')
    match_form_entries = db.relationship('StudentMatchFormEntry', backref='student_user', lazy='dynamic')
    cancel_match_form_entries = db.relationship('StudentCancelMatchFormEntry', backref='student_cancel_user', lazy='dynamic')

    def __repr__(self):
        return '<Student {}>'.format(self.username)

    #as soon as we initialise an object of the class, its password is automatically hashed
    def __init__(self, username, password, active):
        self.username = username
        self.set_password(password)
        self.active = active

    #this method sets the password of a new user, passing in the password as a parameter
    def set_password(self, password):
        self.password = generate_password_hash(password)

    #this method returns True or False depening on whether the input password matches the same one for the username
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Therapist(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    
    matches = db.relationship('Match', backref='caregiver', lazy='dynamic')
    cancel_match_form_entries = db.relationship('StudentCancelMatchFormEntry', backref='cancelled_caregiver', lazy='dynamic')


    def __repr__(self):
        return '<Student {}>'.format(self.username)

    #as soon as we initialise an object of the class, its password is automatically hashed
    def __init__(self, username, password):
        self.username = username
        self.set_password(password)


    #this method sets the password of a new user, passing in the password as a parameter
    def set_password(self, password):
        self.password = generate_password_hash(password)

    #this method returns True or False depening on whether the input password matches the same one for the username
    def check_password(self, password):
        return check_password_hash(self.password, password)

@login.user_loader
def load_student_user(id):
    return Student.query.get(int(id))
def load_therapist_user(id):
    return Therapist.query.get(int(id))

class Match(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
        nullable=False)
	therapist_id = db.Column(db.Integer, db.ForeignKey('therapist.id'),
        nullable=False)
	start_datetime = db.Column(db.DateTime, nullable=False)
	end_datetime = db.Column(db.DateTime, nullable=False)
	cancel_end_datetimes = db.relationship('StudentCancelMatchFormEntry', backref='cancelled_datetimes', lazy='dynamic')

	def __repr__(self):
		return '<Match {}>'.format(self.id)

	def __init__(self, start_datetime):
		self.start_datetime = start_datetime

class StudentMatchFormEntry(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
        nullable=False)
	age = db.Column(db.Integer)
	gender = db.Column(db.String(64))
	grade = db.Column(db.String(64))

	def __repr__(self):
		return '<StudentMatchFormEntry {}>'.format(self.id)

	def __init__(self, age, gender, grade):
		self.age = age
		self.gender = gender
		self.grade = grade

class StudentCancelMatchFormEntry(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
        nullable=False)
	therapist_id = db.Column(db.Integer, db.ForeignKey('therapist.id'),
        nullable=False)
	datetime = db.Column(db.DateTime, db.ForeignKey('match.end_datetime'),
        nullable=False)
	confirm = db.Column(db.String(5))
	reason = db.Column(db.String(64))
	reason_text = db.Column(db.String(64))

	def __repr__(self):
		return '<StudentCancelMatchFormEntry {}>'.format(self.id)

	def __init__(self, confirm, reason, reason_text):
		self.confirm = confirm
		self.reason_text = reason_text
		self.reason = reason