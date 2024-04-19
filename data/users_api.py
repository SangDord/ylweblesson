from flask import Blueprint, jsonify, make_response, request
from data import db_session
from data.users import User
from pickle import dump
import requests
import datetime


blueprint = Blueprint('users_api',
                      __name__,
                      template_folder='templates')
API_CONFIG = {}
API_CONFIG['GEOCODER_SERVER'] = 'http://geocode-maps.yandex.ru/1.x/'
API_CONFIG['GEOCODER_API_KEY'] = '40d1649f-0493-4b70-98ba-98533de7710b'
API_CONFIG['STATIC_MAPS_SERVER'] = 'http://static-maps.yandex.ru/1.x/'

@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users: list[User] = db_sess.query(User).all()
    json_res = {
        'users': [item.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality',
                                     'address', 'city_from', 'email', 'modified_date')) for item in users]}
    return jsonify(json_res)


@blueprint.route('/api/users/<int:user_id>')
def get_user(user_id):
    db_sess = db_session.create_session()
    user: User = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    json_res = {
        'user': user.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                     'speciality', 'address', 'city_from', 'email', 'modified_date'))}
    return json_res


@blueprint.route('/api/users', methods=['POST'])
def add_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'},), 400)
    if not all(key in request.json for key in ['surname', 'name', 'position', 'speciality', 'age',
                                               'address', 'password', 'email', 'city_from']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    
    db_sess = db_session.create_session()
    
    if db_sess.query(User).filter(User.email == request.json['email']).first():
        return make_response(jsonify({'error': 'Bad request. Email is already busy'}), 400)
    
    if not (isinstance(request.json['name'], str) and isinstance(request.json['surname'], str) and
            isinstance(request.json['age'], int) and isinstance(request.json['position'], str) and
            isinstance(request.json['speciality'], str) and isinstance(request.json['address'], str) and
            isinstance(request.json['city_from'], str)):
        return make_response(jsonify({'error': 'Bad request. Type error'}), 400)
    
    if not isinstance(request.json['email'], str) and '@' not in request.json['email']:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    
    new_user = User()
    new_user.surname = request.json['surname']
    new_user.name = request.json['name']
    new_user.age = request.json['age']
    new_user.position = request.json['position']
    new_user.speciality = request.json['speciality']
    new_user.address = request.json['address']
    new_user.city_from = request.json['city_from']
    new_user.email = request.json['email']
    new_user.set_password(request.json['password'])
    db_sess.add(new_user)
    db_sess.commit()
    return jsonify({'id': new_user.id})
    

@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'},), 400)
    if not all(key in request.json for key in ['surname', 'name', 'position', 'speciality', 'age',
                                               'address', 'password', 'email', 'city_from']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    user: User = db_sess.query(User).get(user_id)
    
    if db_sess.query(User).filter(User.email == request.json['email'], User.id != user.id).first():
        return make_response(jsonify({'error': 'Bad request'}), 400)
    
    if not (isinstance(request.json['name'], str) and isinstance(request.json['surname'], str) and
            isinstance(request.json['age'], int) and isinstance(request.json['position'], str) and
            isinstance(request.json['speciality'], str) and isinstance(request.json['address'], str) and
            isinstance(request.json['city_from'], str)):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    
    if not isinstance(request.json['email'], str) and '@' not in request.json['email']:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    
    user.surname = request.json['surname']
    user.name = request.json['name']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.city_from = request.json['city_from']
    user.email = request.json['email']
    user.set_password(request.json['password'])
    db_sess.commit()
    return jsonify({'id': user.id, 'success': 'ok'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user: User = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'id': user.id, 'success': 'ok'})


@blueprint.route('/api/users_show/<int:user_id>')
def get_city_img(user_id):
    db_sess = db_session.create_session()
    user: User = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    geocoder_params = {
        'apikey': API_CONFIG['GEOCODER_API_KEY'],
        'geocode': user.city_from + ' town',
        'format': 'json'
    }
    response = requests.get(API_CONFIG['GEOCODER_SERVER'], params=geocoder_params)
    if not response:
        return make_response(jsonify({'error': response.reason}), response.status_code)
    
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_lon, toponym_lat = toponym["Point"]["pos"].split(" ")
    
    map_params = {
        'll': ','.join([toponym_lon, toponym_lat]),
        'spn': '0.05,0.05',
        'l': 'sat'
    }
    response = requests.get(API_CONFIG['STATIC_MAPS_SERVER'], params=map_params)
    
    if not response:
        return make_response(jsonify({'error': response.reason}), response.status_code)
    
    return jsonify({'img': str(response.content)})
    