
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


def get_4(*args, **kwargs):
    try:
        req = '%s/api/users/me/accounts' % test_case['url']
        session_id = test_results['result1']
        session_token = test_results['result3']
        headers_token = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-us,en;q=0.8",
            "Content-Type": "application/json;charset=UTF-8",
            "X-Session-Id": session_id,
            "X-Access-Token": session_token,
            }
        logger.debug('Attempt a get request: %s' % (req))
        answ = requests.get(url=req, headers=headers_token)
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Response: %s' % (req, answ.json()))
            raise HttpCode(answ.status_code)
        logger.debug('Response get account: %s' % answ.json())
        preparation_x_account = answ.json()[0]
        return preparation_x_account['id']
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)


def get_5(*args, **kwargs):
    try:
        req = '%s/api/oauth/code' % test_case['url']
        session_id = test_results['result1']
        session_token = test_results['result3']
        x_account = test_results['result4']
        headers_oauth = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-us,en;q=0.8",
            "Content-Type": "application/json;charset=UTF-8",
            "X-Session-Id": session_id,
            "X-Access-Token": session_token,
            "X-Account": x_account,
            }
        payload = {
        "clientId": "2",
        "credentials": {
                "id": ["main","accounts"],
                "distribution": ["main"],
                "storage": ["main"],
                "social": ["main"]
            }
        }
        logger.debug('Attempt a post request oauth: %s, payload: %s' % (req, payload))
        answ = requests.post(url=req, data=json.dumps(payload), headers=headers_oauth)
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Payload: %s , Response: %s' % (req, payload, answ.json()))
            raise HttpCode(answ.status_code)
        logger.debug('Response get AfterCode: %s' % answ.json())
        return answ.json()['code']
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)


def get_6(*args, **kwargs):
    try:
        req = '%s/api/oauth/token' % test_case['url']
        ses_code = test_results['result5']
        session_id = test_results['result1']
        session_token = test_results['result3']
        x_account = test_results['result4']
        headers_oauth = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-us,en;q=0.8",
            "Content-Type": "application/json;charset=UTF-8",
            "X-Session-Id": session_id,
            "X-Access-Token": session_token,
            "X-Account": x_account,
            }
        payload = {
                "clientId": "2",
                "clientSecret": "2o1XmaNlHm",
                "grantType": "code",
                "code": ses_code,
                "refreshToken": "null"
                    }
        logger.debug('Attempt a post request: %s, payload: %s' % (req, payload))
        answ = requests.post(url=req, data=json.dumps(payload), headers=headers_oauth)
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Payload: %s , Response: %s' % (req, payload, answ.json()))
            raise HttpCode(answ.status_code)
        logger.debug('Response get AfterToken: %s' % answ.json())
        return answ.json()['token']
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)


def get_7(*args, **kwargs):
    try:
        req = '%s/api/oauth/scopes/id' % test_case['url']
        session_id = test_results['result1']
        session_token = test_results['result3']
        x_account = test_results['result4']
        headers_oauth = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-us,en;q=0.8",
            "Content-Type": "application/json;charset=UTF-8",
            "X-Session-Id": session_id,
            "X-Access-Token": session_token,
            "X-Account": x_account,
            }
        logger.debug('Attempt a get request: %s' % (req))
        answ = requests.get(url=req, headers=headers_oauth)
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Response: %s' % (req, answ.json()))
            raise HttpCode(answ.status_code)
        logger.debug('Response get Scope: %s' % answ.json())
        return answ.json()
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)


def get_8(*args, **kwargs):
    try:
        req = '%s/api/client/keys' % test_case['url2']
        session_id = test_results['result1']
        session_token = test_results['result6']
        x_account = test_results['result4']
        headers_oauth = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-us,en;q=0.8",
            "Content-Type": "application/json;charset=UTF-8",
            "X-Session-Id": session_id,
            "X-Access-Token": session_token,
            "X-Account": x_account,
            }
        logger.debug('Attempt a get request: %s' % (req))
        answ = requests.get(url=req, headers=headers_oauth)
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Response: %s' % (req, answ.json()))
            raise HttpCode(answ.status_code)
        logger.debug('Response get Keys: %s' % answ.json())
        return answ.json()
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)


def get_9(*args, **kwargs):
    try:
        req = '%s/api/client/leases' % test_case['url2']
        extension_leases = {
            "extend": "catalog,keys"
        }
        session_id = test_results['result1']
        session_token = test_results['result6']
        x_account = test_results['result4']
        headers_oauth = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-us,en;q=0.8",
            "Content-Type": "application/json;charset=UTF-8",
            "X-Session-Id": session_id,
            "X-Access-Token": session_token,
            "X-Account": x_account,
            }
        logger.debug('Attempt a get request: %s' % (req))
        answ = requests.get(url=req, params=extension_leases, headers=headers_oauth)
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Response: %s' % (req, answ.json()))
            raise HttpCode(answ.status_code)
        logger.debug('Response get Leases: %s' % answ.json())
        return answ.json()
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)

