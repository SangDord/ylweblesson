from flask import Blueprint, jsonify, make_response, request
from data import db_session
from data.jobs import Jobs
from data.users import User
from data.categories import Category


blueprint = Blueprint('jobs_api',
                      __name__,
                      template_folder='templates')

@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs: list[Jobs] = db_sess.query(Jobs).all()
    json_res = {
        'jobs': [item.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators',
                                    'start_date', 'end_date', 'is_finished')) for item in jobs]}
    return jsonify(json_res)


@blueprint.route('/api/jobs/<int:job_id>')
def get_job(job_id):
    db_sess = db_session.create_session()
    job: Jobs = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    json_res = {
        'job': job.to_dict(only=('id', 'team_leader', 'job', 'work_size',
                                 'collaborators','start_date', 'end_date', 'is_finished'))}
    return jsonify(json_res)


@blueprint.route('/api/jobs', methods=['POST'])
def add_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in ['team_leader', 'job', 'work_size',
                                                 'collaborators', 'is_finished', 'category']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    elif not(isinstance(request.json['work_size'], int) and isinstance(request.json['is_finished'], bool) and 
             isinstance(request.json['job'], str)):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    if not db_sess.query(User).filter(User.id == request.json['team_leader']).first():
        return make_response(jsonify({'error': 'Bad request'}), 400)
    
    try:
        if not all([not db_sess.query(User).filter(User.id == int(user_id)).first() is None
                                for user_id in request.json['collaborators'].split(', ')]):
            return make_response(jsonify({'error': 'Bad request'}), 400)
    except ValueError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    
    category = db_sess.query(Category).filter(Category.id == request.json['category']).first()
    if not category:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    
    new_job = Jobs()
    new_job.team_leader = request.json['team_leader']
    new_job.job = request.json['job']
    new_job.work_size = request.json['work_size']
    new_job.collaborators = request.json['collaborators']
    new_job.categories.append(category)
    new_job.is_finished = request.json['is_finished']
    
    db_sess.add(new_job)
    db_sess.commit()
    return jsonify({'id': new_job.id})
