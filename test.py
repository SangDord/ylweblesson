from requests import get, post
from pprint import pprint


pprint(post('http://localhost:8080/api/jobs', json={}).json())
print()
pprint(post('http://localhost:8080/api/jobs', json={'team_leader': 1}).json())
print()
pprint(post('http://localhost:8080/api/jobs',
            json={'team_leader': 2,
                  'job': 'test_job',
                  'work_size': 40,
                  'collaborators': '3, 4',
                  'is_finished': False,
                  'category': 2}).json())