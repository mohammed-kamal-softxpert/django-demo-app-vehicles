from typing import Any
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status
from .serializers import VehicleSerializer
from .repositories import VehicleRepository

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'vehicles': reverse('vehicle-list', request=request, format=format)
    })

class VehicleViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._repo = VehicleRepository()
    
    def list(self, request):
        page_filters = {key: request.query_params.get(key, None) for key in ['page', 'per_page']}
        vehicles = self._repo.get_many_vehicles(user_id=request.user.id, **page_filters)
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = VehicleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        vehicle = self._repo.get_one_vehicle(id=pk, user_id=request.user.id)
        if vehicle:
            serializer = VehicleSerializer(vehicle)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        vehicle = self._repo.get_one_vehicle(id=pk, user_id=request.user.id)
        if vehicle:
            serializer = VehicleSerializer(instance=vehicle, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        vehicle = self._repo.get_one_vehicle(id=pk, user_id=request.user.id)
        if vehicle:
            serializer = VehicleSerializer(instance=vehicle, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        vehicle = self._repo.get_one_vehicle(id=pk, user_id=request.user.id)
        if vehicle:
            vehicle.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    