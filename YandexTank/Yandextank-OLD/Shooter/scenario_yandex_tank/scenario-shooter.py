# coding=utf-8
import requests
import logging
import time
import json
from Queue import Queue
import pickle

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
        logging.info("error while yield: %s %s" % (marker, e))
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


def get_sessionID(*args, **kwargs):
    try:
        req = '%s/api/auth/local' % test_case['url']
        headers_auth = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-us,en;q=0.8",
            "Content-Type": "application/json;charset=UTF-8"}
        payload = {"login": "golubenkov_test@mail.ru","password": "321666"}
        logger.debug('Attempt a post request: %s, payload: %s' % (req, payload))
        answ = requests.post(url=req, data=json.dumps(payload), headers=headers_auth)
        logger.debug('Response: %s' % answ.json())
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Payload: %s , Response: %s' % (req, payload, answ.json()))
            raise HttpCode(answ.status_code)
        return answ.json()['sessionId']
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)


def get_sessionCODE(*args, **kwargs):
    try:
        req = '%s/api/oauth/code' % test_case['url']
        session_id = test_results['result1']
        headers_oauth = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-us,en;q=0.8",
            "Content-Type": "application/json;charset=UTF-8",
            "X-Session-Id": session_id,
            }
        payload = {"clientId":0, "credentials": {"id": ["main","accounts","groups"]}}
        logger.debug('Attempt a post request oauth: %s, payload: %s' % (req, payload))
        answ = requests.post(url=req, data=json.dumps(payload), headers=headers_oauth)
        logger.debug('Response: %s' % answ.json())
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Payload: %s , Response: %s' % (req, payload, answ.json()))
            raise HttpCode(answ.status_code)
        return answ.json()['code']
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)


def get_sessionTOKEN(*args, **kwargs):
    try:
        req = '%s/api/oauth/token' % test_case['url']
        ses_code = test_results['result2']
        session_id = test_results['result1']
        headers_oauth = {
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
        answ = requests.post(url=req, data=json.dumps(payload), headers=headers_oauth)
        logger.debug('Response: %s' % answ.json())
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Payload: %s , Response: %s' % (req, payload, answ.json()))
            raise HttpCode(answ.status_code)
        return answ.json()['token']
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)


def get_X_account(*args, **kwargs):
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
        logger.debug('Response: %s' % answ.json())
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Response: %s' % (req, answ.json()))
            raise HttpCode(answ.status_code)
        preparation_x_account = answ.json()[0]
        return preparation_x_account['id']
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)


def get_code_afteraut(*args, **kwargs):
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
                "storage": ["mian"],
                "social": ["main"]
            }
        }
        logger.debug('Attempt a post request oauth: %s, payload: %s' % (req, payload))
        answ = requests.post(url=req, data=json.dumps(payload), headers=headers_oauth)
        logger.debug('Response: %s' % answ.json())
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Payload: %s , Response: %s' % (req, payload, answ.json()))
            raise HttpCode(answ.status_code)
        return answ.json()['code']
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)

def get_token_afteraut(*args, **kwargs):
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
        logger.debug('Response: %s' % answ.json())
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Payload: %s , Response: %s' % (req, payload, answ.json()))
            raise HttpCode(answ.status_code)
        return answ.json()['token']
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)


def get_serverToken(*args, **kwargs):
    try:
        req = '%s/api/oauth/serverToken' % test_case['url']
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
                "auth": {
                "login": "golubenkov_test@mail.ru",
                "password": "321666",
                "expiresIn": 157680000,
                "credentials": {
                "id": ["main", "accounts"],
                "market": ["main"]
                            }
                        }
                    }
        logger.debug('Attempt a post request: %s, payload: %s' % (req, payload))
        answ = requests.post(url=req, data=json.dumps(payload), headers=headers_oauth)
        logger.debug('Response: %s' % answ.json())
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Payload: %s , Response: %s' % (req, payload, answ.json()))
            raise HttpCode(answ.status_code)
        return answ.json()['token']
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)


def get_collection(*args, **kwargs):
    try:
        req = '%s/api/client/keys' % test_case['url2']
        session_token = test_results['result6']
        x_account = test_results['result4']
        headers_oauth = {
            "X-Access-Token": session_token,
            "X-Account": x_account,
            }
        logger.debug('Attempt a get request: %s' % (req))
        answ = requests.get(url=req, headers=headers_oauth)
        logger.debug('Response: %s' % answ.json())
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Response: %s' % (req, answ.json()))
            raise HttpCode(answ.status_code)
        return answ.json()
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)


def get_leases(*args, **kwargs):
    try:
        req = '%s/api/client/leases' % test_case['url2']
        extension_leases = {
            "extend": "catalog,keys"
        }
        session_token = test_results['result6']
        x_account = test_results['result4']
        headers_oauth = {
            "X-Access-Token": session_token,
            "X-Account": x_account,
            }
        logger.debug('Attempt a get request: %s' % (req))
        answ = requests.get(url=req, params=extension_leases, headers=headers_oauth)
        logger.debug('Response: %s' % answ.json())
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Response: %s' % (req, answ.json()))
            raise HttpCode(answ.status_code)
        return answ.json()
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)


