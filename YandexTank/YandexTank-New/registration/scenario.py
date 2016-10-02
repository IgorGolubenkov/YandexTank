# -*- coding: utf-8 -*-

import logging
import string
import random
import requests
log = logging.getLogger(__name__)

requests.packages.urllib3.disable_warnings()

class ModelRegistration:

    def __init__(self, firstname=None, lastname=None, secondname=None,
                 email=None):
        self.firstname = firstname
        self.lastname = lastname
        self.secondname = secondname
        self.email = email

    def __repr__(self):
        return "%s + %s + %s + %s" % (self.firstname, self.lastname, self.secondname, self.email)

class StrHelper:

    def random_string_name(self, len):
        """
        get a string from lowercaseto length
        """
        symbols = string.ascii_lowercase
        return ''.join([random.choice(symbols) for i in range(len)])

    def random_number_phone(self):
        """
        received a random phone number in the area +7
        """
        symbols = string.digits
        return "+79" + "".join([random.choice(symbols) for i in range(9)])

class Transliterator:

    def transliterate_cyrillic(self, name):
        """
        Transliterate from Latin to Cyrillic
        """
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
        """
        Transliteracy with kirilitsi to Latin
        """
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
        self.str = StrHelper()

    def get_reg_data(self):
        """
        :return объект Registration с полученными данными регистрации
        """
        firstname = self.str.random_string_name(self.len_firstname)
        return [ModelRegistration(firstname=self.translit.transliterate_cyrillic(firstname),
                             lastname=self.translit.transliterate_cyrillic(self.str.random_string_name(self.len_lastname)),
                             secondname=self.translit.transliterate_cyrillic(self.str.random_string_name(self.len_secondname)),
                             email=self.email.get_email_address(firstname))]

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

class LoadTest(object):

    def __init__(self, gun):

        # you'll be able to call gun's methods using this field:
        self.gun = gun

        # for example, you can get something from the 'ultimate' section of a config file:
        my_var = self.gun.get_option("my_var", "hello")

    def case1(self, missile):

        with self.gun.measure("case1"):
            log.info("Shoot case 1: %s", missile)

        with self.gun.measure("case1_step2") as sample:
            log.info("Shoot case 1, step 2: %s", missile)
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
                if answ.status_code != 201:
                    log.error('User: %s, NOT REGISTRATION!' % (email))
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