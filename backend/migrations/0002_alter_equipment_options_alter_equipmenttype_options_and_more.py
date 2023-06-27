# Generated by Django 4.2.2 on 2023-06-25 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipment',
            options={'ordering': ['is_archived', 'equipment_type', 'serial_number'], 'verbose_name': 'Equipment', 'verbose_name_plural': 'Equipment'},
        ),
        migrations.AlterModelOptions(
            name='equipmenttype',
            options={'ordering': ['id'], 'verbose_name': 'Type of equipment', 'verbose_name_plural': 'Type of equipment'},
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='create_at',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='create_by',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='update_at',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='update_by',
        ),
        migrations.AddField(
            model_name='equipment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='equipment',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_by', to=settings.AUTH_USER_MODEL, verbose_name='Updated by'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='equipment_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipments', to='backend.equipmenttype', verbose_name='Type of equipment'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='is_archived',
            field=models.BooleanField(default=False, verbose_name='Is archived'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='serial_number',
            field=models.CharField(max_length=50, verbose_name='Serial number'),
        ),
        migrations.AlterField(
            model_name='equipmenttype',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Type name'),
        ),
        migrations.AlterField(
            model_name='equipmenttype',
            name='serial_number_mask',
            field=models.CharField(max_length=50, verbose_name='Serial number mask'),
        ),
    ]
