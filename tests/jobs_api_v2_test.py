from requests import get, post, delete, put
from pprint import pprint

HOST, PORT = '127.0.0.1', 8080

def TestJobAddEmtpy():
    data = {}
    resp = post(f'http://{HOST}:{PORT}/api/v2/jobs', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())
    

def TestJobAddNotEnoughJson():
    data = {'team_leader': 2, 'work_size': 30, 'collaborators': '1, 3, 4'}
    resp = post(f'http://{HOST}:{PORT}/api/v2/jobs', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())
    
    
def TestJobAddWithValueError():
    data = {
            'team_leader': 2,
            'work_size': '15a',
            'collaborators': '1, 3, 4',
            'job': 'testjob',
            'category': 1,
            'is_finished': 'True'
            }
    resp = post(f'http://{HOST}:{PORT}/api/v2/jobs', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())
    

def TestJobAddWithNotExistUsers1():
    data = {
            'team_leader': 10,
            'work_size': 15,
            'collaborators': '1, 3, 4',
            'job': 'testjob',
            'category': 1,
            'is_finished': True
            }
    resp = post(f'http://{HOST}:{PORT}/api/v2/jobs', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())
    

def TestJobAddWithNotExistUsers2():
    data = {
            'team_leader': 2,
            'work_size': 15,
            'collaborators': '1, 3, 40',
            'job': 'testjob',
            'category': 1,
            'is_finished': True
            }
    resp = post(f'http://{HOST}:{PORT}/api/v2/jobs', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())
    
    
def TestJobAddWithNotExistCategory():
    data = {
            'team_leader': 2,
            'work_size': 15,
            'collaborators': '1, 3, 4',
            'job': 'testjob',
            'category': 5,
            'is_finished': True
            }
    resp = post(f'http://{HOST}:{PORT}/api/v2/jobs', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())
    

def TestJobEditEmtpy():
    data = {}
    resp = put(f'http://{HOST}:{PORT}/api/v2/jobs/1', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())
    
    
def TestJobEditNotExistJob():
    data = {
            'team_leader': 2,
            'work_size': 15,
            'collaborators': '1, 3, 4',
            'job': 'testjob',
            'category': 2,
            'is_finished': True
            }
    resp = put(f'http://{HOST}:{PORT}/api/v2/jobs/15', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())
    

def TestJobDeleteNotExistJob():
    resp = delete(f'http://{HOST}:{PORT}/api/v2/jobs/18')
    print('url:', resp.url, '\njson-body:', '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())


def GetAllJobs():
    resp = get(f'http://{HOST}:{PORT}/api/v2/jobs')
    print('url:', resp.url, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())


def GetOneJob():
    resp = get(f'http://{HOST}:{PORT}/api/v2/jobs/1')
    print('url:', resp.url, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())


def AddDeleteJob():
    data = {
            'team_leader': 2,
            'work_size': 15,
            'collaborators': '1, 3, 4',
            'job': 'testjob',
            'category': 1,
            'is_finished': True
            }
    resp = post(f'http://{HOST}:{PORT}/api/v2/jobs', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())
    
    print()
    print('Проверим')
    pprint(get(f'http://{HOST}:{PORT}/api/v2/jobs/{resp.json()["id"]}').json())
    print()
    
    print('Удалим')
    pprint(delete(f'http://{HOST}:{PORT}/api/v2/jobs/{resp.json()["id"]}').json())
    

def AddEditJob():
    print('Создадим работу')
    data = {
            'team_leader': 2,
            'work_size': 15,
            'collaborators': '1, 3, 4',
            'job': 'testjob',
            'category': 1,
            'is_finished': True
            }
    resp = post(f'http://{HOST}:{PORT}/api/v2/jobs', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())
    
    print()
    print('Проверим')
    pprint(get(f'http://{HOST}:{PORT}/api/v2/jobs/{resp.json()["id"]}').json())
    print()
    
    print('Изменим')
    data = {
            'team_leader': 2,
            'work_size': 15,
            'collaborators': '1, 3, 4',
            'job': 'Editedtestjob',
            'category': 2,
            'is_finished': True
            }
    resp = put(f'http://{HOST}:{PORT}/api/v2/jobs/{resp.json()["id"]}', json=data)
    print('url:', resp.url, '\njson-body:', data, '\nstatus-code:', resp.status_code,
          '\nmethod:', resp.request.method, '\nresponse| ', end='')
    pprint(resp.json())
    print()
    
    print()
    print('Проверим')
    pprint(get(f'http://{HOST}:{PORT}/api/v2/jobs/{resp.json()["id"]}').json())
    print()
    
    print('Удалим')
    pprint(delete(f'http://{HOST}:{PORT}/api/v2/jobs/{resp.json()["id"]}').json())
    
    
if __name__ == '__main__':
    option = {0: ['Пустой запрос на добавление работы',
                  TestJobAddEmtpy],
              1: ['Запрос на добавление работы с неполным json',
                  TestJobAddNotEnoughJson],
              2: ['Запрос на добавление работы с некорректным значением (work_size)',
                  TestJobAddWithValueError],
              3: ['Запрос на добавление работы с несуществующим тим лидом',
                  TestJobAddWithNotExistUsers1],
              4: ['Запрос на добавления работы с несуществующим составом коллабораторов',
                  TestJobAddWithNotExistUsers2],
              5: ['Запрос на добавления работы с несуществующей категорией',
                  TestJobAddWithNotExistCategory],
              6: ['Пустой запрос на изменение работы',
                  TestJobEditEmtpy],
              7: ['Запрос на изменение несуществующей работы',
                  TestJobEditNotExistJob],
              8: ['Запрос на удаление несуществующей работы',
                  TestJobDeleteNotExistJob],
              9: ['Запрос на получение всех работ',
                  GetAllJobs],
              10: ['Запрос на получение одной работы',
                   GetOneJob],
              11: ['Запрос на добавление удаление работы',
                   AddDeleteJob],
              12: ['Запрос на добавление и изменение, в последующем и удаление работы',
                   AddEditJob]}
    choice = -2
    print('-1 - выход из программы')
    while choice != -1:
        print('Выберете тест введя соответствующую цифру')
        for k, v in option.items():
            print(f'[{k}] -', v[0])
        try:
            choice = int(input('Выбор| '))
        except ValueError:
            continue
        print()
        if test := option.get(choice, False):
            test[1]()
        else:
            continue
        print()
    print('Пока-пока')