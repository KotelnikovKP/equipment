import re

from django.contrib.auth.models import User
from rest_framework import serializers, status

from backend.models import Equipment, EquipmentType


class SimpleResponseSerializer(serializers.Serializer):
    """
        Схема для ошибок
    """
    detail = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


simple_responses = {
    status.HTTP_400_BAD_REQUEST: SimpleResponseSerializer,
    status.HTTP_401_UNAUTHORIZED: SimpleResponseSerializer,
    status.HTTP_403_FORBIDDEN: SimpleResponseSerializer,
    status.HTTP_404_NOT_FOUND: SimpleResponseSerializer,
}


class BaseResponseSerializer(serializers.Serializer):
    """
        Схема базового ответа (от нее наследуются все схемы ответов)
    """
    retCode = serializers.IntegerField(help_text='Return code')
    retMsg = serializers.CharField(help_text='Return message')
    result = serializers.CharField(help_text='Result')
    retExtInfo = serializers.CharField(help_text='External result information')
    retTime = serializers.IntegerField(help_text='Return timestamp')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class PaginationListSerializer(serializers.Serializer):
    """
        Схема для дополнительной информации для пагинированого списка
    """
    count_items = serializers.IntegerField(help_text='Total number of items in result set')
    items_per_page = serializers.IntegerField(help_text='Number of items on one page')
    start_item_index = serializers.IntegerField(help_text='Index of start item on current page')
    end_item_index = serializers.IntegerField(help_text='Index of end item on current page')
    previous_page = serializers.IntegerField(help_text='Number of previous page (null if the current page is the last)')
    current_page = serializers.IntegerField(help_text='Number of current page')
    next_page = serializers.IntegerField(help_text='Number of next page (null if the current page is the first)')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class EquipmentTypeSerializer(serializers.ModelSerializer):
    """
        Стандартная схема типа оборудования (используется во всех ответах)
    """
    class Meta:
        model = EquipmentType
        fields = ('id', 'name', 'serial_number_mask', )


class EquipmentTypeRequestSerializer(serializers.ModelSerializer):
    """
        Схема типа оборудования во входящих запросах

        1. Валидация полей
        2. Зависимость обязательности полей от типа запроса (создание/изменение)
    """
    class Meta:
        model = EquipmentType
        fields = ('id', 'name', 'serial_number_mask', )
        read_only_fields = ['id']
        extra_kwargs = dict()

    def __init__(self, instance=None, data=None, **kwargs):
        super().__init__(instance, data, **kwargs)
        if instance:
            self.Meta.extra_kwargs['name'] = {'required': False}
            self.Meta.extra_kwargs['serial_number_mask'] = {'required': False}
        else:
            self.Meta.extra_kwargs = dict()

    @staticmethod
    def validate_serial_number_mask(value):
        """
            Валидация маски (значение только из определенных символов)
        """
        match = re.findall(r'[NAaXZ]+', value)
        if not match or match[0] != value:
            raise serializers.ValidationError(f"Serial number mask must consist of the characters"
                                              f" 'N', 'A', 'a', 'X', and 'Z' only",
                                              code='serial_number_mask')
        return value

    def validate_name(self, value):
        """
            Валидация имени (сохраняем только уникальные значения)
        """
        if self.instance:
            equipment_types = self.Meta.model.objects.filter(name__iexact=value).exclude(pk=self.instance.pk)
        else:
            equipment_types = self.Meta.model.objects.filter(name__iexact=value)
        if len(equipment_types) != 0:
            raise serializers.ValidationError(f"Equipment type with name='{value}' is already exist"
                                              f" (id={equipment_types[0].pk})",
                                              code='name')
        return value


class EquipmentTypeListSerializer(BaseResponseSerializer):
    """
        Схема ответа в списке типов оборудования
    """
    result = EquipmentTypeSerializer(many=True)
    retExtInfo = PaginationListSerializer()


class EquipmentTypeCreateUpdateSerializer(BaseResponseSerializer):
    """
        Схема ответа для создания и изменения типов оборудования
    """
    result = EquipmentTypeSerializer(many=False)


class EquipmentSerializer(serializers.ModelSerializer):
    """
        Стандартная схема оборудования (используется во всех ответах)
    """
    equipment_type_name = serializers.SerializerMethodField(help_text='Name of type of equipment')

    class Meta:
        model = Equipment
        fields = ('id', 'equipment_type', 'equipment_type_name', 'serial_number', 'description', )

    @staticmethod
    def get_equipment_type_name(obj) -> serializers.CharField:
        return obj.equipment_type.name if isinstance(obj, Equipment) else dict(obj)['equipment_type'].name


