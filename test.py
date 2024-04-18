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
print('Изменим добавленную работу')
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