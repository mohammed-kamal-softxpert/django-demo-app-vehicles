from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Vehicle
from .serializers import VehicleSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'vehicles': reverse('vehicle-list', request=request, format=format)
    })

class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Vehicle.objects.filter(user_id=self.request.user.id)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    