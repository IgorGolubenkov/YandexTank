# coding=utf-8
import requests
import logging
import time
from Queue import Queue
import json
import random
import os
requests.packages.urllib3.disable_warnings()

from contextlib import contextmanager
from collections import namedtuple

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

test_case = {}
test_case['url'] = 'http://sandbox.cognita.ru/api/v2/' # для продакшен 'https://lecta/api/v2/' тестовый 'http://sandbox.cognita.ru/api/v2/'
test_case['url_id'] = 'http://id.sandbox.cognita.ru/api/' # для продакшен 'https://id.lecta/api/v2/' тестовый 'http://id.sandbox.cognita.ru/api/v2/'
test_case['url_ds'] = 'http://ds.sandbox.cognita.ru/api/' # для продакшен 'https://ds.lecta/api/v2/' тестовый 'http://ds.sandbox.cognita.ru/api/v2/'
test_case['login'] = 'peredacha100@extremail.ru'
test_case['new_aut_headers'] = {
            'Accept': 'application/json',
            'Content-Type': 'application/vnd.api+json'
        }
test_case['new_headers'] = {
            'Accept': 'application/json'
        }
test_case['reader_headers'] = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
#test_case['name_book'] = u'Математика № 1'

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


def get_client_book(login):
    """ получение портфеля пользователя """
    headers = test_case['new_headers']
    headers['Authorization'] = 'bearer ' + get_new_token(login)
    url_book = '%sclient/books' % test_case['url']
    answ = requests.get(url=url_book, headers=headers, verify=False)
    return answ.json()

#print len(get_client_book(test_case['login']))
# получаем длину портфеля


def get_url_token_book(login, book_name):
    """ получаем массив данных книги по названию книги
    data_book = {}
    key 'url' - valuye url открытие книги
    key 'token' - value токен доступности книги
    """
    data_book = {}
    for book in get_client_book(login):
        if book['title'] == book_name:
            book_reader = book['reader']
            data_book['token'] = book_reader['token']
            data_book['url'] = book_reader['url']
            break
    return data_book

def get_url_token_book_randomindex(login):
    """ получаем массив данных книги рандомно выбирается книга
    data_book = {}
    key 'url' - value url открытие книги
    key 'token' - value токен доступности книги
    key 'title' - value название книги
    """
    data_book = {}
    array_book = get_client_book(login)
    index_book = random.randrange(len(array_book))
    index_array = -1
    for book in get_client_book(login):
        index_array += 1
        if index_book == index_array:
            book_reader = book['reader']
            data_book['token'] = book_reader['token']
            data_book['url'] = book_reader['url']
            data_book['title'] = book['title']
            break
    return data_book

#print get_url_token_book_randomindex(test_case['login'])
#print get_url_token_book(test_case['login'], book_name=u'Математика № 1')
# проверка получения списка данных для открытия книги в ридере


import urllib
import urllib2

urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor))


#def open_book(login, book_name):
#    """ переход по url
#    осуществляется редирект на страницу книги
#    """
#    book_data_array = get_id_url_token_book(login, book_name)
#    params = urllib.urlencode({
#            'token' : book_data_array['token'],
#            'password': "1"
#            })
#    return urllib2.urlopen(book_data_array['url'], params)

#from bs4 import BeautifulSoup
#
#def parsing_html():
#    """ парсим html и возвращаем тэг title"""
#    boo = open_book(test_case['login'], book_name=u'Математика № 1').read()
#    boo_2 = BeautifulSoup(boo, "lxml")
#    return boo_2.title


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



def open_book_reader(login, *args, **kwargs):
    try:
        book_data_array = get_url_token_book_randomindex(login)
        params = urllib.urlencode({
            'token': book_data_array['token']
        })
        obj_open_book = urllib2.urlopen(book_data_array['url'], params)
        status_open_book = obj_open_book.code
        if status_open_book != 200:
            print obj_open_book
            logger.error('WARNING NOT OPEN BOOK: %s, STATUS: %s' % (book_data_array['title'], status_open_book))
            raise HttpCode(status_open_book)
        logger.debug('OPEN BOOK: %s, STATUS: %s' % (book_data_array['title'], status_open_book))
    except RuntimeError as e:
        logger.Error('Сценарий провалился с %s' % e)


def shoot_one(missile, marker, results):
    for login in test_case['login_array']:
        try:
            test_case['OpenBook'] = "1"
            with measure("openbook", results):
                open_book_reader(login)
        except RuntimeError as e:
            logger.Error('Следующий сценарий %s провалился с %s', marker, e)


if __name__ == '__main__':
    shoot_one("", "", Queue())


SCENARIOS = {
    "shoot_one": shoot_one
}
