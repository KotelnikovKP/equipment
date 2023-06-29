"""
    Контроллеры

    Для генерации OpenAPI спецификаций используется drf_spectacular
    Вся обработка перенесена в сервисный слой
    Схемы запросов и ответов посредством сериализаторов
"""
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from backend.filters import EquipmentTypeFilter, EquipmentFilter
from backend.helpers import expand_dict
from backend.models import Equipment, EquipmentType
from backend.permissons import EquipmentTypePermission
from backend.serializers import EquipmentSerializer, EquipmentTypeSerializer, EquipmentTypeListSerializer, \
    EquipmentListSerializer, simple_responses, EquipmentTypeCreateUpdateSerializer, EquipmentDetailsSerializer, \
    EquipmentRequestSerializer, EquipmentTypeRequestSerializer, EquipmentUpdateSerializer, EquipmentCreateSerializer, \
    EquipmentDeleteSerializer, UserRegisterSerializer, UserSerializer, UserCreateSerializer, UserDetailsSerializer
from backend.services import GetEquipmentTypeListService, GetEquipmentListService, CreateEquipmentTypeService, \
    UpdateEquipmentTypeService, GetEquipmentDetailsService, UpdateEquipmentService, CreateEquipmentService, \
    DeleteEquipmentService, CreateUserService, GetUserDetailsService


@extend_schema(tags=['Type of equipment'])
class EquipmentTypeViewSet(ModelViewSet):
    """
        Методы для типов оборудования
    """

    permission_classes = (EquipmentTypePermission, )
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
        return Response(equipment_list.initial_data)

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


@extend_schema(tags=['Auth'])
@extend_schema_view(
    post=extend_schema(
        summary='Authorize user and retrieve an access token',
        description='Authorize user and retrieve a bearer token, bla-bla-bla...',
    ),
)
class EquipmentCustomTokenObtainPairView(TokenObtainPairView):
    """
        Класс для авторизации и получения access токена (используем стандартный DFR класс)
    """
    pass


@extend_schema(tags=['Auth'])
@extend_schema_view(
    post=extend_schema(
        summary='Retrieve a refresh token',
        description='Retrieve a refresh token, bla-bla-bla...',
    ),
)
class EquipmentCustomTokenRefreshView(TokenRefreshView):
    """
        Класс для получения refresh токена (используем стандартный DFR класс)
    """
    pass


@extend_schema(tags=['Auth'])
class UserRegisterViewSet(ModelViewSet):
    permission_classes = (AllowAny, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        summary='Register user',
        description='Register user, bla-bla-bla...',
        request=UserRegisterSerializer(many=False),
        responses=expand_dict({status.HTTP_200_OK: UserCreateSerializer, }, simple_responses),
    )
    def create(self, request, *args, **kwargs):
        """
            Регистрация пользователя
        """
        user_create = CreateUserService.execute(request, self, *args, **kwargs)
        return Response(user_create.data)

    @extend_schema(
        summary='Retrieve user profile',
        description='Retrieve user profile, bla-bla-bla...',
        responses=expand_dict({status.HTTP_200_OK: UserDetailsSerializer, }, simple_responses),
    )
    def retrieve(self, request, *args, **kwargs):
        """
            Получение профиля пользователя
        """
        user_details = GetUserDetailsService.execute(request, self, *args, **kwargs)
        return Response(user_details.data)