class EquipmentRequestSerializer(serializers.ModelSerializer):
    """
        Схема оборудования во входящих запросах

        1. Валидация полей
        2. Зависимость обязательности полей от типа запроса (создание/изменение)
    """
    PATTERNS = {
        'N': '[0-9]',
        'a': '[a-z]',
        'A': '[A-Z]',
        'X': '[A-Z0-9]',
        'Z': '[-_@]',
    }

    class Meta:
        model = Equipment
        fields = ('id', 'equipment_type', 'serial_number', 'description', )
        read_only_fields = ['id']
        extra_kwargs = dict()

    def __init__(self, instance=None, data=None, **kwargs):
        super().__init__(instance, data, **kwargs)
        if instance:
            self.Meta.extra_kwargs['equipment_type'] = {'required': False}
            self.Meta.extra_kwargs['serial_number'] = {'required': False}
            self.Meta.extra_kwargs['description'] = {'required': False}
        else:
            self.Meta.extra_kwargs = dict()

    def validate(self, data):
        """
            Валидация по типу и серийному номеру

            1. Проверка серийного номера по маске типа
            2. Уникальность тип + серийный номер
        """
        serial_number = dict(data).get('serial_number', None)
        equipment_type = dict(data).get('equipment_type', None)

        if self.instance:
            if not serial_number and not equipment_type:
                return data
            elif not serial_number:
                serial_number = self.instance.serial_number
            elif not equipment_type:
                equipment_type = self.instance.equipment_type
        else:
            if not serial_number or not equipment_type:
                return data
        serial_number_mask = EquipmentType.objects.get(pk=equipment_type.id).serial_number_mask

        pattern = ''.join([self.PATTERNS.get(c, ')АДМИН ПОСТАРАЛСЯ(') for c in serial_number_mask])
        match = re.findall(pattern, serial_number)
        if not match or match[0] != serial_number:
            raise serializers.ValidationError(f"Serial number '{serial_number}' does not match "
                                              f"'{equipment_type.name}' equipment type mask '{serial_number_mask}' "
                                              f"where 'N' is in [0-9], 'A' is in [A-Z], 'a' is in [a-z], "
                                              f"'X' is in [A-Z, 0-9], 'Z' is in [-_@]",
                                              code='serial_number')

        if self.instance:
            equipments = self.Meta.model.objects\
                .filter(equipment_type_id=equipment_type.id, serial_number=serial_number)\
                .exclude(pk=self.instance.pk)
        else:
            equipments = self.Meta.model.objects\
                .filter(equipment_type_id=equipment_type.id, serial_number=serial_number)
        if len(equipments) != 0:
            archive_flag = '-archived' if equipments[0].is_archived else ''
            raise serializers.ValidationError(f"Equipment with type '{equipment_type.name}' and "
                                              f"serial number '{serial_number}' is already exist"
                                              f" (id={equipments[0].pk}{archive_flag})",
                                              code='serial_number')

        return data


class EquipmentListSerializer(BaseResponseSerializer):
    """
        Схема ответа в списке оборудования
    """
    result = EquipmentSerializer(many=True)
    retExtInfo = PaginationListSerializer()


class EquipmentDetailsSerializer(BaseResponseSerializer):
    """
        Схема ответа в получении деталей заданного оборудования
    """
    result = EquipmentSerializer(many=False)


class ErrorCreateEquipmentSerializer(serializers.Serializer):
    """
        Схема ошибочной входящей записи оборудования (для ответа при создании оборудования)
    """
    index = serializers.IntegerField(help_text='Index of item in input set')
    error = serializers.CharField(help_text='Error message')
    data = serializers.CharField(help_text='Item data')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class InfoCreateEquipmentSerializer(serializers.Serializer):
    """
        Схема дополнительной информации для ответа при создании оборудования
    """
    count = serializers.IntegerField(help_text='Count of items in input set')
    saved = serializers.IntegerField(help_text='Count of saved items')
    failed = serializers.IntegerField(help_text='Count of failed items')
    errors = ErrorCreateEquipmentSerializer(many=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class EquipmentCreateSerializer(BaseResponseSerializer):
    """
        Схема ответа для создания оборудования
    """
    result = EquipmentSerializer(many=True)
    retExtInfo = InfoCreateEquipmentSerializer(many=False)


class EquipmentUpdateSerializer(BaseResponseSerializer):
    """
        Схема ответа для изменения оборудования
    """
    result = EquipmentSerializer(many=False)


class EquipmentDeleteSerializer(BaseResponseSerializer):
    """
        Схема ответа для удаления оборудования
    """
    pass


class UserSerializer(serializers.ModelSerializer):
    """
        Стандартная схема пользователя (используется во всех ответах)
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', )


class UserRegisterSerializer(serializers.ModelSerializer):
    """
        Схема пользователя во входящих запросах (регистрация)

        1. Валидация полей
        2. Проверка совпадения паролей
    """
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "password2", )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class UserCreateSerializer(BaseResponseSerializer):
    """
        Схема ответа для создания пользователя
    """
    result = UserSerializer(many=False)


class UserDetailsSerializer(serializers.Serializer):
    """
        Схема ответа в получении профиля пользователя
    """

    user = UserSerializer(many=False)


