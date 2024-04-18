from requests import get, post, delete
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
print('Удалим добавленную работу')
print(delete(f'http://localhost:8080/api/jobs/{resp["id"]}').json())
print()
print('Проверим')
pprint(get('http://localhost:8080/api/jobs').json())