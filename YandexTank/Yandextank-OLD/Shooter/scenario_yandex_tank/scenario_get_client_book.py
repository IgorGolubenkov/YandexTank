# coding=utf-8

import requests
import logging
from Queue import Queue
import json
import random
import os
import time
requests.packages.urllib3.disable_warnings()

from contextlib import contextmanager
from collections import namedtuple

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


test_case = {}
test_case['url'] = 'http://sandbox.cognita.ru/api/v2/' # для продакшен 'https://lecta/api/v2/' тестовый 'http://sandbox.cognita.ru/api/v2/'
test_case['new_aut_headers'] = {
            'Accept': 'application/json',
            'Content-Type': 'application/vnd.api+json'
        }
test_case['new_headers'] = {
            'Accept': 'application/json'
        }

def read_file(name_file):
    """
    :param name_file: имя файла
    :return: список из логинов
    """
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.txt" % name_file)
    list_logins = []
    for login in open(file_path, "r").readlines():
        username = login.rstrip('\n')
        list_logins.append(username)
        #print(username)
    return list_logins


test_case['name_file'] = '1_login'                              # имя файла с логинами
test_case['login_array'] = read_file(test_case['name_file'])


def get_new_token(login):
    """ возвращает токен полученный новой ручкой """
    url_login = '%susers/login' % test_case['url']
    payload = {"login": login, "password": "12345678"}
    answ = requests.post(url=url_login, data=json.dumps(payload), headers=test_case['new_aut_headers'], verify=False)
    return answ.json()['access_token']

#def get_client_book(login):
#    """ получение портфеля пользователя """
#    headers = test_case['new_headers']
#    headers['Authorization'] = 'Bearer ' + get_new_token(login)
#    url_book = '%sclient/books' % test_case['url']
#    answ = requests.get(url=url_book, headers=headers, verify=False)
#    return answ.json()
#
#for login in test_case['login_array']:
#    print len(get_client_book(login))
# проверка получения портфеля



Sample = namedtuple(
        'Sample', 'marker,threads,overallRT,httpCode,netCode,sent,received,connect,send,latency,receive,accuracy')

@contextmanager
def measure(marker, queue):
    start_ms = time.time()

    resp_code = 0
    http_code = 200
    try:
        yield
    except HttpCode as exc:
        logging.info("%s for request: %s" % (exc.value, marker))
        http_code = exc.value
    except Exception as e:
        logging.info("error while yield: marker:%s, e:%s" % (marker, e))
        # print 'error while yield', marker, e
        http_code = 600

    response_time = int((time.time() - start_ms) * 1000)

    data_item = Sample(
            marker,  # маркер
            1,  # число активных потоков
            response_time,  # время отклика (основная метрика)
            http_code,  # код ошибки прикладного уровня
            resp_code,  # код ошибки сетевого уровня
            0,  # отправлено байт
            0,  # принято байт
            response_time,  # время соединения
            0,  # время отправки
            response_time,  # время от завершения отправки до начала приема
            0,  # время приема
            0,  # точность
    )
    queue.put((int(time.time()), data_item), timeout=5)


class HttpCode(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)



def get_client_book(login, *args, **kwargs):
    try:
        headers = test_case['new_headers']
        headers['Authorization'] = 'Bearer ' + get_new_token(login)
        url_book = '%sclient/books' % test_case['url']
        answ = requests.get(url=url_book, headers=headers, verify=False)
        resp = answ.json()
        len_book =  len(resp)
        if answ.status_code != 200:
            logger.error('У пользователя: %s, портфель НЕ ПОЛУЧЕН! Ответ от сервера: %s' % (login, resp))
            raise HttpCode(answ.status_code)
        logger.debug('ПОЛУЧЕН портфель из: %s книг, У пользователя: %s' % (len_book, login))
    except RuntimeError as e:
        logger.Error('Сценарий провалился с %s' % e)


def shoot_one(missile, marker, results):
    for login in test_case['login_array']:
        try:
            test_case['GetClientBook'] = "1"
            with measure("getclientbook", results):
                get_client_book(login)
        except RuntimeError as e:
            logger.Error('Следующий сценарий %s провалился с %s', marker, e)


if __name__ == '__main__':
    shoot_one("", "", Queue())


SCENARIOS = {
    "shoot_one": shoot_one
}
