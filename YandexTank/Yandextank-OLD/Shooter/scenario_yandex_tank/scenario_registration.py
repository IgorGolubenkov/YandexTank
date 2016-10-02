# -*- coding: utf-8 -*-


import logging
from Queue import Queue
import time
import requests
import random
import string
import sys, traceback


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
    traceback_template = '''Traceback (most recent call last):
      File "%(filename)s", line %(lineno)s, in %(name)s
    %(type)s: %(message)s\n'''
    try:
        yield
    except HttpCode as exc:
        logging.info("%s for request: %s" % (exc.value, marker))
        http_code = exc.value
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = {
            'filename': exc_traceback.tb_frame.f_code.co_filename,
            'lineno': exc_traceback.tb_lineno,
            'name': exc_traceback.tb_frame.f_code.co_name,
            'type': exc_type.__name__,
            'message': exc_value.message,
        }
        del (exc_type, exc_value, exc_traceback)
        print traceback.format_exc()
        print traceback_template % traceback_details
        logging.info("error while yield: marker:%s, e:%s" % (marker, e))
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


def random_string_name(len):
    """
    получаем строку, из строчных символов, согласно переданной длины
    """
    symbols = string.ascii_lowercase
    return ''.join([random.choice(symbols) for i in range(len)])

def random_number_phone():
    """
    получаем рандомный номер телефона в зоне +7
    """
    symbols = string.digits
    return "+79" + "".join([random.choice(symbols) for i in range(9)])

class ModelRegistration:
    def __init__(self, firstname=None, lastname=None, secondname=None,
                 email=None):
        self.firstname = firstname
        self.lastname = lastname
        self.secondname = secondname
        self.email = email

    def __repr__(self):
        return "%s + %s + %s + %s" % (self.firstname, self.lastname, self.secondname, self.email)

class Transliterator:

    def transliterate_cyrillic(self, name):
        """ Траслитерация с латиницы на кирилицу"""
        slovar = {'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'е', 'j': 'ж', 'z': 'з', 'i': 'и',
                  'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'r': 'р', 's': 'с', 't': 'т',
                  'u': 'у', 'f': 'ф', 'h': 'х', 'c': 'ц', 'y': 'й', 'q': 'кью', 'w': 'вэ', 'x': 'икс',
                  'A': 'А', 'B': 'Б', 'V': 'В', 'G': 'Г', 'D': 'Д', 'E': 'Е', 'J': 'Ж', 'Z': 'З', 'I': 'И',
                  'K': 'К', 'L': 'Л', 'M': 'М', 'N': 'Н', 'O': 'О', 'P': 'П', 'R': 'Р', 'S': 'С', 'T': 'Т',
                  'U': 'У', 'F': 'Ф', 'H': 'Х', 'C': 'Ц', 'Y': 'Й', 'Q': 'Кью', 'W': 'Вэ', 'X': 'Икс',
                  "'": 'ь'}
        for key in slovar:
            name = name.replace(key, slovar[key])
        return name

    def transliterate_latin(self, name):
        """ Траслитерация с кирилици на латиницу """
        slovar = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
                  'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
                  'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
                  'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
                  'ю': 'u', 'я': 'ja', 'А': 'a', 'Б': 'b', 'В': 'v', 'Г': 'g', 'Д': 'd', 'Е': 'e', 'Ё': 'e',
                  'Ж': 'zh', 'З': 'z', 'И': 'i', 'Й': 'i', 'К': 'k', 'Л': 'l', 'М': 'm', 'Н': 'n',
                  'О': 'o', 'П': 'p', 'Р': 'r', 'С': 's', 'Т': 't', 'У': 'u', 'Ф': 'f', 'Х': 'h',
                  'Ц': 'c', 'Ч': 'ch', 'Ш': 'sh', 'Щ': 'scz', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'e',
                  'Ю': 'u', 'Я': 'ja', ',': '', '?': '', ' ': '_', '~': '', '!': '', '@': '', '#': '',
                  '$': '', '%': '', '^': '', '&': '', '*': '', '(': '', ')': '', '-': '', '=': '', '+': '',
                  ':': '', ';': '', '<': '', '>': '', '\'': '', '"': '', '\\': '', '/': '', '№': '',
                  '[': '', ']': '', '{': '', '}': '', 'ґ': '', 'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i',
                  'Є': 'e'}

        for key in slovar:
            name = name.replace(key, slovar[key])
        return name



class EmailGenerator:

    def __init__(self, domain=None, api_domain='api.temp-mail.ru'):
        self.domain = domain
        self.api_domain = api_domain

    def get_mail_domain(self):
        """
        :return: список доменов сервеcа https://temp-mail.ru/
        """
        url = 'http://%s/request/domains/format/json/' % self.api_domain
        req = requests.get(url)
        return req.json()

    def get_email_address(self, name):
        """
        домен захаркоден
        :param name: имя пользователя
        :return: емейл адрес
        """
        login = name
        return '%s@testmail.cognita.ru ' % (login)

class EntryRegData:

    def __init__(self, len_firstname=None, len_lastname=None, len_secondname=None, name_file=None):
        if len_firstname == None:
            self.len_firstname = 10
        if len_lastname == None:
            self.len_lastname = 10
        if len_secondname == None:
            self.len_secondname = 10
        self.name_file = name_file
        self.translit = Transliterator()
        self.email = EmailGenerator()

    def get_reg_data(self):
        """
        :return объект Registration с полученными данными регистрации
        """
        firstname = random_string_name(self.len_firstname)
        return [ModelRegistration(firstname=self.translit.transliterate_cyrillic(firstname),
                             lastname=self.translit.transliterate_cyrillic(random_string_name(self.len_lastname)),
                             secondname=self.translit.transliterate_cyrillic(random_string_name(self.len_secondname)),
                             email=self.email.get_email_address(firstname))]


def registration_users(*args, **kwargs):
    try:
        url_registration = "%susers" % test_case['url']
        entry = EntryRegData()
        registration = entry.get_reg_data()[0]
        lastname = registration.lastname
        firstname = registration.firstname
        secondname = registration.secondname
        email = registration.email
        body = {
            'user': {
                'info': {
                    'firstname': firstname,
                    'lastname': lastname,
                    'secondname': secondname
                },
                'login': email,
                'password': '12345678'
            }
        }
        answ = requests.post(url=url_registration, headers=test_case['new_headers'], json=body, verify=False)
        #print 'User: ' + answ.content
        if answ.status_code != 201:
            logger.error('User: %s, NOT REGISTRATION!' % (email))
            raise HttpCode(answ.status_code)
        logger.debug('REGISTRATION USER: %s' % (email))
    except Exception as exc:
        logger.error('Сценарий провалился с %s' % exc)
        raise


def shoot_one(missile, marker, results):
    try:
        test_case['RegistrationUser'] = "1"
        with measure("registrationuser", results):
            registration_users()
    except RuntimeError as e:
        logger.error('Следующий сценарий %s провалился с %s', marker, e)


if __name__ == '__main__':
    shoot_one("", "", Queue())


SCENARIOS = {
    "shoot_one": shoot_one
}

#try:
#    shoot_one("", "", Queue())
#except Exception as exc:
#    print "MY EXCEPTION" + exc