def get_bundles(*args, **kwargs):
    try:
        req = '%s/api/bundles' % test_case['url2']
        session_token = test_results['result6']
        x_account = test_results['result4']
        headers_oauth = {
            "X-Access-Token": session_token,
            "X-Account": x_account,
            }
        logger.debug('Attempt a get request: %s' % (req))
        answ = requests.get(url=req, headers=headers_oauth)
        logger.debug('Response: %s' % answ.json())
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Response: %s' % (req, answ.json()))
            raise HttpCode(answ.status_code)
        return answ.json()
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)


def get_copies(*args, **kwargs):
    try:
        req = '%s/api/copies' % test_case['url2']
        session_token = test_results['result6']
        x_account = test_results['result4']
        headers_oauth = {
            "X-Access-Token": session_token,
            "X-Account": x_account,
            }
        logger.debug('Attempt a get request: %s' % (req))
        answ = requests.get(url=req, headers=headers_oauth)
        logger.debug('Response: %s' % answ.json())
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Response: %s' % (req, answ.json()))
            raise HttpCode(answ.status_code)
        return answ.json()
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)


def get_provider(*args, **kwargs):
    try:
        req = '%s/api/provider/users' % test_case['url1']
        session_token = test_results['result6']
        x_account = test_results['result4']
        headers_oauth = {
            "X-Access-Token": session_token,
            "X-Account": x_account,
            }
        logger.debug('Attempt a get request: %s' % (req))
        answ = requests.get(url=req, headers=headers_oauth)
        logger.debug('Response: %s' % answ.json())
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Response: %s' % (req, answ.json()))
            raise HttpCode(answ.status_code)
        return answ.json()
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)


def get_files(*args, **kwargs):
    try:
        req = '%s/api/files' % test_case['url3']
        session_token = test_results['result11']
        x_account = test_results['result4']
        headers_oauth = {
            "X-Access-Token": session_token,
            "X-Account": x_account,
            }
        logger.debug('Attempt a get request: %s' % (req))
        answ = requests.get(url=req, headers=headers_oauth)
        logger.debug('Response: %s' % answ.json())
        if answ.status_code != 200:
            logger.error('Not 200 answer code for Req: %s \n Response: %s' % (req, answ.json()))
            raise HttpCode(answ.status_code)
        return answ.json()
    except RuntimeError as e:
        logger.Error('Scenario failed with %s' % e)

# =================================
# SCENARIOS BELOW
# =================================


test_case = {}
test_case['url'] = "https://id.lecta.ru"
test_case['url2'] = "https://ds.lecta.ru"
test_case['url3'] = "https://storage.lecta.ru"

test_results = {}


def scenario1(missile, marker, results):
    try:
        test_case['Access_Token'] = "1"
        with measure("get_sessionId", results):
            test_results['result1'] = get_sessionID(test_case)
        with measure("get_code", results):
            test_results['result2'] = get_sessionCODE(test_case, test_results)
        with measure("get_token", results):
            test_results['result3'] = get_sessionTOKEN(test_case, test_results)
        with measure("get_X_account", results):
            test_results['result4'] = get_X_account(test_case, test_results)
        with measure("get_code_afteraut", results):
            test_results['result5'] = get_code_afteraut(test_case, test_results)
        with measure("get_token_afteraut", results):
            test_results['result6'] = get_token_afteraut(test_case, test_results)
    except RuntimeError as e:
        logger.Error('Scenario %s failed with %s', marker, e)



def scenario2(missile, marker, results):
    try:
        test_case['Working_app'] = "2"
        with measure("get_serverToken", results):
            test_results['result11'] = get_serverToken(test_case, test_results)
        with measure("get_collection", results):
            test_results['result7'] = get_collection(test_case, test_results)
        with measure("get_collection", results):
            test_results['result8'] = get_leases(test_case, test_results)
        with measure("get_bundles", results):
            test_results['result9'] = get_bundles(test_case, test_results)
        with measure("get_copies", results):
            test_results['result10'] = get_copies(test_case, test_results)
    except RuntimeError as e:
        logger.Error('Scenario %s failed with %s', marker, e)


def scenario3(missile, marker, results):
    try:
        test_case['Get_providerToken'] = "3"
        with measure("get_provider", results):
            test_results['result11'] = get_files(test_case, test_results)
            print test_results['result11']
    except RuntimeError as e:
        logger.Error('Scenario %s failed with %s', marker, e)


if __name__ == '__main__':
    scenario1("", "", Queue())
    scenario2("", "", Queue())
    scenario3("", "", Queue())


SCENARIOS = {
    "scenario1": scenario1,
    "scenario2": scenario2,
    "scenario3": scenario3
}

