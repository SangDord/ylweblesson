from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.jobs import Jobs
from forms.__all_forms import *
import datetime
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ylweblesson_secret_key'


def get_member(surname='', name='', age='', position='', speciality='', address='', email=''):
    member = User()
    member.surname = surname
    member.name = name
    member.age = age
    member.position = position
    member.speciality = speciality
    member.address = address
    member.email = email
    return member


def get_job(team_leader=0, job='', work_size=0, collaborators='', start_date='', is_finished=None):
    job_ob = Jobs()
    job_ob.team_leader = team_leader
    job_ob.job = job
    job_ob.work_size = work_size
    job_ob.collaborators = collaborators
    if start_date:
        if start_date == 'now':
            job_ob.start_date = datetime.datetime.now()
        else:
            job_ob.start_date = datetime.datetime(**start_date)
        job_ob.end_date = job_ob.start_date + datetime.timedelta(hours=work_size)
    job_ob.is_finished = is_finished
    return job_ob


def solution1():
    db_session.global_init('db/mars_mission.sqlite')
    session = db_session.create_session()
    with open('templates/members.json') as json_file:
        members = json.load(json_file)
    for member_data in members["Members"].values():
        session.add(get_member(**member_data))
    session.commit()
    session.close()


def solution2():
    db_session.global_init('db/mars_misson.sqlite')
    session = db_session.create_session()
    with open('templates/members.json') as json_file:
        members = json.load(json_file)
    for member_data in members["Members"].values():
        session.add(get_member(**member_data))
    with open('templates/jobs.json') as json_file:
        jobs = json.load(json_file)
    for job in jobs['Jobs'].values():
        session.add(get_job(**job))
    session.commit()
    session.close()


def solution3():
    if 'mars_mission.sqlite' in os.listdir('db'):
        os.remove('db/mars_mission.sqlite')
    db_session.global_init('db/mars_mission.sqlite')
    session = db_session.create_session()
    with open('templates/members.json') as json_file:
        members = json.load(json_file)
    for member_data in members["Members"].values():
        session.add(get_member(**member_data))
    with open('templates/jobs.json') as json_file:
        jobs = json.load(json_file)
    for job in jobs['Jobs'].values():
        session.add(get_job(**job))
    session.commit()
    session.close()
    app.run(port=8080, host='127.0.0.1')


def solution4():
    db_session.global_init('db/mars_mission.sqlite')
    app.run(port=8080, host='127.0.0.1')


@app.route('/')
def works_log():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template('works_log.html', jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            speciality=form.speciality.data,
            position=form.position.data,
            address=form.address.data,
            age=form.age.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/success')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/success', methods=['GET', 'POST'])
def success():
    return "<h2> You've successfully registered </h2>"


if __name__ == "__main__":
    solution4()
