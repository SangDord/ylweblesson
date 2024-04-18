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
print('Ошибочный запрос с несущеcтвующим id=999')
pprint(delete(f'http://localhost:8080/api/jobs/999').json())
print()
print('Ошибочный запрос с несущеcтвующим id="deleteit"')
pprint(delete(f'http://localhost:8080/api/jobs/deleteit').json())
print()
print('Корректно удалим добавленную работу')
pprint(delete(f'http://localhost:8080/api/jobs/{resp["id"]}').json())
print()
print('Проверим')
pprint(get('http://localhost:8080/api/jobs').json())