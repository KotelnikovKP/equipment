"""
    Контроллеры

    Для генерации OpenAPI спецификаций используется drf_spectacular
    Вся обработка перенесена в сервисный слой
    Схемы запросов и ответов посредством сериализаторов
"""

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from backend.authentication import BearerAuthentication
from backend.filters import EquipmentTypeFilter, EquipmentFilter
from backend.helpers import expand_dict
from backend.models import Equipment, EquipmentType
from backend.permissons import EquipmentTypePermission
from backend.serializers import EquipmentSerializer, EquipmentTypeSerializer, EquipmentTypeListSerializer, \
    EquipmentListSerializer, simple_responses, EquipmentTypeCreateUpdateSerializer, EquipmentDetailsSerializer, \
    EquipmentRequestSerializer, EquipmentTypeRequestSerializer, EquipmentUpdateSerializer, EquipmentCreateSerializer, \
    EquipmentDeleteSerializer
from backend.services import GetEquipmentTypeListService, GetEquipmentListService, CreateEquipmentTypeService, \
    UpdateEquipmentTypeService, GetEquipmentDetailsService, UpdateEquipmentService, CreateEquipmentService, \
    DeleteEquipmentService


@extend_schema(tags=['Login'])
@extend_schema_view(
    post=extend_schema(
        summary='Authorize user and retrieve a bearer token',
        description='Authorize user and retrieve a bearer token, bla-bla-bla...',
    ),
)
class EquipmentCustomAuthToken(ObtainAuthToken):
    """
        Класс для авторизации и получения токена (используем стандартный DFR класс)
    """
    pass


@extend_schema(tags=['Type of equipment'])
class EquipmentTypeViewSet(ModelViewSet):
    """
        Методы для типов оборудования
    """

    permission_classes = (EquipmentTypePermission, )
    authentication_classes = (BearerAuthentication, )
    queryset = EquipmentType.objects.all()
    serializer_class = EquipmentTypeSerializer
    filterset_class = EquipmentTypeFilter

    @extend_schema(
        summary='Retrieve paginated and filtered list of type of equipments',
        description='Retrieve paginated and filtered list of type of equipments, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: EquipmentTypeListSerializer, }, simple_responses),
    )
    def list(self, request: Request, *args, **kwargs):
        """
            Получение пагинированого и отфильтрованного списка типов оборудования
        """
        equipment_type_list = GetEquipmentTypeListService.execute(request, self, *args, **kwargs)
        return Response(equipment_type_list.data)

    @extend_schema(
        summary='Create type of equipments (administrator only permission)',
        description='Create type of equipments (administrator access only), bla-bla-bla...',
        request=EquipmentTypeRequestSerializer,
        responses=expand_dict({status.HTTP_200_OK: EquipmentTypeCreateUpdateSerializer, }, simple_responses),
    )
    def create(self, request: Request, *args, **kwargs):
        """
            Создание типа оборудования
        """
        equipment_type_create = CreateEquipmentTypeService.execute(request, self, *args, **kwargs)
        return Response(equipment_type_create.data)

    @extend_schema(
        summary='Update type of equipments (administrator only permission)',
        description='Update type of equipments (administrator access only), bla-bla-bla...',
        request=EquipmentTypeRequestSerializer,
        responses=expand_dict({status.HTTP_200_OK: EquipmentTypeCreateUpdateSerializer, }, simple_responses),
    )
    def update(self, request: Request, *args, **kwargs):
        """
            Изменения типа оборудования
        """
        equipment_type_update = UpdateEquipmentTypeService.execute(request, self, *args, **kwargs)
        return Response(equipment_type_update.data)


@extend_schema(tags=['Equipment'])
class EquipmentViewSet(ModelViewSet):
    """
        Методы для оборудования
    """

    permission_classes = (IsAuthenticated, )
    authentication_classes = (BearerAuthentication, )
    queryset = Equipment.objects.select_related('equipment_type').filter(is_archived=False)
    serializer_class = EquipmentSerializer
    filterset_class = EquipmentFilter

    @extend_schema(
        summary='Retrieve paginated and filtered list of equipments',
        description='Retrieve paginated and filtered list of equipments, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: EquipmentListSerializer, }, simple_responses),
    )
    def list(self, request, *args, **kwargs):
        """
            Получение пагинированого и отфильтрованного списка оборудования
        """
        equipment_list = GetEquipmentListService.execute(request, self, *args, **kwargs)
        return Response(equipment_list.data)

    @extend_schema(
        summary='Create equipment',
        description='Create equipment, bla-bla-bla...',
        request=EquipmentRequestSerializer(many=True),
        responses=expand_dict({status.HTTP_200_OK: EquipmentCreateSerializer, }, simple_responses),
    )
    def create(self, request, *args, **kwargs):
        """
            Создание оборудования
        """
        equipment_create = CreateEquipmentService.execute(request, self, *args, **kwargs)
        return Response(equipment_create.initial_data)

    @extend_schema(
        summary='Retrieve equipment details',
        description='Retrieve equipment details, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: EquipmentDetailsSerializer, }, simple_responses),
    )
    def retrieve(self, request, *args, **kwargs):
        """
            Получение детальной информации по заданному оборудованию
        """
        equipment_details = GetEquipmentDetailsService.execute(request, self, *args, **kwargs)
        return Response(equipment_details.data)

    @extend_schema(
        summary='Update equipment',
        description='Update equipment, bla-bla-bla...',
        request=EquipmentRequestSerializer,
        responses=expand_dict({status.HTTP_200_OK: EquipmentUpdateSerializer, }, simple_responses),
    )
    def update(self, request, *args, **kwargs):
        """
            Изменение оборудования
        """
        equipment_update = UpdateEquipmentService.execute(request, self, *args, **kwargs)
        return Response(equipment_update.data)

    @extend_schema(
        summary='Delete equipment',
        description='Delete equipment, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: EquipmentDeleteSerializer, }, simple_responses),
    )
    def destroy(self, request,  *args, **kwargs):
        """
            Удаление оборудования
        """
        equipment_delete = DeleteEquipmentService.execute(request, self, *args, **kwargs)
        return Response(equipment_delete.data)


