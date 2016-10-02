
# coding=utf-8
import requests
import logging
import time
from Queue import Queue
import json
import os
import datetime
from requests_toolbelt import MultipartEncoder
requests.packages.urllib3.disable_warnings()

from contextlib import contextmanager
from collections import namedtuple


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


test_case = {}
test_case['url_sand'] = 'http://sandbox.cognita.ru/api/v2/'
test_case['new_headers'] = {
            'Accept': 'application/json',
            'Content-Type': 'application/vnd.api+json'
        }

#userID_array = [
#    '578cc10808ebbb66dcb748dc', '578cc10a08ebbb66dcb748e3', '578cc10d08ebbb66e1b7485a', '578cc10f08ebbb66e8b747fc', '578cc11108ebbb66e1b74861',
#    '578cc11408ebbb66e8b74803', '578cc11608ebbb66e8b7480a', '578cc11808ebbb66e8b74811', '578cc11b08ebbb66e8b74818', '578cc11d08ebbb66e8b7481f',
#    '578cc11f08ebbb66e8b74826', '578cc12208ebbb66e8b7482d', '578cc12408ebbb66e8b74834', '578cc12708ebbb66e5b7491b', '578cc12908ebbb66e1b74868',
#    '578cc12b08ebbb66e1b7486f', '578cc12e08ebbb66dcb748ea', '578cc13008ebbb66e1b74876', '578cc13208ebbb66dcb748f1', '578cc13508ebbb66e8b7483b',
#    '578cc13708ebbb66e8b74842', '578cc13908ebbb66e8b74849', '578cc13c08ebbb66e8b74850', '578cc13e08ebbb66e8b74857', '578cc14008ebbb66e8b7485e',
#    '578cc14308ebbb66dcb748f8', '578cc14508ebbb66dcb748ff', '578cc14708ebbb66dcb74906', '578cc14a08ebbb66e8b74865', '578cc14c08ebbb66dfb747e0',
#    '578cc14f08ebbb66dfb747e7', '578cc15108ebbb66dfb747ee', '578cc15308ebbb66dfb747f5', '578cc15608ebbb66dfb747fc', '578cc15808ebbb66dfb74803',
#    '578cc15a08ebbb66dfb7480a', '578cc15d08ebbb66dfb74811', '578cc15f08ebbb66e1b7487d', '578cc16108ebbb66e1b74884', '578cc16408ebbb66e1b7488b',
#    '578cc16608ebbb66e1b74892', '578cc16808ebbb66e1b74899', '578cc16b08ebbb66e1b748a0', '578cc16d08ebbb66e1b748a7', '578cc17008ebbb66e1b748ae',
#    '578cc17208ebbb66e1b748b5', '578cc17408ebbb66e1b748bc', '578cc17708ebbb66e1b748c3', '578cc17908ebbb66e1b748ca', '578cc17b08ebbb66e1b748d1',
#    '578cc17e08ebbb66e1b748d8', '578cc18008ebbb66e1b748df', '578cc18208ebbb66e1b748e6', '578cc18508ebbb66e1b748ed', '578cc18708ebbb66e1b748f4',
#    '578cc18908ebbb66e1b748fb', '578cc18c08ebbb66dcb7490d', '578cc18e08ebbb66dcb74914', '578cc19008ebbb66dfb74818', '578cc19308ebbb66dfb7481f',
#    '578cc19508ebbb66dfb74826', '578cc19708ebbb66dfb7482d', '578cc19a08ebbb66dfb74834', '578cc19c08ebbb66dfb7483b', '578cc19e08ebbb66dfb74842',
#    '578cc1a108ebbb66e1b74902', '578cc1a308ebbb66dfb74849', '578cc1a608ebbb66e5b74922', '578cc1a808ebbb66e5b74929', '578cc1aa08ebbb66e5b74930',
#    '578cc1ad08ebbb66e5b74937', '578cc1af08ebbb66e5b7493e', '578cc1b108ebbb66e5b74945', '578cc1b408ebbb66e5b7494c', '578cc1b608ebbb66e5b74953',
#    '578cc1b808ebbb66e5b7495a', '578cc1bb08ebbb66e5b74961', '578cc1bd08ebbb66e5b74968', '578cc1bf08ebbb66e5b7496f', '578cc1c208ebbb66e5b74976',
#    '578cc1c408ebbb66e5b7497d', '578cc1c708ebbb66e5b74984', '578cc1c908ebbb66e5b7498b', '578cc1cb08ebbb66e8b7486c', '578cc1ce08ebbb66dcb7491b',
#    '578cc1d008ebbb66e8b74873', '578cc1d208ebbb66dcb74922', '578cc1d508ebbb66dfb74850', '578cc1d708ebbb66dfb74857', '578cc1d908ebbb66dfb7485e',
#    '578cc1dc08ebbb66dfb74865', '578cc1de08ebbb66e8b7487a', '578cc1e008ebbb66e8b74881', '578cc1e308ebbb66e5b74992', '578cc1e508ebbb66dfb7486c',
#    '578cc1e708ebbb66dfb74873', '578cc1ea08ebbb66dfb7487a', '578cc1ec08ebbb66dfb74881', '578cc1ee08ebbb66e5b74999', '578cc1f108ebbb66e5b749a0']


name_file = "peredacha"
path_to_file_login = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Data/%s.txt" % name_file)
UserLogin_array = []
for user_login_1 in open(path_to_file_login, "r").readlines():
    user_login_2 = user_login_1.rstrip('\n')
    UserLogin_array.append(user_login_2)


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




def autorization(login, *args, **kwargs):
    """ метод новой авторизации"""
    try:
        req = '%susers/login' % test_case['url_sand']
        payload = {"login": login,"password": "12345678"}
        logger.debug('Ручка: %s' % (req))
        answ = requests.post(url=req, data=json.dumps(payload), headers=test_case['new_headers'], verify=False)
        if answ.status_code != 201:
            logger.error('НЕ АВТОРИЗОВАН пользователь: %s , Ответ от сервера: %s' % (payload, answ.json()))
            raise HttpCode(answ.status_code)
        logger.debug('АВТОРИЗОВАН, пользователь: %s, ответ от сервера %s' % (payload, answ.json()))
    except RuntimeError as e:
        logger.Error('Сценарий провалился с %s' % e)


def shoot_one(missile, marker, results):
    for login in UserLogin_array:
        try:
            test_case['Authorization'] = "1"
            with measure("authorization", results):
                autorization(login, test_case)
        except RuntimeError as e:
            logger.Error('Следующий сценарий %s провалился с %s', marker, e)


if __name__ == '__main__':
    shoot_one("", "", Queue())


SCENARIOS = {
    "shoot_one": shoot_one
}