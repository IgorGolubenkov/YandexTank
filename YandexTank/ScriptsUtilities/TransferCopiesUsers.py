# -*- coding: utf-8 -*-


import requests
requests.packages.urllib3.disable_warnings()
import os
import sys
import argparse
import datetime
import time

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--login', default='0909books@mail.ru')
    parser.add_argument('-p', '--password', default='12345678')
    parser.add_argument('-url', '--url', choices=['debug', 'release'], default='debug')
    parser.add_argument('-m', '--metod', choices=['userID, createLib, libraryID, transfer', 'unixtime'], default='createLib')
    parser.add_argument('-lib', '--namelib', default='newtank_test1')
    parser.add_argument('-u', '--users', default='novyi')
    parser.add_argument('-b', '--library', default='newtank1')
    parser.add_argument('-n', '--numlib', default='80')
    parser.add_argument('-nc', '--numcop', default='25')
    parser.add_argument('-life', '--life', default='20161005')
    return parser

parser = createParser()
namespace = parser.parse_args(sys.argv[1:])

if namespace.url == "debug":
    url_default = 'http://sandbox.cognita.ru'
    protocol = 'http'
    host_default = 'sandbox.cognita'
elif namespace.url == "release":
    url_default = 'https://lecta.ru'
    protocol = 'https'
    host_default = 'lecta'

url = {}
url['url'] = url_default
url['url_ds'] = '%s://ds.%s.ru/api/' % (protocol, host_default)
url['url_id'] = '%s://id.%s.ru/api/' % (protocol, host_default)


class LectaApi:

    def __init__(self, login=None, password=None):
        self.login = login
        self.password = password
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.new_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/vnd.api+json'
        }

    def login_user_obj(self):
        """
        Авторизация users/login
        :return RESPONSE request object
        """
        req = "%s/api/v2/users/login" % url['url']
        body = {
            "data": {
                "type": "token",
                "attributes": {
                    "login": self.login,
                    "password": self.password
                }
            }
        }
        return requests.post(url=req, headers=self.new_headers, json=body, verify=False)

    def get_user_ID_login(self, login, password):
        """
        Авторизация users/login
        :argument login, password передаем непосредственно в функцию
        :return USER_ID
        """
        req = "%s/api/v2/users/login" % url['url']
        body = {
        "login": login,
        "password": password
        }
        answ = requests.post(url=req, headers=self.new_headers, json=body, verify=False)
        return answ.json()['user_id']

    def login_user(self):
        """
        Авторизация  users/login
        :return 'access_token'
        """
        req = "%s/api/v2/users/login" % url['url']
        body = {
            "data": {
                "type": "token",
                "attributes": {
                    "login": self.login,
                    "password": self.password
                        }
                    }
                }
        answ = requests.post(url=req, headers=self.new_headers, json=body, verify=False)
        return answ.json()['access_token']

    def get_token_headers(self):
        """
        Добавление токена в загаловки
        """
        token = self.login_user()
        self.headers['X-Access-Token'] = token

    def get_account_and_token(self):
        """
        Добавление id аккаунта "X-Account" в загаловки
        """
        account = self.get_account_ID()
        self.headers['X-Account'] = account

    def old_token_and_account_headers(self):
        """
        получаем авторизованные заголовки старое апи
        :return загаловки
        """
        self.get_account_and_token()
        headers = self.headers
        return headers

    def get_account_ID(self):
        """
        Получаем X Account
        ручка: users/me/accounts
        :return id аккаунта "X-Account"
        """
        token = self.login_user()
        self.headers['X-Access-Token'] = token
        req = '%susers/me/accounts' % url['url_id']
        answ = requests.get(url=req, headers=self.headers, verify=False)
        #print("\nStatus_accounts_id:", answ.status_code)
        for x in answ.json():
            if x['isOrganization'] == False:
                return x['id']
        #preparation_x_account = answ.json()[0]

    def login_user_data(self, login, password):
        """
        Авторизация users/login
        :argument логин и пароль
        :return авторизованный токен
        """
        req = "%s/api/v2/users/login" % url['url']
        body = {
            "data": {
                "type": "token",
                "attributes": {
                    "login": login,
                    "password": password
                }
            }
        }
        answ = requests.post(url=req, headers=self.new_headers, json=body, verify=False)
        return answ.json()['access_token']

    def get_account_ID_user(self, login, password):
        """
        Получение id аккаунта "X-Account"
        ручка: users/me/accounts
        :argument login and password передаем непосредственно в функцию
        :return id X-Account
        """
        token = self.login_user_data(login, password)
        self.headers['X-Access-Token'] = token
        req = '%susers/me/accounts' % url['url_id']
        answ = requests.get(url=req, headers=self.headers, verify=False)
        #print("\nStatus_accounts_id:", answ.status_code)
        preparation_x_account = answ.json()[0]
        return preparation_x_account['id']

    def create_libraries(self, name):
        """
        Создание библиотеки
        :return имя библиотеки
        """
        self.get_account_and_token()
        req = '%slibraries' % url['url_ds']
        body ={
            "name": name
        }
        answ = requests.post(url=req, headers=self.headers, json=body, verify=False)
        print("\nCreate_libraries:", answ.status_code)
        return answ.json()

    def trail_create_libraries(self, name):
        """ Пробное создание библиотеки
        название передается аргументом
        """
        headers_2 = self.old_token_and_account_headers()
        req = '%slibraries' % url['url_ds']
        body ={
            "name": name
        }
        answ = requests.post(url=req, headers=headers_2, json=body, verify=False)
        print("\nCreate_libraries:", answ.status_code)
        return answ.json()

    def get_all_library_user(self):
        """
        Получение всех библиотек пользователя
        """
        req = '%slibraries' % url['url_ds']
        answ = requests.get(url=req, headers=self.headers, verify=False)
        print("\nStatus_get_libraryes:", answ.status_code)
        return answ.json()

    def get_keys(self):
        """
        Не реализовано.
        Получение старого портфеля
        Получение коллекции пользователя с данными
        """
        req = '%sclient/keys' % url['url_ds']
        answ = requests.get(url=req, headers=self.headers, verify=False)
        print("\nStatus_get_collection:", answ.status_code)
        return answ.json()

