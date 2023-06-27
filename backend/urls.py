from django.urls import path, include

from backend.routers import EquipmentRouter, EquipmentTypeRouter
from backend.views import EquipmentCustomAuthToken, EquipmentTypeViewSet, EquipmentViewSet

equipment_router = EquipmentRouter()
equipment_router.register(r'equipment', EquipmentViewSet)
equipment_type_router = EquipmentTypeRouter()
equipment_type_router.register(r'equipment-type', EquipmentTypeViewSet)

urlpatterns = [
    path('api/', include(equipment_router.urls)),
    path('api/', include(equipment_type_router.urls)),
    path('api/user/login', EquipmentCustomAuthToken.as_view()),
]
