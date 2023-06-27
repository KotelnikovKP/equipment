from rest_framework import authentication


class BearerAuthentication(authentication.TokenAuthentication):
    # Используется стандартный класс, только ключевое слово 'Token' заменено на 'Bearer'
    keyword = 'Bearer'