class UserID(LectaApi):


    def get_users_id_list(self, name_file):
        """
        Создаем список из user id
        :return список 'user_id'
        """
        list_usersID = []
        password = "12345678"
        path_to_file_login = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data/%s.txt" % name_file)
        for user_login in open(path_to_file_login, "r").readlines():
            login = user_login.rstrip('\n')
            usersID = self.get_user_ID_login(login, password)
            list_usersID.append(usersID)
            #print(usersID)
        return list_usersID

    def two_get_usersID_list(self, name_file):
        """
        Метод получения спика id account
        login and password не нужно вызывать при инициализации класса
        """
        list_usersID = []
        password = "12345678"
        path_to_file_login = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data/%s.txt" % name_file)
        for user_login in open(path_to_file_login, "r").readlines():
            login = user_login.rstrip('\n')
            usersID = self.get_account_ID_user(login, password)
            list_usersID.append(usersID)
            print(usersID)
        return list_usersID

    def get_usersID_list(self, name_file):
        """
        Метод получения спика id account
        login and password не нужно вызывать при инициализации класса
        по другому происходит построчное чтение файла
        id аккаунта 'X-Account' через user/me
        """
        list_usersID = []
        password = "12345678"
        path_to_file_login = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data/%s.txt" % name_file)
        for user_login in open(path_to_file_login, "r").readlines():
            login = user_login[:-1]
            #print(login)
            usersID = self.get_account_ID_user(login, password)
            list_usersID.append(usersID)
            #print(usersID)
        return list_usersID

    def activate_package(self):
        """
        Не реализован
        Метод активации комплекта
        """
        req = "packagecodes/activate"


