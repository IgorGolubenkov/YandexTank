# coding=utf-8
import json
import requests
import logging
import time
from Queue import Queue
import json
import random
import pickle
import traceback
from requests_toolbelt import MultipartEncoder
requests.packages.urllib3.disable_warnings()

from contextlib import contextmanager
from collections import namedtuple

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

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


def get_1(*args, **kwargs):
    try:
        req = '%s/api/auth/local' % test_case['url']
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-us,en;q=0.8",
            "Content-Type": "application/json;charset=UTF-8"}
        payload = {"login": "golubenkov_test@mail.ru","password": "321666"}
        logger.debug('Attempt a post request: %s, payload: %s' % (req, payload))
        answ = requests.post(url=req, data=json.dumps(payload), headers=headers)
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Payload: %s , Response: %s' % (req, payload, answ.json()))
            raise HttpCode(answ.status_code)
        logger.debug('Response get SessionID: %s' % answ.json())
        return answ.json()['sessionId']
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)



def get_2(*args, **kwargs):
    try:
        req = '%s/api/oauth/code' % test_case['url']
        session_id = test_results['result1']
        headers_auth = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-us,en;q=0.8",
            "Content-Type": "application/json;charset=UTF-8",
            "X-Session-Id": session_id,
            }
        payload = {"clientId":0, "credentials": {"id": ["main","accounts","groups"]}}
        logger.debug('Attempt a post request oauth: %s, payload: %s' % (req, payload))
        answ = requests.post(url=req, data=json.dumps(payload), headers=headers_auth)
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Payload: %s , Response: %s' % (req, payload, answ.json()))
            raise HttpCode(answ.status_code)
        logger.debug('Response get Code: %s' % answ.json())
        return answ.json()['code']
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)



def get_3(*args, **kwargs):
    try:
        req = '%s/api/oauth/token' % test_case['url']
        ses_code = test_results['result2']
        session_id = test_results['result1']
        headers_auth = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-us,en;q=0.8",
            "Content-Type": "application/json;charset=UTF-8",
            "X-Session-Id": session_id,
            }
        payload = {
            "clientId": "0",
            "clientSecret": "@Mqb8Xh7m5N5~eW",
            "grantType": "code",
            "code": ses_code,
            "refreshToken": "null"}
        logger.debug('Attempt a post request: %s, payload: %s' % (req, payload))
        answ = requests.post(url=req, data=json.dumps(payload), headers=headers_auth)
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Payload: %s , Response: %s' % (req, payload, answ.json()))
            raise HttpCode(answ.status_code)
        logger.debug('Response get Token: %s' % answ.json())
        return answ.json()['token']
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)



# =================================
# SCENARIOS BELOW
# =================================


test_case = {}
test_case['url'] = "https://id.demo.cognita.ru"
test_case['url2'] = "https://ds.demo.cognita.ru"
test_case['url3'] = "https://storage.demo.cognita.ru"


test_results = {}


def scenario1(missile, marker, results):
    try:
        test_case['Access_Token'] = "1"
        with measure("get_sessionId", results):
            test_results['result1'] = get_1(test_case)
        with measure("get_code", results):
            test_results['result2'] = get_2(test_case, test_results)
        with measure("get_token", results):
            test_results['result3'] = get_3(test_case, test_results)
    except RuntimeError as e:
        logger.Error('Scenario %s failed with %s', marker, e)



# =====================

if __name__ == '__main__':
    scenario1("", "", Queue())


SCENARIOS = {
    "scenario1": scenario1
}