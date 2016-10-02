# -*- coding: utf-8 -*-

import logging
import json
import os
import requests
log = logging.getLogger(__name__)

requests.packages.urllib3.disable_warnings()

test_case = {}
test_case['url'] = 'http://sandbox.cognita.ru/api/v2/'  # для продакшен 'https://lecta/api/v2/' тестовый 'http://sandbox.cognita.ru/api/v2/'
test_case['new_aut_headers'] = {
            'Accept': 'application/json',
            'Content-Type': 'application/vnd.api+json'
        }
test_case['new_headers'] = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
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
    return requests.post(url=url_login, data=json.dumps(payload), headers=test_case['new_aut_headers'], verify=False)
    #answ = requests.post(url=url_login, data=json.dumps(payload), headers=test_case['new_aut_headers'], verify=False)
    #resp_json = answ.json()
    #return resp_json['access_token']


class LoadTest(object):

    def __init__(self, gun):

        # you'll be able to call gun's methods using this field:
        self.gun = gun

        # for example, you can get something from the 'ultimate' section of a config file:
        my_var = self.gun.get_option("my_var", "hello")

    def get_book(self, missile):
        index = 0
        login_list = test_case['login_array']
        log.info("Get login list: %s" % login_list)
        for login in login_list:
            index += 1
            with self.gun.measure("get_book_user:%s" % index) as sample:
                log.info("Shoot get_book user: %s", missile)
                try:
                    headers = test_case['new_headers']
                    req_obj = get_new_token(login)
                    req_json = req_obj.json()
                    req_status_code = req_obj.status_code
                    log.debug("REQUEST INFO: STATUS-CODE: %s, JSON: %s" % (req_status_code, req_json))
                    headers['Authorization'] = 'Bearer ' + req_json['access_token']
                    url_book = '%sclient/books' % test_case['url']
                    answ = requests.get(url=url_book, headers=headers, verify=False)
                    resp = answ.json()
                    len_book = len(resp)
                    if answ.status_code != 200:
                        log.error('У пользователя: %s, портфель НЕ ПОЛУЧЕН! Ответ от сервера: %s' % (login, resp))
                    log.debug('ПОЛУЧЕН портфель из: %s книг, У пользователя: %s' % (len_book, login))
                except RuntimeError as e:
                    # set your exit code
                    sample['proto_code'] = 500
                finally:
                    "< ...some finishing work... >"

    def setup(self, param):
        ''' this will be executed in each worker before the test starts '''
        log.info("Setting up LoadTest: %s", param)

    def teardown(self):
        ''' this will be executed in each worker after the end of the test '''
        log.info("Tearing down LoadTest")