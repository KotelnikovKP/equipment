from django.contrib import admin

from backend.models import EquipmentType, Equipment


class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'serial_number_mask', )
    list_display_links = ('id', )
    search_fields = ('id', 'name', 'serial_number_mask', )
    fields = ('id', 'name', 'serial_number_mask', )
    list_filter = ('id', 'name', 'serial_number_mask', )
    readonly_fields = ('id', )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(EquipmentType, EquipmentTypeAdmin)


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipment_type', 'serial_number', 'description',
                    'created_at', 'updated_at', 'is_archived', 'created_by', 'updated_by', )
    list_display_links = ('id', )
    search_fields = ('id', 'equipment_type', 'serial_number', 'description',
                     'created_at', 'updated_at', 'is_archived', 'created_by', 'updated_by', )
    fields = ('id', 'equipment_type', 'serial_number', 'description',
              'created_at', 'updated_at', 'is_archived', 'created_by', 'updated_by', )
    list_filter = ('id', 'equipment_type', 'serial_number', 'description',
                   'created_at', 'updated_at', 'is_archived', 'created_by', 'updated_by', )
    readonly_fields = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by', )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Equipment, EquipmentAdmin)