class Libraries:

    def __init__(self, login=None, password=None):
        self.headers = LectaApi(login, password).old_token_and_account_headers()


    def get_catalogID_list(self):
        """
        Получение списка из всех catalogID
        у авторизованного пользователя
        """
        list_catalogID = []
        req = '%scatalog' % url['url_ds']
        answ = requests.get(url=req, headers=self.headers, verify=False)
        for array_catalog in answ.json():
            catalogID = array_catalog['id']
            list_catalogID.append(catalogID)
            print(catalogID)
        return list_catalogID[:26]


    def create_number_libraries(self, number, name, num_copies):
        """
        Создание библиотек и запись в файл ID library
        В аргументах передается
        number= количество библиотек
        name= дефолтное имя, полное имя индекс-name
        num_copies= количество копий каталога в библотеке
        """
        index = 0
        list_catalogID = self.get_catalogID_list()
        path_to_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data/library_%s.txt" % name)
        with open(path_to_file, 'w', encoding="utf-8") as file:
            for x in range(number):
                index += 1
                name_libraries = "%s-%s" % (index, name)
                req = '%slibraries' % url['url_ds']
                body = {
                    "name": name_libraries
                }
                answ = requests.post(url=req, headers=self.headers, json=body, verify=False)
                if answ.status_code == 201:
                    libraryID = answ.json()['id']
                    self.transfer_content_to_library(list_catalogID, libraryID, num_copies)
                    file.write(libraryID + '\n')
                    print("Библиотека: %s, СОЗДАНА" % name_libraries)
                else:
                    print("Библиотека: %s, не создана" % name_libraries)

    def get_libraryID_list(self, name_file):
        """
        Получение списка из ID библиотек из записанного файла
        """
        list_libraryID = []
        path_to_file_library = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data/%s.txt" % name_file)
        for library in open(path_to_file_library, "r").readlines():
            library_ID = library.rstrip('\n')
            list_libraryID.append(library_ID)
            #print(library_ID)
        return list_libraryID

    def transfer_content_to_library(self, list_catalogID, libraryID, num_copies):
        """
        Метод передачи контента в библиотеки
        list_catalogID= список из элементов каталога
        libraryID= ID библиотеки куда передаются копии
        num_copies= количество копий для передачи в библиотеку
        """
        for catalogID in list_catalogID:
            req = '%scopies/multi' % url['url_ds']
            body = {
                "catalog" : catalogID,
                "expirationDate": None,
                "library": libraryID,
                "qty": num_copies
            }
            answ = requests.post(url=req, headers=self.headers, json=body, verify=False)
            if answ.status_code != 201:
                print("Элемент каталога ID: %s, не передан в библиотеку ID: %s" % (catalogID, libraryID))
            else:
                print("Передан каталог ID: %s в библиотеку: %s" % (catalogID, libraryID))

    def get_mili_unixtime(self, yearmonday, hour=23, min=59, sec=59):
        """
        Получаем unix время в милисекундах
        :argument год(формат:ХХХХ) + месяц(формат:ХХ) + день(формат:ХХ)
        остальное автоматически подставляется, последняя секунда дня
        """
        year = yearmonday[:4]
        if yearmonday[4] == str(0):
            day = yearmonday[-1:]
        else:
            day = yearmonday[-2:]
        if yearmonday[4] == str(0):
            month = yearmonday[5]
        else:
            month = yearmonday[4:6]
        time_unix = datetime.datetime(int(year), int(month), int(day), hour, min, sec)
        time_unix_second = time.mktime(time_unix.timetuple())
        return int(round(time_unix_second * 1000))

    def transfer_copies_of_users(self, user_file, library_file, life_copies):
        """
        Передача копиий каталога из конкретной библиотеки
        список из user_id парсинг файла с логинами
        список из library_id из файла с id библиотек
        catalog_id список всех id у пользователя
        """
        userID = UserID()
        list_usersID = userID.get_users_id_list(user_file)
        list_library = self.get_libraryID_list(library_file)
        list_catalogID = self.get_catalogID_list()
        index = -1
        for user in list_usersID:
            index += 1
            library_index = index // 25
            for catalog in list_catalogID:
                req = '%scopies/createLeasesForUsers' % url['url_ds']
                body = {
                    "copyParams": [{"catalog": catalog, "expirationDate": None}],
                    "expirationDate": self.get_mili_unixtime(life_copies),
                    "fromLibrary": list_library[library_index],
                    "users": [user]
                    }
                answ = requests.post(url=req, headers=self.headers, json=body, verify=False)
                print(answ.status_code)

    def transfer_array_copies_of_users(self, user_file, library_file):
        """
        Передача копиий каталога из конкретной библиотеки
        список из user_id парсинг файла с логинами
        список из library_id из файла с id библиотек
        catalog_id все передаются массивом
        """
        userID = UserID()
        list_usersID = userID.get_users_id_list(user_file)
        list_library = self.get_libraryID_list(library_file)
        list_catalogID = self.get_catalogID_list()
        library_index = 0
        index = -1
        for user in list_usersID:
            index += 1
            if index % 25 == 0:
                library_index += 1
            for catalog in list_catalogID:
                req = '%scopies/createLeasesForUsers' % url['url_ds']
                body = {
                    "copyParams": [
                        {"catalog": catalog, "expirationDate": None},
                        {"catalog": catalog, "expirationDate": None},
                        {"catalog": catalog, "expirationDate": None},
                        {"catalog": catalog, "expirationDate": None},
                    ],
                    "expirationDate": 1480585105827,
                    "fromLibrary": list_library[library_index],
                    "users": [user]
                }
                answ = requests.post(url=req, headers=self.headers, json=body, verify=False)
                print(answ.status_code)

if __name__ == '__main__':
    if namespace.metod == 'userID':
        #class_libraries = Libraries()
        user_aut = UserID()
        print(user_aut.get_usersID_list(namespace.users))
        # проверяем создание списка из ID пользователей
    elif namespace.metod == 'createLib':
        library = Libraries(login=namespace.login, password=namespace.password)  # авторизация
        library.create_number_libraries(number=int(namespace.numlib), name=namespace.namelib, num_copies=int(namespace.numcop))
        # Создание новых библиотек и передача копий из каталога
    elif namespace.metod == 'libraryID':
        user_aut = UserID()
        user_aut.two_get_usersID_list(namespace.library)
        # Получение списка из librari id
    elif namespace.metod == 'transfer':
        library = Libraries(login=namespace.login, password=namespace.password)  # авторизация
        #library.get_catalogID_list()
        library.transfer_copies_of_users(user_file=namespace.users, library_file="library_%s" % namespace.namelib, life_copies=namespace.life)
        # передача копий пользователям
    elif namespace.metod == 'unixtime':
        user_aut = UserID()
        print(user_aut.get_mili_unixtime(namespace.life))
    else:
        print("Что то пошло не так.....")
