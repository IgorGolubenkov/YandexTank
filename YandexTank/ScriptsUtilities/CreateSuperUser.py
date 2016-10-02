

class ActivationSuperuser:

    def __init__(self):
        self.headers = {}
        self.data = {}
        self.data['url'] = ""   # продакшн ""

    def req_create_claims(self):
        """
        Создание заявки на книговыдачу
        :return:
        """
        url = '%s' % self.data['url']
        claim = {
            "claim": {
            "organization_name": "string",
            "organization_inn": "string",
            "organization_kpp": "string",
            "organization_address": "string",
            "phone": "string",
            "email": "string",
            "chief_last_name": "string",
            "chief_first_name": "string",
            "chief_middle_name": "string",
            "license_count": "number",
            "comment": "string"
          }
        }

    def confirmation_create_claims(self):
        """
        подтверждение зарегистрованного с помощью заявки пользователя
        :return:
        """

    def req_login(self):
        """
        Авторизация зарегистрованного с помощью заявки пользователя
        :return:
        """

    def req_get_claims_list(self):
        """
        получение списка заявок пользователя
        :return:
        """

    def req_activation_cert(self):
        """
        активация сертификаты полученного через soap
        :return:
        """

#package = {
#  "package": {
#    "name": "string",
#    "expire_at": "datetime",
#    "license_count": "number",
#    "grade_restriction": "number",
#    "comment": "string",
#    "quantity": "number",
#    "catalog_ids": [
#      "string"
#    ]
#  }
#}

# package  - сертификаты
# name  - имя сертификата
# expire_at  - дата до которой можно активировать сертификаты
# license_count  - колличество кодов активации
# grade_restriction
# grade_restriction
# comment
# catalog_ids  - массив с id catalog (id книг)


#code = {
#  "code": "string"
#}