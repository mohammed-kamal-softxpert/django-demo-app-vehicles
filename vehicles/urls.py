from django.urls import path
from rest_framework import renderers
from .views import VehicleViewSet, api_root

vehcile_list = VehicleViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

vehicle_detail = VehicleViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', api_root),
    path('vehicles/', vehcile_list, name='vehicle-list'),
    path('vehicle/<int:pk>/', vehicle_detail, name='vehicle-detail')
]