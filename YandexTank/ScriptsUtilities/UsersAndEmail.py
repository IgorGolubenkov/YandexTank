# -*- coding: utf-8 -*-


import requests
requests.packages.urllib3.disable_warnings()
from hashlib import md5
import time
import re
import os
import sys
import argparse

username_default = 'Новый'
lasrname_default = 'Танк'
number_user_default = '10'

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', default=number_user_default)
    parser.add_argument('-u', '--username', default=username_default)
    parser.add_argument('-l', '--lastname', default=lasrname_default)
    parser.add_argument('-url', '--url', choices=['debug', 'release'], default='debug')
    return parser

parser = createParser()
namespace = parser.parse_args(sys.argv[1:])

if namespace.url == "debug":
    url_default = 'http://sandbox.cognita.ru'
elif namespace.url == "release":
    url_default = 'https://lecta.ru'

url = {}
url['url'] = url_default
print("Url for registration: %s" % url['url'])

class Email:


    def get_hash(self, email):
        """
        :argument: емейл
        :return хеш конректного емейла
        """
        return md5(email.encode('utf-8')).hexdigest()

    def get_mailbox(self, email):
        """
        :argument: емейл
        :return письма в виде json
        """
        api_domain = "api.temp-mail.ru"
        email_hash = self.get_hash(email)
        url = 'http://%s/request/mail/id/%s/format/json/' % (api_domain, email_hash)
        req = requests.get(url)
        return req.json()

    def get_mailbox_status(self, email):
        """
        :argument: емейл
        :return все данные запроса проверки временной почты
        """
        api_domain = "api.temp-mail.ru"
        email_hash = self.get_hash(email)
        url = 'http://%s/request/mail/id/%s/format/json/' % (api_domain, email_hash)
        req = requests.get(url)
        return req

    def get_url_for_confirmation(self, email):
        """ НЕ используется,
        :return ссылка для подтверждения регистарции
        плохой вариант регулярного выражения
        """
        for x in range(5):
            time.sleep(2)
            json_mail = self.get_mailbox(email)
        result = re.findall('http://\w+.\w+/\w+/\w+/....................', str(json_mail))[0]
        return re.sub('lecta', 'sandbox.cognita', str(result))

    def test_get_url_for_confirmation(self, email):
        """
        Запрос к почтовому сервису
        вытаскивание URL для подтверждения емейла
        """
        time.sleep(2)
        mail = self.get_mailbox_status(email)
        status = mail.status_code
        json_mail = mail.json()
        if status == 200:
            return re.findall('="(.[^">]+)">', str(json_mail))[0]
            #return re.sub('lecta', 'sandbox.cognita', str(result))
        else:
            for x in range(5):
                mail = self.get_mailbox_status(email)
                json_mail = mail.json()
                status = mail.status_code
                time.sleep(2)
                if status == 200:
                    return re.findall('="(.[^">]+)">', str(json_mail))[0]
                    #return re.sub('lecta', 'sandbox.cognita', str(result))
                else:
                    for x in range(10):
                        mail = self.get_mailbox_status(email)
                        json_mail = mail.json()
                        status = mail.status_code
                        time.sleep(2)
                        if status == 200:
                            return re.findall('="(.[^">]+)">', str(json_mail))[0]
                            #return re.sub('lecta', 'sandbox.cognita', str(result))
                        else:
                            print("Не пришло сообщение для подтверждения")

    def open_link(self, email_url):
        """
        :argument: URL для перехода
        GET запрос подтверждения емейла
        Возможность проверки URL редиректа
        :return всех данные запроса
        """
        return requests.get(url=email_url, allow_redirects=True, verify=False)



class Registration:

    headers_2 = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def get_domen_email(self):
        """
        Получение домена для проверки почты от сервиса временной почты
        """
        api_domain = 'api.temp-mail.ru'
        url = 'http://%s/request/domains/format/json/' % api_domain
        req = requests.get(url)
        return req.json()[0]

    def transliterate(self, name):
        """
        Траслитерация с кирилици на латиницу
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

    def registration_number_users(self, number_of_users, name_users, lastname_users):
        """
        Регистрация новых пользователей
        number_of_users= можно задать количестко пользователей,
        name_users= имя,
        lastname_users= фамилию,
        имя присваивается с префиксом: каждый новый пользователь прибавляет префикс на еденицу
        """
        req = "%s/api/v2/users" % url['url']
        file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.txt" % self.transliterate(name_users))
        url_email = self.get_domen_email()
        index = 0
        mailbox = Email()
        correct_redirect_url = "%s/email/confirmation/success" % url['url']  # шаблон урла редиректа
        with open(file, 'w', encoding="utf-8") as file:
            for x in range(int(number_of_users)):
                index += 1
                firstname = name_users + str(index)
                lastname = lastname_users + str(index)
                secondname = firstname + lastname
                email = (self.transliterate(firstname) + url_email)
                body = {
                    'user':{
                        'info':{
                            'firstname':firstname,
                            'lastname':lastname,
                            'secondname':secondname
                            },
                        'login': email,
                        'password':'12345678'
                        }
                    }

                answ = requests.post(url=req, headers=self.headers_2, json=body, verify=False)
                # запрос на регистрацию нового пользователя
                if answ.status_code == 201:
                    # получение ссылки для подтверждения
                    email_url = mailbox.test_get_url_for_confirmation(email)
                    # get запрос подтверждения емейла
                    link = mailbox.open_link(email_url)
                    # получение урла редиректа подтверждения емейла
                    redirect_url = link.url
                    print("Redirect to: %s" % redirect_url)
                    if redirect_url == correct_redirect_url:
                        login = answ.json()['login']
                        # запись в файл зарегистрированных логинов
                        file.write(login + '\n')
                        print("Registration %s user, email: %s, url: %s" % (index, email, email_url))
                    else:
                        print("Не совершается переход по ссылке", link.status_code)
                else:
                    print("Пользователь не зарегистрирован:", body)
                    print(answ.json())
            file.close()


registration = Registration()
email = Email()

if __name__ == '__main__':
    registration.registration_number_users(number_of_users=namespace.number, name_users=namespace.username,
                                           lastname_users=namespace.lastname)
    # регистрация новых пользователей

"""
mail = "vdlao5@extremail.ru"
req = email.get_mailbox_status(email=mail)
print(req.status_code)
# Проверка статуса запроса емейла
print(req.json())
# Проверка ответа емейл сервиса
email_url = email.test_get_url_for_confirmation(mail)
print(email_url)
# получение урла для подтверждения регистарции
print(email.open_link(email_url)
# подтверждение емейла
"""