def get_10(*args, **kwargs):
    try:
        req = '%s/api/files' % test_case['url3']
        session_token = test_results['result6']
        x_account = test_results['result4']
        headers_oauth = {
            "X-Access-Token": session_token,
            "X-Account": x_account,
        }
        logger.debug('Attempt a get request: %s' % (req))
        answ = requests.get(url=req, headers=headers_oauth)
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Response: %s' % (req, answ.json()))
            raise HttpCode(answ.status_code)
        logger.debug('Response get Files array: %s' % answ.json())
        index_files = random.randrange(len(answ.json()))
        resourceId_array = answ.json()[index_files]
        resourceId = resourceId_array['resourceId']
        #print resourceId
        return resourceId
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)


def get_11(*args, **kwargs):
    try:
        req = '%s/api/files/%s/data' % (test_case['url3'], test_results['result10'])
        session_token = test_results['result6']
        x_account = test_results['result4']
        headers_oauth = {
            "X-Access-Token": session_token,
            "X-Account": x_account,
        }
        logger.debug('Attempt a get request: %s' % (req))
        answ = requests.get(url=req, headers=headers_oauth)
        if answ.status_code != 200:
            logger.error('Not 301 answer code for Req: %s \n Response Headers: %s' % (req, answ.headers))
            raise HttpCode(answ.status_code)
        logger.debug('Response get URL files: %s' % answ.headers)
        return "OK"
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)

def get_12(*args, **kwargs):
    try:
        req = '%s/api/files' % test_case['url3']
        session_token = test_results['result6']
        x_account = test_results['result4']
        load_files_body = MultipartEncoder(
            fields={'meta': '{"name":"test_file.jpg","sharing":{"byLink":true}}',
                    'data': ('filename', open("//home/golubenkov/yatank_data/Shooter/test_file.jpg", "rb"), 'image/jpeg')})
        headers_files = {
            "Content-Type": load_files_body.content_type,
            "Content-Length": 83988,
            "X-Access-Token": session_token,
            "X-Account": x_account,
        }
        logger.debug('Attempt a get request: %s' % (req))
        answ = requests.post(url=req, data=load_files_body, headers=headers_files, verify=False)
        if answ.status_code != 201:
            logger.error('Not 201 answer code for Req: %s \n Response: %s' % (req, answ.json()))
            raise HttpCode(answ.status_code)
        logger.debug('Response Load Files: %s' % answ.json())
        return answ.json()['resourceId']
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)


def get_13(*args, **kwargs):
    try:
        req = '%s/api/files/%s/' % (test_case['url3'], test_results['result12'])
        session_token = test_results['result6']
        x_account = test_results['result4']
        headers_oauth = {
            "X-Access-Token": session_token,
            "X-Account": x_account,
        }
        logger.debug('Attempt a get request: %s' % (req))
        answ = requests.delete(url=req, headers=headers_oauth, verify=False)
        if answ.status_code != 204:
            logger.error('Not 204 answer code for Req: %s \n Response Headers: %s' % (req, answ.headers))
            raise HttpCode(answ.status_code)
        logger.debug('Response Remove files: %s' % answ.headers)
        return "OK"
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
        with measure("get_X_account", results):
            test_results['result4'] = get_4(test_case, test_results)
        with measure("get_after_code", results):
            test_results['result5'] = get_5(test_case, test_results)
        with measure("get_after_token", results):
            test_results['result6'] = get_6(test_case, test_results)
        with measure("load_files", results):
            test_results['result12'] = get_12(test_case, test_results)
        with measure("get_scope", results):
            test_results['result7'] = get_7(test_case, test_results)
        with measure("get_collection", results):
            test_results['result8'] = get_8(test_case, test_results)
        with measure("get_leases", results):
            test_results['result9'] = get_9(test_case, test_results)
        with measure("get_files", results):
            test_results['result10'] = get_10(test_case, test_results)
        with measure("url_files", results):
            test_results['result11'] = get_11(test_case, test_results)
        with measure("remove_files", results):
            test_results['result13'] = get_13(test_case, test_results)
    except RuntimeError as e:
        logger.Error('Scenario %s failed with %s', marker, e)



# =====================

if __name__ == '__main__':
    scenario1("", "", Queue())


SCENARIOS = {
    "scenario1": scenario1
}