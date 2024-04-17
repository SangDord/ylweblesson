from flask import Flask, render_template, redirect, abort, make_response, jsonify
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.categories import Category, Association
from data.departement import Department
from forms.__all_forms import *
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import jobs_api


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
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
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
                
            if not all([not db_sess.query(User).filter(User.id == int(user_id)).first() is None
                        for user_id in form.collaborators.data.split(', ')]):
                return render_template('addjob.html', title='Adding a job', 
                                    form=form, message='Collaborators are incorrectly listed')
                
        except ValueError:
            return render_template('addjob.html', title='Adding a job',
                                    form=form, message='Collaborators\'s field is incorrectly filled')

        category = db_sess.query(Category).filter(Category.id == form.category.data).first()
        if not category:
            return render_template('addjob.html', title='Adding a job',
                                   form=form, message='Category does not exist')
        new_job = Jobs()
        new_job.job = form.job.data
        new_job.team_leader = form.team_leader.data
        new_job.work_size = form.work_size.data
        new_job.collaborators = form.collaborators.data
        new_job.categories.append(category)
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
        if not (job.team_leader == current_user.id or current_user.id == 1):
            return render_template('addjob.html', title='Editing a job', form=form, message='Access denied')
        
        if not db_sess.query(User).filter(User.id == form.team_leader.data).first():
            return render_template('addjob.html', title='Editing a job',
                                   form=form, message='Team leader does not exist')
            
        try:
            if not all(isinstance(user_id, int) for user_id in map(int, form.collaborators.data.split(', '))):
                return render_template('addjob.html', title='Editing a job',
                                       form=form, message='Collaborators\'s field is incorrectly filled')
                
            if not all([not db_sess.query(User).filter(User.id == int(user_id)).first() is None
                    for user_id in form.collaborators.data.split(', ')]):
                return render_template('addjob.html', title='Editing a job',
                                       form=form, message='Collaborators are incorrectly listed')
                
        except ValueError:
            return render_template('addjob.html', title='Editing a job',
                                    form=form, message='Collaborators\'s field is incorrectly filled')
            
        category = db_sess.query(Category).filter(Category.id == form.category.data).first()
        if not category:
            return render_template('addjob.html', title='Adding a job',
                                   form=form, message='Category does not exist')
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        prev_category_id = db_sess.query(Association).filter(Association.job == job.id).first().category
        job.categories.remove(db_sess.query(Category).filter(Category.id == prev_category_id).first())
        job.categories.append(category)
        job.is_finished = form.is_finished.data
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title='Editing a job', form=form)


@app.route('/deletejob/<int:id>', methods=['GET', 'POST'])
@login_required
def deletejob(id):
    db_sess = db_session.create_session()
    job: Jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if job.team_leader == current_user.id or current_user.id == 1:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/departments')
def departments():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    return render_template('departments.html', departments=departments)


@app.route('/departments/adddepartment', methods=['GET', 'POST'])
@login_required
def adddepartments():
    form = AdddepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(User.id == form.chief.data).first():
            return render_template('adddepartment.html', title='Adding a department',
                                   form=form, message='Chief does not exist')
            
        try:
            if not all(isinstance(user_id, int) for user_id in map(int, form.members.data.split(', '))):
                return render_template('adddepartment.html', title='Adding a department',
                                    form=form, message='Members\'s field is incorrectly filled')
                
            if not all([not db_sess.query(User).filter(User.id == int(user_id)).first() is None
                        for user_id in form.members.data.split(', ')]):
                return render_template('adddepartment.html', title='Adding a department', 
                                    form=form, message='Members are incorrectly listed')
                
        except ValueError:
            return render_template('adddepartment.html', title='Adding a department',
                                    form=form, message='Members\'s field is incorrectly filled')
            
        new_department = Department()
        new_department.title = form.title.data
        new_department.chief = form.chief.data
        new_department.members = form.members.data
        new_department.email = form.email.data
        db_sess.add(new_department)
        db_sess.commit()
        return redirect('/departments')
    return render_template('adddepartment.html', title='Adding a department', form=form)
        

@app.route('/departments/editdepartment/<int:id>', methods=['GET', 'POST'])
@login_required
def editdepartment(id):
    form = AdddepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department: Department = db_sess.query(Department).filter(Department.id == id).first()
        if not (department.chief == current_user.id or current_user.id == 1):
            return render_template('adddepartment.html', title='Editing a department',
                                   form=form, message='Access denied')
            
        if not db_sess.query(User).filter(User.id == form.chief.data).first():
            return render_template('adddepartment.html', title='Editing a department',
                                   form=form, message='Chief does not exist')
        
        try:
            if not all(isinstance(user_id, int) for user_id in map(int, form.members.data.split(', '))):
                return render_template('adddepartment.html', title='Editing a department',
                                    form=form, message='Members\'s field is incorrectly filled')
                
            if not all([not db_sess.query(User).filter(User.id == int(user_id)).first() is None
                        for user_id in form.members.data.split(', ')]):
                return render_template('adddepartment.html', title='Editing a department', 
                                    form=form, message='Members are incorrectly listed')
                
        except ValueError:
            return render_template('adddepartment.html', title='Editing a department',
                                    form=form, message='Members\'s field is incorrectly filled')
        
        department.title = form.title.data
        department.chief = form.chief.data
        department.members = form.members.data
        department.email = form.email.data
        db_sess.commit()
        return redirect('/departments')
    return render_template('adddepartment.html', title='Editing a department', form=form)
        
    
@app.route('/departments/deletedepartment/<int:id>')
@login_required
def deletedepartment(id):
    db_sess = db_session.create_session()
    department: Department = db_sess.query(Department).filter(Department.id == id).first()
    if department.chief == current_user.id or current_user.id == 1:
        db_sess.delete(department)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')

   
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == "__main__":
    db_session.global_init('db/mars_mission.sqlite')
    app.register_blueprint(jobs_api.blueprint)
    app.run(port=8080, host='127.0.0.1')
