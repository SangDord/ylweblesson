from requests import get, post, delete, put
from pprint import pprint


print('Пустой запрос на добавление юзера')
pprint(post('http://localhost:8080/api/users', json={}).json())
print()
print('Ошибочный запрос на добавление юзера с неполным набором json-параметра')
pprint(post('http://localhost:8080/api/users',
            json={'surname': 'testsurname',
                  'name': 'testname',
                  'position': 'middle_test',
                  'email': 'test99@mars.org',
                  'password': 'testpass99'}).json())
print()
print('Корректное добавление юзера')
pprint(resp := post('http://localhost:8080/api/users',
            json={'surname': 'testsurname',
                  'name': 'testname',
                  'position': 'middle_test',
                  'speciality': 'test-engineer',
                  'age': 99,
                  'address': 'module_test',
                  'email': 'test99@mars.org',
                  'password': 'testpass99'}).json())
print()
print('Проверка')
pprint(get('http://localhost:8080/api/users').json())
print()
print('Пустой запрос на изменение юзера')
pprint(put(f'http://localhost:8080/api/users/{resp["id"]}', json={}).json())
print()
pprint('Ошибочный запрос на изменение юзера с неполным набором json-параметра')
pprint(put(f'http://localhost:8080/api/users/{resp["id"]}',
           json={'name': 'testname',
                 'position': 'middle_test',
                 'email': 'test99@mars.org',}).json())
print()
print('Корректное изменение добавленного юзера')
pprint(put(f'http://localhost:8080/api/users/{resp["id"]}',
           json={'surname': 'editedsurname',
                  'name': 'editedname',
                  'position': 'middle_testedit',
                  'speciality': 'test-engineer-edit',
                  'age': 123,
                  'address': 'module_test',
                  'email': 'test99@mars.org',
                  'password': 'testpass99'}).json())
print()
print('Получение данных о измененом юзере')
pprint(get(f'http://localhost:8080/api/users/{resp["id"]}').json())
print()
print('Корректное удаление юзера')
pprint(delete(f'http://localhost:8080/api/users/{resp["id"]}').json())
print()
print('Проверка')
pprint(get('http://localhost:8080/api/users').json())