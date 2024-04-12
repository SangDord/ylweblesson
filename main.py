from data import db_session
from data.users import User
import json


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


def main():
    db_session.global_init('db/mars_misson.sqlite')
    session = db_session.create_session()
    with open('templates/members.json') as json_file:
        members = json.load(json_file)
    for member_data in members["Members"].values():
        session.add(get_member(**member_data))
    session.commit()
    session.close()
    

if __name__ == "__main__":
    main()
