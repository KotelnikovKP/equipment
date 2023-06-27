from rest_framework import pagination


class EquipmentPageNumberPagination(pagination.PageNumberPagination):
    def get_paginated_response_schema(self, schema):
        # Уберем алгоритм формирования OpenAPI схемы от данного класса - схема будет от сериализатора
        return schema['items']
