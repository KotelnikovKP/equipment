from rest_framework import permissions


class EquipmentTypePermission(permissions.BasePermission):
    """
        Раздача привилегий для методов для типа оборудования

        Список - авторизованным
        Создание и изменение - только администратору
    """

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated
        elif view.action in ['create', 'update']:
            return request.user.is_authenticated and request.user.is_staff
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'update':
            return request.user.is_authenticated and request.user.is_staff
        else:
            return False
