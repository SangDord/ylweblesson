from data import db_session
import os, json
from data.users import User
from data.jobs import Jobs
from data.categories import Category, Association
from data.departement import Department
import datetime


def get_member(surname='', name='', age='', position='', speciality='', address='', email='', password=''):
    member = User()
    member.surname = surname
    member.name = name
    member.age = age
    member.position = position
    member.speciality = speciality
    member.address = address
    member.email = email
    member.set_password(password)
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


def get_department(title='', chief=0, members='', email=''):
    department = Department()
    department.title = title
    department.chief = chief
    department.members = members
    department.email = email
    return department


def get_category(name=''):
    category = Category()
    category.name = name
    return category


def get_asso(job=0, category=0):
    asso = Association()
    asso.job = job
    asso.category = category
    return asso
    
    
if __name__ == '__main__':
    if 'mars_mission.sqlite' in os.listdir('db'):
        os.remove('db/mars_mission.sqlite')
    db_session.global_init('db/mars_mission.sqlite')
    session = db_session.create_session()
    with open('templates/members.json') as json_file:
        members = json.load(json_file)
    for member_data in members["Members"].values():
        session.add(get_member(**member_data))
    
    with open('templates/categories.json') as json_file:
        categories = json.load(json_file)
    for category in categories['Categories'].values():
        session.add(get_category(**category))
        
    with open('templates/jobs.json') as json_file:
        jobs = json.load(json_file)
    for job in jobs['Jobs'].values():
        session.add(get_job(**job))
        
    with open('templates/associations.json') as json_file:
        assos = json.load(json_file)
    for asso in assos['Associations'].values():
        session.add(get_asso(**asso))
        
    with open('templates/departments.json') as json_file:
        departs = json.load(json_file)
    for depart in departs['Departments'].values():
        session.add(get_department(**depart))
        
    session.commit()
    session.close()