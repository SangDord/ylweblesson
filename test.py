from requests import get, post, delete, put
from pprint import pprint


print('Добавим job')
pprint(resp := post('http://localhost:8080/api/jobs',
            json={'team_leader': 2,
                  'job': 'test_job',
                  'work_size': 40,
                  'collaborators': '3, 4',
                  'is_finished': False,
                  'category': 2}).json())
print()
print('Проверим')
pprint(get('http://localhost:8080/api/jobs').json())
print()
print('Пустой запрос')
print(put(f'http://localhost:8080/api/jobs/{resp["id"]}', json={}).json())
print()
print('Oшибочный запрос с некорректным id=999 и неполными параметрами')
print(put('http://localhost:8080/api/jobs/999',
          json={'team_leader': 2}).json())
print()
print('Ошибочный запрос с некорректным id="q"')
print(put('http://localhost:8080/api/jobs/q',
          json={'team_leader': 3,
                'job': 'Edited test job',
                'work_size': 30,
                'collaborators': '2, 4',
                'is_finished': True,
                'category': 3}).json())
print()
print('Ошибочный запрос со связкой с несуществующими существами (не существует тимлида, категории, коллабораторов, категории)')
print(put(f'http://localhost:8080/api/jobs/{resp["id"]}',
          json={'team_leader': 1233,
                'job': 'Edited test job',
                'work_size': 30,
                'collaborators': '122, 99',
                'is_finished': True,
                'category': 123}).json())
print()
print('Ошибочный запрос с неправильными типами данных (job в int, work_size в str, is_finished в str)')
print(put(f'http://localhost:8080/api/jobs/{resp["id"]}',
          json={'team_leader': 3,
                'job': 12423,
                'work_size': '30',
                'collaborators': '2, 4',
                'is_finished': 'True',
                'category': 3}).json())
print()
print('Корректно изменим добавленную работу')
print(put(f'http://localhost:8080/api/jobs/{resp["id"]}',
          json={'team_leader': 3,
                'job': 'Edited test job',
                'work_size': 30,
                'collaborators': '2, 4',
                'is_finished': True,
                'category': 3}).json())
print()
print('Проверим')
pprint(get('http://localhost:8080/api/jobs').json())
print()
print('Корректно удалим добавленную работу')
pprint(delete(f'http://localhost:8080/api/jobs/{resp["id"]}').json())
print()
print('Проверим')
pprint(get('http://localhost:8080/api/jobs').json())