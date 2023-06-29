"""
    Сервисный слой приложения
"""
import time

from rest_framework import serializers
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from backend.serializers import EquipmentTypeListSerializer, EquipmentListSerializer, PaginationListSerializer, \
    EquipmentTypeSerializer, EquipmentTypeCreateUpdateSerializer, EquipmentTypeRequestSerializer, \
    EquipmentDetailsSerializer, EquipmentSerializer, EquipmentRequestSerializer, EquipmentUpdateSerializer, \
    EquipmentCreateSerializer, EquipmentDeleteSerializer, ErrorCreateEquipmentSerializer, InfoCreateEquipmentSerializer, \
    UserRegisterSerializer, UserSerializer, UserCreateSerializer, UserDetailsSerializer


class GetEquipmentTypeListService:
    """
        Сервис получения пагинированого и отфильтрованного списка типов оборудования
    """

    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> EquipmentTypeListSerializer:
        """
            Получение пагинированого и отфильтрованного списка типов оборудования
        """

        # Фильтрация списка
        queryset = view.filter_queryset(view.get_queryset())

        # Пагининация списка
        page = view.paginate_queryset(queryset)
        if page is None:
            equipment_type_list_serializer = view.get_serializer(queryset, many=True)
            count = view.paginator.count
            items_per_page = view.paginator.per_page
            start_item_index = 0 if count == 0 else 1
            end_item_index = count
            previous_page = None
            current_page = 1
            next_page = None
        else:
            equipment_type_list_serializer = view.get_serializer(page, many=True)
            count = view.paginator.page.paginator.count
            items_per_page = view.paginator.page.paginator.per_page
            start_item_index = view.paginator.page.start_index()
            end_item_index = view.paginator.page.end_index()
            previous_page = view.paginator.page.previous_page_number() if view.paginator.page.has_previous() else None
            current_page = view.paginator.page.number
            next_page = view.paginator.page.next_page_number() if view.paginator.page.has_next() else None

        # Формирование дополнительной информации по результатам пагинации
        pagination_list_serializer = PaginationListSerializer(
            data={
                'count_items': count,
                'items_per_page': items_per_page,
                'start_item_index': start_item_index,
                'end_item_index': end_item_index,
                'previous_page': previous_page,
                'current_page': current_page,
                'next_page': next_page,
            }
        )
        pagination_list_serializer.is_valid()

        # Формирование схемы ответа
        return_serializer = EquipmentTypeListSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok' if count > 0 else 'Result set is empty',
                'result': equipment_type_list_serializer.data,
                'retExtInfo': pagination_list_serializer.data,
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class CreateEquipmentTypeService:
    """
        Сервис создания типа оборудования
    """

    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> EquipmentTypeCreateUpdateSerializer:
        """
            Создание типа оборудования
        """

        # Обработка входящих данных (валидация и сохранение)
        equipment_type_serializer = EquipmentTypeRequestSerializer(data=request.data)
        equipment_type_serializer.is_valid(raise_exception=True)
        instance = equipment_type_serializer.save()

        # Преобразование данных в стандартную схему для ответа
        equipment_type_serializer = EquipmentTypeSerializer(data=equipment_type_serializer.data, instance=instance)
        equipment_type_serializer.is_valid()

        # Формирование схемы ответа
        return_serializer = EquipmentTypeCreateUpdateSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok',
                'result': equipment_type_serializer.data,
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class UpdateEquipmentTypeService:
    """
        Сервис изменения типа оборудования
    """

    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> EquipmentTypeCreateUpdateSerializer:
        """
            Изменения типа оборудования
        """

        # Обработка входящих данных (корректность ключа)
        pk = kwargs.get("pk", None)
        if not pk:
            raise ParseError(f"Request must have 'id' parameter", code='id')
        try:
            instance = view.queryset.get(pk=pk)
        except:
            raise NotFound(f"Equipment type with id='{pk}' was not found", code='id')

        # Обработка входящих данных (валидация и сохранение)
        equipment_type_serializer = EquipmentTypeRequestSerializer(data=request.data, instance=instance)
        equipment_type_serializer.is_valid(raise_exception=True)
        instance = equipment_type_serializer.save()

        # Преобразование данных в стандартную схему для ответа
        equipment_type_serializer = EquipmentTypeSerializer(data=equipment_type_serializer.data, instance=instance)
        equipment_type_serializer.is_valid()

        # Формирование схемы ответа
        return_serializer = EquipmentTypeCreateUpdateSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok' if request.data else 'You changed nothing',
                'result': equipment_type_serializer.data,
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class GetEquipmentListService:
    """
        Сервис получения пагинированого и отфильтрованного списка оборудования
    """

    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> EquipmentListSerializer:
        """
            Получение пагинированого и отфильтрованного списка оборудования
        """

        # Фильтрация списка
        queryset = view.filter_queryset(view.get_queryset())

        # Пагининация списка
        page = view.paginate_queryset(queryset)
        if page is None:
            equipment_list_serializer = view.get_serializer(queryset, many=True)
            count = view.paginator.count
            items_per_page = view.paginator.per_page
            start_item_index = 0 if count == 0 else 1
            end_item_index = count
            previous_page = None
            current_page = 1
            next_page = None
        else:
            equipment_list_serializer = view.get_serializer(page, many=True)
            count = view.paginator.page.paginator.count
            items_per_page = view.paginator.page.paginator.per_page
            start_item_index = view.paginator.page.start_index()
            end_item_index = view.paginator.page.end_index()
            previous_page = view.paginator.page.previous_page_number() if view.paginator.page.has_previous() else None
            current_page = view.paginator.page.number
            next_page = view.paginator.page.next_page_number() if view.paginator.page.has_next() else None

        # Формирование дополнительной информации по результатам пагинации
        pagination_list_serializer = PaginationListSerializer(
            data={
                'count_items': count,
                'items_per_page': items_per_page,
                'start_item_index': start_item_index,
                'end_item_index': end_item_index,
                'previous_page': previous_page,
                'current_page': current_page,
                'next_page': next_page,
            }
        )
        pagination_list_serializer.is_valid()

        # Формирование схемы ответа
        return_serializer = EquipmentListSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok' if count > 0 else 'Result set is empty',
                'result': equipment_list_serializer.data,
                'retExtInfo': pagination_list_serializer.data,
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class CreateEquipmentService:
    """
        Сервис создания оборудования
    """

    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> EquipmentCreateSerializer:
        """
            Создание оборудования
        """

        # Приведение входящих данных к списку, если пришло единичное оборудование
        if not isinstance(request.data, list):
            equipments = [request.data]
        else:
            equipments = request.data

        saved_equipments = list()
        failed_equipments = list()

        # Обработка каждого оборудования в списке
        for i, equipment in enumerate(equipments):

            # Ловим ошибки валидации, чтобы не отваливаться, а сохранять в список ошибок
            try:
                # Обработка входящих данных (валидация и сохранение)
                equipment_serializer = EquipmentRequestSerializer(data=equipment)
                equipment_serializer.is_valid(raise_exception=True)
                equipment_serializer.validated_data['created_by_id'] = request.user.id
                equipment_serializer.validated_data['updated_by_id'] = request.user.id
                instance = equipment_serializer.save()

                # Преобразование данных в стандартную схему для ответа
                equipment_serializer = EquipmentSerializer(data=equipment_serializer.data, instance=instance)
                equipment_serializer.is_valid()

                # Добавление данных в массив для ответа
                saved_equipments.append(equipment_serializer.data)

            except serializers.ValidationError as e:

                # Формирование схемы ошибочной входящей записи
                error_equipment_serializer = ErrorCreateEquipmentSerializer(
                    data={
                        "index": i,
                        "error": str(e),
                        "data": str(equipment)
                    }
                )
                error_equipment_serializer.is_valid()

                # Добавление данных в массив ошибок для ответа
                failed_equipments.append(error_equipment_serializer.data)

        # Формирование дополнительной информации по результатам создания оборудования
        info_created_serializer = InfoCreateEquipmentSerializer(
            data={
                "count": len(equipments),
                "saved": len(saved_equipments),
                "failed": len(failed_equipments),
                "errors": failed_equipments,
            }
        )
        info_created_serializer.is_valid()

        # Формирование схемы ответа
        return_serializer = EquipmentCreateSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok' if len(failed_equipments) == 0 else 'There are some errors',
                'result': saved_equipments,
                'retExtInfo': info_created_serializer.data,
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class GetEquipmentDetailsService:
    """
        Сервис получения детальной информации по заданному оборудованию
    """

    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> EquipmentDetailsSerializer:
        """
            Получение детальной информации по заданному оборудованию
        """

        # Обработка входящих данных (корректность ключа)
        pk = kwargs.get("pk", None)
        if not pk:
            raise ParseError(f"Request must have 'id' parameter", code='id')
        try:
            instance = view.queryset.get(pk=pk)
        except:
            raise NotFound(f"Equipment with id='{pk}' was not found", code='id')

        # Преобразование данных в стандартную схему для ответа
        equipment_serializer = EquipmentSerializer(
            data={
                'id': instance.id,
                'equipment_type': instance.equipment_type_id,
                'serial_number': instance.serial_number,
                'description': instance.description
            },
            instance=instance
        )
        equipment_serializer.is_valid()

        # Формирование схемы ответа
        return_serializer = EquipmentDetailsSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok',
                'result': equipment_serializer.data,
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class UpdateEquipmentService:
    """
        Сервис изменения оборудования
    """

    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> EquipmentUpdateSerializer:
        """
            Изменение оборудования
        """

        # Обработка входящих данных (корректность ключа)
        pk = kwargs.get("pk", None)
        if not pk:
            raise ParseError(f"Request must have 'id' parameter", code='id')
        try:
            instance = view.queryset.get(pk=pk)
        except:
            raise NotFound(f"Equipment with id='{pk}' was not found", code='id')

        # Обработка входящих данных (валидация и сохранение)
        equipment_serializer = EquipmentRequestSerializer(data=request.data, instance=instance)
        equipment_serializer.is_valid(raise_exception=True)
        equipment_serializer.validated_data['updated_by_id'] = request.user.id
        instance = equipment_serializer.save()

        # Преобразование данных в стандартную схему для ответа
        equipment_serializer = EquipmentSerializer(data=equipment_serializer.data, instance=instance)
        equipment_serializer.is_valid()

        # Формирование схемы ответа
        is_data = request.data.get('equipment_type', None) is not None or \
            request.data.get('serial_number', None) is not None or \
            request.data.get('description', None) is not None
        return_serializer = EquipmentUpdateSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok' if is_data else 'You changed nothing',
                'result': equipment_serializer.data,
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class DeleteEquipmentService:
    """
        Сервис удаления оборудования
    """

    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> EquipmentDeleteSerializer:
        """
            Удаление оборудования
        """

        # Обработка входящих данных (корректность ключа)
        pk = kwargs.get("pk", None)
        if not pk:
            raise ParseError(f"Request must have 'id' parameter", code='id')
        try:
            instance = view.queryset.get(pk=pk)
        except:
            raise NotFound(f"Equipment with id='{pk}' was not found", code='id')

        # "Мягкое" удаление
        instance.is_archived = True
        instance.save()

        # Формирование схемы ответа
        return_serializer = EquipmentDeleteSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok',
                'result': f'Equipment with id={pk} was deleted',
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class CreateUserService:
    """
        Сервис регистрации пользователя
    """

    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> UserCreateSerializer:
        """
            Регистрация пользователя
        """

        # Обработка входящих данных (валидация и сохранение)
        user_serializer = UserRegisterSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        instance = user_serializer.save()

        # Преобразование данных в стандартную схему для ответа
        user_serializer = UserSerializer(data=user_serializer.data, instance=instance)
        user_serializer.is_valid()

        # Формирование схемы ответа
        return_serializer = UserCreateSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok',
                'result': user_serializer.data,
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer


class GetUserDetailsService:
    """
        Сервис получения профиля пользователя
    """

    @staticmethod
    def execute(request: Request, view: ModelViewSet, *args, **kwargs) -> UserDetailsSerializer:
        """
            Получение профиля пользователя
        """

        # Обработка входящих данных (корректность ключа)
        pk = kwargs.get("pk", None)
        if not pk:
            raise ParseError(f"Request must have 'id' parameter", code='id')
        try:
            instance = view.queryset.get(pk=pk)
        except:
            raise NotFound(f"User with id='{pk}' was not found", code='id')

        # Преобразование данных в стандартную схему для ответа
        user_serializer = UserSerializer(
            data={
                'id': instance.id,
                'username': instance.username,
                'first_name': instance.first_name,
                'last_name': instance.last_name,
                'email': instance.email,
            },
            instance=instance
        )
        user_serializer.is_valid()

        # Формирование схемы ответа
        return_serializer = UserDetailsSerializer(
            data={
                'retCode': 0,
                'retMsg': 'Ok',
                'result': user_serializer.data,
                'retExtInfo': '',
                'retTime': int(time.time() * 10 ** 3)
            }
        )
        return_serializer.is_valid()

        return return_serializer
