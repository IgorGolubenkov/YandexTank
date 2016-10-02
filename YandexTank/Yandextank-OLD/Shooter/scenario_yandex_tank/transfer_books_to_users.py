
# coding=utf-8
import requests
import logging
import time
from Queue import Queue
import json
import datetime
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
test_case['login'] = 'nekasakome@divismail.ru'
test_case['old_headers'] = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
test_case['new_headers'] = {
            'Accept': 'application/json',
            'Content-Type': 'application/vnd.api+json'
        }
test_case['users_array'] = [
    '578cc10808ebbb66dcb748dc', '578cc10a08ebbb66dcb748e3', '578cc10d08ebbb66e1b7485a', '578cc10f08ebbb66e8b747fc', '578cc11108ebbb66e1b74861',
    '578cc11408ebbb66e8b74803', '578cc11608ebbb66e8b7480a', '578cc11808ebbb66e8b74811', '578cc11b08ebbb66e8b74818', '578cc11d08ebbb66e8b7481f',
    '578cc11f08ebbb66e8b74826', '578cc12208ebbb66e8b7482d', '578cc12408ebbb66e8b74834', '578cc12708ebbb66e5b7491b', '578cc12908ebbb66e1b74868',
    '578cc12b08ebbb66e1b7486f', '578cc12e08ebbb66dcb748ea', '578cc13008ebbb66e1b74876', '578cc13208ebbb66dcb748f1', '578cc13508ebbb66e8b7483b',
    '578cc13708ebbb66e8b74842', '578cc13908ebbb66e8b74849', '578cc13c08ebbb66e8b74850', '578cc13e08ebbb66e8b74857', '578cc14008ebbb66e8b7485e',
    '578cc14308ebbb66dcb748f8', '578cc14508ebbb66dcb748ff', '578cc14708ebbb66dcb74906', '578cc14a08ebbb66e8b74865', '578cc14c08ebbb66dfb747e0',
    '578cc14f08ebbb66dfb747e7', '578cc15108ebbb66dfb747ee', '578cc15308ebbb66dfb747f5', '578cc15608ebbb66dfb747fc', '578cc15808ebbb66dfb74803',
    '578cc15a08ebbb66dfb7480a', '578cc15d08ebbb66dfb74811', '578cc15f08ebbb66e1b7487d', '578cc16108ebbb66e1b74884', '578cc16408ebbb66e1b7488b',
    '578cc16608ebbb66e1b74892', '578cc16808ebbb66e1b74899', '578cc16b08ebbb66e1b748a0', '578cc16d08ebbb66e1b748a7', '578cc17008ebbb66e1b748ae',
    '578cc17208ebbb66e1b748b5', '578cc17408ebbb66e1b748bc', '578cc17708ebbb66e1b748c3', '578cc17908ebbb66e1b748ca', '578cc17b08ebbb66e1b748d1',
    '578cc17e08ebbb66e1b748d8', '578cc18008ebbb66e1b748df', '578cc18208ebbb66e1b748e6', '578cc18508ebbb66e1b748ed', '578cc18708ebbb66e1b748f4',
    '578cc18908ebbb66e1b748fb', '578cc18c08ebbb66dcb7490d', '578cc18e08ebbb66dcb74914', '578cc19008ebbb66dfb74818', '578cc19308ebbb66dfb7481f',
    '578cc19508ebbb66dfb74826', '578cc19708ebbb66dfb7482d', '578cc19a08ebbb66dfb74834', '578cc19c08ebbb66dfb7483b', '578cc19e08ebbb66dfb74842',
    '578cc1a108ebbb66e1b74902', '578cc1a308ebbb66dfb74849', '578cc1a608ebbb66e5b74922', '578cc1a808ebbb66e5b74929', '578cc1aa08ebbb66e5b74930',
    '578cc1ad08ebbb66e5b74937', '578cc1af08ebbb66e5b7493e', '578cc1b108ebbb66e5b74945', '578cc1b408ebbb66e5b7494c', '578cc1b608ebbb66e5b74953',
    '578cc1b808ebbb66e5b7495a', '578cc1bb08ebbb66e5b74961', '578cc1bd08ebbb66e5b74968', '578cc1bf08ebbb66e5b7496f', '578cc1c208ebbb66e5b74976',
    '578cc1c408ebbb66e5b7497d', '578cc1c708ebbb66e5b74984', '578cc1c908ebbb66e5b7498b', '578cc1cb08ebbb66e8b7486c', '578cc1ce08ebbb66dcb7491b',
    '578cc1d008ebbb66e8b74873', '578cc1d208ebbb66dcb74922', '578cc1d508ebbb66dfb74850', '578cc1d708ebbb66dfb74857', '578cc1d908ebbb66dfb7485e',
    '578cc1dc08ebbb66dfb74865', '578cc1de08ebbb66e8b7487a', '578cc1e008ebbb66e8b74881', '578cc1e308ebbb66e5b74992', '578cc1e508ebbb66dfb7486c',
    '578cc1e708ebbb66dfb74873', '578cc1ea08ebbb66dfb7487a', '578cc1ec08ebbb66dfb74881', '578cc1ee08ebbb66e5b74999', '578cc1f108ebbb66e5b749a0']
