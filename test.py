from requests import get
from pprint import pprint


pprint(get('http://localhost:8080/api/jobs').json())