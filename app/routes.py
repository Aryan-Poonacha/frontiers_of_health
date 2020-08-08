from app import app, db
from flask import render_template, flash, redirect, session, url_for, request, g, Markup
from flask_login import current_user, login_user, logout_user, login_required

from .forms import StudentLoginForm, TherapistLoginForm, StudentMatchForm, StudentCancelMatchForm
from app.models import Student, Therapist, Match, StudentMatchFormEntry, StudentCancelMatchFormEntry

import datetime

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Frontiers Of Health")


@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if current_user.is_authenticated:
        return redirect(url_for('student_dashboard'))
    form = StudentLoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(username=form.username.data).first()
        if student is None or not student.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(student, remember=form.remember_me.data)
        return redirect(url_for('student_dashboard'))
    return render_template('student login.html', title='Sign In', form=form)


@app.route('/therapist_login', methods=['GET', 'POST'])
def therapist_login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = TherapistLoginForm()
    if form.validate_on_submit():
        therapist = Therapist.query.filter_by(username=form.username.data).first()
        if therapist is None or not therapist.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(therapist, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('therapist login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/student_dashboard')
@login_required
def student_dashboard():
	matches = Match.query.filter_by(student_id=current_user.id).first()
	student = Student.query.filter_by(id=current_user.id).first()
	if matches is None:
		msg = Markup("<br> <a href= '/student_match_form' class='btn'>Get Started</a>")
		flash("It looks like this is your first time! Welcome! To get started, you first need to fill out a short survey. Based on your responses and student profile, we will match you with three therapists to choose from. After that, you can get started!")
		flash(msg)
	return render_template('student dashboard.html', title='Student Dashboard', student = student)


@app.route('/student_match_form', methods=['GET', 'POST'])
@login_required
def student_match_form():
	form = StudentMatchForm()
	student = Student.query.filter_by(id=current_user.id).first()

	if form.validate_on_submit():
		entry = StudentMatchFormEntry(student_id = current_user.id, age = form.age.data, gender = form.gender.data, grade = form.grade.data)
		db.session.add(entry)
		db.session.commit()
		flash("jobs done")
		return redirect(url_for('student_dashboard'))
	
	return render_template('student match form.html', title='Student Match Form', student = student, form = form)

@app.route('/student_cancel_match_form', methods=['GET', 'POST'])
@login_required
def student_cancel_match_form():
	form = StudentCancelMatchForm()
	student = Student.query.filter_by(id=current_user.id).first()

	if form.validate_on_submit():
		
		match = Match.query.filter_by(student_id = current_user.id).first()
		present_time = datetime.datetime.now()
		entry = StudentCancelMatchFormEntry(student_id = current_user.id, confirm = form.confirm.data, reason = form.reason.data, reason_text = form.reason_text.data, datetime = present_time)
		match.end_datetime = present_time
		db.session.add(entry)
		db.session.commit()
		flash("Match succesfully cancelled.")
		return redirect(url_for('student_dashboard'))
	
	return render_template('student cancel match form.html', title='Cancel Match Form', student = student, form = form)