test_case['library_array'] = ['57a0714836fd0c6f44f98395', '57a0714936fd0c6f44f99723', '57a0714b36fd0c6f44f9aab1', '57a0714c36fd0c6f44f9be3f']
test_case['catalog_array'] = ['578c78c636fd0c6f44f7bdce', '578c790936fd0c6f44f7bdd2', '578c793836fd0c6f44f7bdd6', '578c796e36fd0c6f44f7bdda', '578c79a436fd0c6f44f7bdde']


def get_new_token(login):
    """ возвращает токен полученный новой ручкой """
    url_login = '%susers/login' % test_case['url']
    payload = {"login": login, "password": "12345678"}
    answ = requests.post(url=url_login, data=json.dumps(payload), headers=test_case['new_headers'], verify=False)
    return answ.json()['access_token']

def get_userme_account(login):
    """ возвращает загаловки с добавленным токеном
    и аккаунтом авторизованного пользователя
    """
    token = get_new_token(login)
    headers = test_case['old_headers']
    headers['X-Access-Token'] = token
    url_userme = '%susers/me/accounts' % test_case['url_id']
    answ = requests.get(url=url_userme, headers=headers, verify=False)
    preparation_x_account = answ.json()[0]
    headers['X-Account'] = preparation_x_account['id']
    return headers


test_case['aut_headers'] = get_userme_account(test_case['login'])
print test_case['aut_headers']

def get_mili_unixtime(year, mon=12, day=31, hour=23, min=59, sec=59):
    """ Получаем unix время в милисекундах
    обязательный аргемент год
    остально автоматически подставляется, последняя секунда года"""
    time_unix = datetime.datetime(year, mon, day, hour, min, sec)
    time_unix_second = time.mktime(time_unix.timetuple())
    return int(round(time_unix_second * 1000))

test_case['expiration_date'] = get_mili_unixtime(2016, 10, 1)

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



def transfer_books_to_users(user, library_index, catalog, *args, **kwargs):
    try:
        req = '%scopies/createLeasesForUsers' % test_case['url_ds']
        body = {
            "copyParams": [{"catalog": catalog, "expirationDate": None}],
            "expirationDate": test_case['expiration_date'],
            "fromLibrary": test_case['library_array'][library_index],
            "users": [user]
        }
        answ = requests.post(url=req, headers=test_case['aut_headers'], json=body, verify=False)
        status_resp = answ.status_code
        if status_resp != 201:
            logger.error('позиция каталога: %s НЕ ПЕРЕДАНА пользователю: %s , Статус передачи: %s' % (catalog, user, status_resp))
            raise HttpCode(status_resp)
        logger.debug('пользователю: %s ПЕРЕДАНО: %s, Статус передачи %s' % (user, catalog, status_resp))
    except RuntimeError as e:
        logger.Error('Сценарий провалился с %s' % e)


def shoot_one(missile, marker, results):
    index = -1
    for user in test_case['users_array']:
        index += 1
        library_index = index // 25
        for catalogID in test_case['catalog_array']:
            try:
                test_case['Autorization'] = "1"
                with measure("autorization", results):
                    transfer_books_to_users(user, library_index, catalogID)
            except RuntimeError as e:
                logger.Error('Следующий сценарий %s провалился с %s', marker, e)


if __name__ == '__main__':
    shoot_one("", "", Queue())


SCENARIOS = {
    "shoot_one": shoot_one
}
