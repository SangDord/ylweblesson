from flask_restful import Resource, abort
from flask import jsonify

from data import db_session
from data.users import User
from data.users_reqparser import parser

from re import fullmatch

REGS_MAIL_DOMAINS = ['com', 'org', 'ru']


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")
        

def type_check(*args):
    try:
        for var, cls in args:
            cls(var)
        return True
    except ValueError:
        return False
    

def email_check(email):
    email_pattern = rf"^[a-zA-Z0-9_.+-]+@[a-z-]+\.(?:{'|'.join(REGS_MAIL_DOMAINS)})+$"
    return fullmatch(email_pattern, email)
    
        
class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users: list[User] = session.query(User).all()
        return jsonify({'users': [item.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                                     'speciality', 'address', 'city_from', 'email',
                                                     'modified_date')) for item in users]})
    
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if session.query(User).filter(User.email == args['email']).first():
            abort(409, message=f"Email is already busy")
        if not type_check((args['surname'], str), (args['name'], str), (args['age'], int),
                          (args['position'], str), (args['speciality'], str), (args['address'], str),
                          (args['city_from'], str), (args['email'], str)):
            return abort(400, message='Bad request. Value error')
        if not email_check(args['email']):
            return abort(400, message=f'Bad request. Email incorrect. Use only: {", ".join(REGS_MAIL_DOMAINS)} domains')
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            city_from=args['city_from'],
            email=args['email']
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})
    
    
class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user: User = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                                   'speciality', 'address', 'city_from', 'email',
                                                   'modified_date'))})
    
    def put(self, user_id):
        abort_if_user_not_found(user_id)
        args = parser.parse_args()
        session = db_session.create_session()
        user: User = session.query(User).get(user_id)
        if session.query(User).filter(User.email == args['email'], User.id != user.id).first():
            abort(409, message=f"Email is already busy")
        if not type_check((args['surname'], str), (args['name'], str), (args['age'], int),
                          (args['position'], str), (args['speciality'], str), (args['address'], str),
                          (args['city_from'], str), (args['email'], str)):
            return abort(400, message='Bad request. Value error')
        if not email_check(args['email']):
            return abort(400, message=f'Bad request. Email incorrect. Use only {", ".join(REGS_MAIL_DOMAINS)} domains')
        user.surname = args['surname']
        user.name = args['name']
        user.age = args['age']
        user.position = args['position']
        user.speciality = args['speciality']
        user.address = args['address']
        user.city_from = args['city_from']
        user.email = args['email']
        user.set_password(args['password'])
        session.commit()
        return jsonify({'id': user_id, 'success': 'ok'})
    
    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user: User = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'id': user_id, 'success': 'ok'})
        