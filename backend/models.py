from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Index
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class EquipmentType(models.Model):
    """
        Тип оборудования
    """
    name = models.CharField(max_length=255, verbose_name='Type name')
    serial_number_mask = models.CharField(max_length=50, verbose_name='Mask of serial numbers')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Type of equipment'
        verbose_name_plural = 'Type of equipment'
        ordering = ['id']
        indexes = (
            Index(fields=['name'], name='equ_typ__name__idx'),
        )
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='equ_typ__name__unq'
            ),
        ]


class Equipment(models.Model):
    """
        Оборудование
    """
    equipment_type = models.ForeignKey('EquipmentType', on_delete=models.PROTECT, related_name='equipments',
                                       verbose_name='Type of equipment')
    serial_number = models.CharField(max_length=50, verbose_name='Serial number of equipment')
    description = models.TextField(verbose_name='Description of equipment', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    is_archived = models.BooleanField(default=False, verbose_name='Is archived')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_by',
                                   null=True, blank=True, verbose_name='Created by')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='updated_by',
                                   null=True, blank=True, verbose_name='Updated by')

    class Meta:
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipment'
        ordering = ['is_archived', 'equipment_type', 'serial_number']
        indexes = (
            Index(
                fields=['is_archived', 'equipment_type', 'serial_number'],
                name='equ__type_serial_number__idx'
            ),
        )
        constraints = [
            models.UniqueConstraint(
                fields=['equipment_type', 'serial_number'],
                name='equ__type_serial_number__unq'
            ),
        ]


# Обработчик сигнала пост-сохранения модели User для генерации токена
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
