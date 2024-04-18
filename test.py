from requests import get, post
from pprint import pprint


print('Пустой запрос')
pprint(post('http://localhost:8080/api/jobs', json={}).json())
print()
print('Ошибочный запрос с недостаточными данными')
pprint(post('http://localhost:8080/api/jobs', json={'team_leader': 1}).json())
print()
print('Ошибочный запрос со связкой с несуществующими существами (не существует тимлида, категории, коллабораторов, категории)')
pprint(post('http://localhost:8080/api/jobs',
            json={'team_leader': 123,
                  'job': 'test_job',
                  'work_size': 40,
                  'collaborators': '15, 99',
                  'is_finished': False,
                  'category': 85}).json())
print()
print('Ошибочный запрос с неправильными типами данных (job в int, work_size в int, is_finished в str)')
pprint(post('http://localhost:8080/api/jobs',
            json={'team_leader': 2,
                  'job': 132,
                  'work_size': '40',
                  'collaborators': '3, 4',
                  'is_finished': 'False',
                  'category': 2}).json())
print()
print('Коррекный запрос')
pprint(post('http://localhost:8080/api/jobs',
            json={'team_leader': 2,
                  'job': 'test_job',
                  'work_size': 40,
                  'collaborators': '3, 4',
                  'is_finished': False,
                  'category': 2}).json())
print()
print('Проверка исполнения запроса')
pprint(get('http://localhost:8080/api/jobs').json())