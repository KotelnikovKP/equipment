from django.db.models import Q
from django_filters import rest_framework as filters

from backend.models import EquipmentType, Equipment


def filter_equipment_type_q(queryset, name, value):
    return queryset.filter(Q(name__icontains=value) | Q(serial_number_mask__icontains=value))


def filter_equipment_type_name(queryset, name, value):
    return queryset.filter(name__icontains=value)


def filter_equipment_type_serial_number_mask(queryset, name, value):
    return queryset.filter(serial_number_mask__icontains=value)


class EquipmentTypeFilter(filters.FilterSet):
    """
        Фильтры для списка типов оборудования

        Общее поле q и оба поля (name, serial_number_mask) с фильтрацией по вхождению
    """
    q = \
        filters.CharFilter(label='Equipment type name or serial number mask for result set filtering '
                                 '(by content case insensitive).',
                           method=filter_equipment_type_q)
    name = \
        filters.CharFilter(label='Equipment type name for result set filtering (by content case insensitive).',
                           method=filter_equipment_type_name)
    serial_number_mask = \
        filters.CharFilter(label='Serial number mask for result set filtering (by content case insensitive).',
                           method=filter_equipment_type_serial_number_mask)

    class Meta:
        model = EquipmentType
        fields = ['name', 'serial_number_mask']


def filter_equipment_q(queryset, name, value):
    return queryset.filter(Q(equipment_type__name__icontains=value) | Q(serial_number__icontains=value) |
                           Q(description__icontains=value))


def filter_equipment_equipment_type(queryset, name, value):
    return queryset.filter(equipment_type__name__icontains=value)


def filter_equipment_serial_number(queryset, name, value):
    return queryset.filter(serial_number__icontains=value)


def filter_equipment_description(queryset, name, value):
    return queryset.filter(description__icontains=value)


class EquipmentFilter(filters.FilterSet):
    """
        Фильтры для списка оборудования

        Общее поле q и поля (equipment_type_name, serial_number, description) с фильтрацией по вхождению
    """
    q = \
        filters.CharFilter(label='Equipment type name or serial number or description for result set filtering '
                                 '(by content case insensitive).',
                           method=filter_equipment_q)
    equipment_type_name = \
        filters.CharFilter(label='Equipment type name for result set filtering (by content case insensitive).',
                           method=filter_equipment_equipment_type)
    serial_number = \
        filters.CharFilter(label='Serial number for result set filtering (by content case insensitive).',
                           method=filter_equipment_serial_number)
    description = \
        filters.CharFilter(label='Description for result set filtering (by content case insensitive).',
                           method=filter_equipment_description)

    class Meta:
        model = Equipment
        fields = ['equipment_type_name', 'serial_number', 'description']

