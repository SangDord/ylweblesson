from requests import get
from pprint import pprint


pprint(get('http://localhost:8080/api/jobs/5').json())
pprint(get('http://localhost:8080/api/jobs/q').json())
pprint(get('http://localhost:8080/api/jobs/1').json())