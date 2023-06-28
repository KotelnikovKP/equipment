from django_filters import rest_framework as filters

from backend.models import EquipmentType, Equipment


def filter_name(queryset, name, value):
    return queryset.filter(name__icontains=value)


def filter_serial_number_mask(queryset, name, value):
    return queryset.filter(serial_number_mask__contains=value)


class EquipmentTypeFilter(filters.FilterSet):
    """
        Фильтры для списка типов оборудования

        Оба поля (name, serial_number_mask) с фильтрацией по вхождению
    """
    name = \
        filters.CharFilter(label='Equipment type name for result set filtering (by content case insensitive).',
                           method=filter_name)
    serial_number_mask = \
        filters.CharFilter(label='Serial number mask for result set filtering (by content case sensitive).',
                           method=filter_serial_number_mask)

    class Meta:
        model = EquipmentType
        fields = ['name', 'serial_number_mask']


def filter_equipment_type(queryset, name, value):
    return queryset.filter(equipment_type__name__icontains=value)


def filter_serial_number(queryset, name, value):
    return queryset.filter(serial_number__icontains=value)


def filter_description(queryset, name, value):
    return queryset.filter(description__icontains=value)


class EquipmentFilter(filters.FilterSet):
    """
        Фильтры для списка оборудования

        Поля (equipment_type_name, serial_number, description) с фильтрацией по вхождению
    """
    equipment_type_name = \
        filters.CharFilter(label='Equipment type name for result set filtering (by content case insensitive).',
                           method=filter_equipment_type)
    serial_number = \
        filters.CharFilter(label='Serial number for result set filtering (by content case insensitive).',
                           method=filter_serial_number)
    description = \
        filters.CharFilter(label='Description for result set filtering (by content case insensitive).',
                           method=filter_description)

    class Meta:
        model = Equipment
        fields = ['equipment_type_name', 'serial_number', 'description']

