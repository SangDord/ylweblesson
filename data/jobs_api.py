from flask import Blueprint, jsonify, make_response
from data import db_session
from data.jobs import Jobs


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
