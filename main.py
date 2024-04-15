from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.jobs import Jobs
from forms.__all_forms import *
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ylweblesson_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template('index.html', jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Registration',
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
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():    
        db_sess = db_session.create_session()
        user: User = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', form=form, message='Wrong login or password')
    return render_template('login.html', title='Authorization', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def addjob():
    form = AddjobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(User.id == form.team_leader.data).first():
            return render_template('addjob.html', title='Adding a job',
                                   form=form, message='Team leader does not exist')
        try:
            if not all(isinstance(user_id, int) for user_id in map(int, form.collaborators.data.split(', '))):
                return render_template('addjob.html', title='Adding a job',
                                    form=form, message='Collaborators\'s field is incorrectly filled')
        except ValueError:
            return render_template('addjob.html', title='Adding a job',
                                    form=form, message='Collaborators\'s field is incorrectly filled')
        if not all([not db_sess.query(User).filter(User.id == int(user_id)).first() is None
                    for user_id in form.collaborators.data.split(', ')]):
            return render_template('addjob.html', title='Adding a job', 
                                   form=form, message='Collaborators are incorrectly listed')
        new_job = Jobs()
        new_job.job = form.job.data
        new_job.team_leader = form.team_leader.data
        new_job.work_size = form.work_size.data
        new_job.collaborators = form.collaborators.data
        new_job.is_finished = form.is_finished.data
        db_sess.add(new_job)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title='Adding a job', form=form)
        

@app.route('/editjob/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = AddjobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job: Jobs = db_sess.query(Jobs).filter(Jobs.id == int(id)).first()
        if not (job.team_leader == current_user.id or current_user == 1):
            return render_template('addjob.html', title='Editing a job', form=form, message='Access denied')
        if not db_sess.query(User).filter(User.id == form.team_leader.data).first():
            return render_template('addjob.html', title='Editing a job',
                                   form=form, message='Team leader does not exist')
        try:
            if not all(isinstance(user_id, int) for user_id in map(int, form.collaborators.data.split(', '))):
                return render_template('addjob.html', title='Editing a job',
                                    form=form, message='Collaborators\'s field is incorrectly filled')
        except ValueError:
            return render_template('addjob.html', title='Editing a job',
                                    form=form, message='Collaborators\'s field is incorrectly filled')
        if not all([not db_sess.query(User).filter(User.id == int(user_id)).first() is None
                    for user_id in form.collaborators.data.split(', ')]):
            return render_template('addjob.html', title='Editing a job', 
                                   form=form, message='Collaborators are incorrectly listed')
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title='Editing a job', form=form)
    

if __name__ == "__main__":
    db_session.global_init('db/mars_mission.sqlite')
    app.run(port=8080, host='127.0.0.1')
