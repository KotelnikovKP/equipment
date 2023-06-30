from rest_framework import permissions


class EquipmentTypePermission(permissions.BasePermission):
    """
        Раздача привилегий для методов для типа оборудования

        Список - авторизованным
        Создание и изменение - только администратору
    """

    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        if view.action == 'list':
            return request.user.is_authenticated
        elif view.action in ['create', 'update']:
            return request.user.is_authenticated and request.user.is_staff
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'OPTIONS':
            return True
        if view.action == 'update':
            return request.user.is_authenticated and request.user.is_staff
        else:
            return False


class EquipmentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        if view.action in ['list', 'create', 'retrieve', 'update', 'destroy']:
            return request.user.is_authenticated
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'OPTIONS':
            return True
        if view.action in ['list', 'create', 'retrieve', 'update', 'destroy']:
            return request.user.is_authenticated
        else:
            return False
