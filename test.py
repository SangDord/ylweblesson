from requests import get
from pprint import pprint


print('Получение всех работ')
pprint(get('http://localhost:8080/api/jobs').json())
print()
print('Корректное получение одной работы (id=1)')
pprint(get('http://localhost:8080/api/jobs/1').json())
print()
print('Ошибочный запрос на получение одной работы (id=99)')
pprint(get('http://localhost:8080/api/jobs/99').json())
print()
print('Ошибочный запрос на получение одной работы (id="stroka")')
pprint(get('http://localhost:8080/api/jobs/stroka').json())