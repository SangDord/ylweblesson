from requests import get, post, delete, put
from pprint import pprint

HOST, PORT = '127.0.0.1', 8080

def TestUserAddEmtpy():
    data = {}
    resp = post(f'http://{HOST}:{PORT}/api/v2/users', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())


def TestUserAddNotEnoughJson():
    data = {'surname': 'Test', 'name': 'nametest', 'age': 12}
    resp = post(f'http://{HOST}:{PORT}/api/v2/users', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())
    

def TestUserAddWithValueError():
    data = {
            "surname": "tsurname",
            "name": "tname",
            "age": "18adsfe",
            "position": "middle_test",
            "speciality": "testing engineer",
            "address": "module_test",
            "email": "tesdt@marg.org",
            "city_from": "Elista",
            "password": "123456qwe"
            }
    resp = post(f'http://{HOST}:{PORT}/api/v2/users', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())


def TestUserAddAlreadyExist():
    data = {
            "surname": "tsurname",
            "name": "tname",
            "age": 18,
            "position": "middle_test",
            "speciality": "testing engineer",
            "address": "module_test",
            "email": "scott_chief@mars.org",
            "city_from": "Elista",
            "password": "123456qwe"
            }
    resp = post(f'http://{HOST}:{PORT}/api/v2/users', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())
    

def TestUserAddEmailIncorrect1():
    data = {
            "surname": "tsurname",
            "name": "tname",
            "age": 18,
            "position": "middle_test",
            "speciality": "testing engineer",
            "address": "module_test",
            "email": "te@asdfe@marg.org",
            "city_from": "Elista",
            "password": "123456qwe"
            }
    resp = post(f'http://{HOST}:{PORT}/api/v2/users', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())


def TestUserAddEmailIncorrect2():
    data = {
            "surname": "tsurname",
            "name": "tname",
            "age": 18,
            "position": "middle_test",
            "speciality": "testing engineer",
            "address": "module_test",
            "email": "tesdfe@marg12.org",
            "city_from": "Elista",
            "password": "123456qwe"
            }
    resp = post(f'http://{HOST}:{PORT}/api/v2/users', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())


def TestUserAddEmailIncorrect3():
    data = {
            "surname": "tsurname",
            "name": "tname",
            "age": 18,
            "position": "middle_test",
            "speciality": "testing engineer",
            "address": "module_test",
            "email": "tesdfe@marg.test",
            "city_from": "Elista",
            "password": "123456qwe"
            }
    resp = post(f'http://{HOST}:{PORT}/api/v2/users', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())
    
    
def CorrectTestUserAdd():
    data = {
            "surname": "tsurname",
            "name": "tname",
            "age": 18,
            "position": "middle_test",
            "speciality": "testing engineer",
            "address": "module_test",
            "email": "tesdfe@marg.org",
            "city_from": "Elista",
            "password": "123456qwe"
            }
    resp = post(f'http://{HOST}:{PORT}/api/v2/users', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())
    if resp.status_code == 200:
        print('Проверка')
        pprint(get(f'http://{HOST}:{PORT}/api/v2/users/{resp.json()["id"]}').json())
        print()
        print('Удаление пользователя (во избежания проблем с уже сущеcтвующим email)')
        pprint(delete(f'http://{HOST}:{PORT}/api/v2/users/{resp.json()["id"]}').json())


def TestEmptyUserEdit():
    data = {}
    resp = put(f'http://{HOST}:{PORT}/api/v2/users/2', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())
    
    
def TestUserEditNotEnoughJson():
    data = {'surname': 'Test', 'name': 'nametest', 'age': 12}
    resp = put(f'http://{HOST}:{PORT}/api/v2/users/2', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())
    
    
def CorrectTestUserEdit():
    print('Добавим пользователя')
    data = {
            "surname": "tsurname",
            "name": "tname",
            "age": 18,
            "position": "middle_test",
            "speciality": "testing engineer",
            "address": "module_test",
            "email": "tesdfe@marg.org",
            "city_from": "Elista",
            "password": "123456qwe"
            }
    resp = post(f'http://{HOST}:{PORT}/api/v2/users', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())
    
    print()
    print('Проверим')
    pprint(get(f'http://{HOST}:{PORT}/api/v2/users/{resp.json()["id"]}').json())
    
    print()
    print('Отредактируем')
    data = {
            "surname": "edsurname",
            "name": "edname",
            "age": 18,
            "position": "middle_tested",
            "speciality": "testing ed engineer",
            "address": "module_tested",
            "email": "tesdfe@marged.org",
            "city_from": "Elista",
            "password": "123456qwef"
            }
    resp_edit = put(f'http://{HOST}:{PORT}/api/v2/users/{resp.json()["id"]}', json=data)
    print('url:', resp_edit.url, '\njson-body:', data, '\nstatus-code:', resp_edit.status_code,
          '\nmethod:', resp_edit.request.method, '\nresponse| ', end='')
    pprint(resp_edit.json())
    if resp_edit.status_code == 200:
        print('Проверка')
        pprint(get(f'http://{HOST}:{PORT}/api/v2/users/{resp.json()["id"]}').json())
        print()
        print('Удаление пользователя (во избежания проблем с уже сущеcтвующим email)')
        pprint(delete(f'http://{HOST}:{PORT}/api/v2/users/{resp.json()["id"]}').json())


def TestGetUsers():
    resp = get(f'http://{HOST}:{PORT}/api/v2/users')
    print('url:', resp.url, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())
    
    
if __name__ == '__main__':
    option = {0: ['Пустой запрос на добавление пользователя',
                  TestUserAddEmtpy],
              1: ['Запрос на добавление пользователя с неполным json',
                  TestUserAddNotEnoughJson],
              2: ['Запрос на добавление пользователя с некорректным значением (age)',
                  TestUserAddWithValueError],
              3: ['Запрос на добавление пользователя с уже существующим email',
                  TestUserAddAlreadyExist],
              4: ['Запрос на добавления пользователя с неправильным email (лишний символ @)',
                  TestUserAddEmailIncorrect1],
              5: ['Запрос на добавления пользователя с неправильным email (неправильный домен)',
                  TestUserAddEmailIncorrect2],
              6: ['Запрос на добавления пользователя с неправильным email (неподдерживающий домен верхнего уровня)',
                  TestUserAddEmailIncorrect3],
              7: ['Запрос на добавление пользователя',
                  CorrectTestUserAdd],
              8: ['Пустой запрос на изменение пользователя',
                  TestEmptyUserEdit],
              9: ['Запрос на изменение пользователя с неполным json',
                  TestUserEditNotEnoughJson],
              10: ['Запрос на изменение пользователя', 
                   CorrectTestUserEdit],
              11: ['Запрос на получение всех пользователей',
                   TestGetUsers]}
    choice = -2
    print('-1 - выход из программы')
    while choice != -1:
        print('Выберете тест введя соответствующую цифру')
        for k, v in option.items():
            print(f'[{k}] -', v[0])
        try:
            choice = int(input('Выбор| '))
        except ValueError:
            continue
        print()
        if test := option.get(choice, False):
            test[1]()
        else:
            continue
        print()
    print('Пока-пока')