from flask_restful import Resource, abort
from flask import jsonify

from data import db_session
from data.jobs import Jobs
from data.users import User
from data.categories import Category, Association
from data.jobs_reqparser import parser


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs: list[Jobs] = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators',
                                                    'is_finished')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if not session.query(User).get(args['team_leader']):
            abort(404, message=f'Team leader {args["team_leader"]} not found')
        try:
            if not all([session.query(User).get(int(user_id)) is not None for user_id in args['collaborators'].split(', ')]):
                abort(404, message=f'Collabors {args["collaborators"]} not found')
        except ValueError:
            abort(400, message=f'Wrong Collabors')
        category = session.query(Category).get(args['category'])
        if not category:
            abort(404, message=f'Category {args["category"]} not found')
        
        job = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished'])
        job.categories.append(category)
        session.add(job)
        session.commit()
        return jsonify({'id': job.id})
            

class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job: Jobs = session.query(Jobs).get(job_id)
        return jsonify({'job': [job.to_dict(only=('id', 'team_leader', 'job', 'work_size',
                                            'collaborators', 'is_finished'))]})
        
    def put(self, job_id):
        abort_if_job_not_found(job_id)
        args = parser.parse_args()
        session = db_session.create_session()
        if not session.query(User).get(args['team_leader']):
            abort(404, message=f'Team leader {args["team_leader"]} not found')
        try:
            if not all([session.query(User).get(int(user_id)) is not None for user_id in args['collaborators'].split(', ')]):
                abort(404, message=f'Collabors {args["collaborators"]} not found')
        except ValueError:
            abort(400, message=f'Wrong Collabors')
        category = session.query(Category).get(args['category'])
        if not category:
            abort(404, message=f'Category {args["category"]} not found')
            
        job: Jobs = session.query(Jobs).get(job_id)
        job.team_leader = args['team_leader']
        job.job = args['job']
        job.collaborators = args['collaborators']
        job.work_size = args['work_size']
        job.is_finished = args['is_finished']
        prev_category_id = session.query(Association).get(job.id).category
        job.categories.remove(session.query(Category).get(prev_category_id))
        job.categories.append(category)
        session.commit()
        return jsonify({'id': job_id, 'success': 'ok'})
    
    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job: Jobs = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'id': job_id, 'success': 'ok'})
    