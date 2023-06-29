from django.urls import path, include

from backend.routers import EquipmentRouter, EquipmentTypeRouter, UserRouter
from backend.views import EquipmentTypeViewSet, EquipmentViewSet, UserRegisterViewSet, \
    EquipmentCustomTokenObtainPairView, EquipmentCustomTokenRefreshView

equipment_router = EquipmentRouter()
equipment_router.register(r'equipment', EquipmentViewSet)
equipment_type_router = EquipmentTypeRouter()
equipment_type_router.register(r'equipment-type', EquipmentTypeViewSet)
user_router = UserRouter()
user_router.register(r'user', UserRegisterViewSet)

urlpatterns = [
    path('api/', include(equipment_router.urls)),
    path('api/', include(equipment_type_router.urls)),
    path('api/', include(user_router.urls)),
    path("api/user/login", EquipmentCustomTokenObtainPairView.as_view(), name="token"),
    path("api/user/refresh_token", EquipmentCustomTokenRefreshView.as_view(), name="refresh_token"),
]
