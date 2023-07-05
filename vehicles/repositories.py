from django.db.models import Q
from ._base_repo import BaseRepo
from .models import Vehicle

class VehicleRepository(BaseRepo):
    def __init__(self):
        super().__init__(Vehicle)
        
    def get_one_vehicle(self, id, user_id):
        return self._get_single(Q(id=id, user_id=user_id))
    
    def get_many_vehicles(self, user_id, page = 1, per_page = 10, sort_by = 'id', sort_direction = 'asc'):
        return self._get_many(Q(user_id=user_id), dict(
            page=page if page else 1,
            per_page=per_page if per_page else 10,
            sort_by=sort_by if sort_by else 'id',
            sort_direction=sort_direction if sort_direction else 'asc'
        ))
    
    def create_vehicle(self, **validated_data):
        return self.build_query().create(**validated_data)
    
    def update_vehicle(self, id, **validated_data):
        instance = self.get_one_vehicle(id, validated_data['user_id'])
        instance.vin = validated_data['vin']
        instance.model = validated_data['model']
        instance.make = validated_data['make']
        instance.is_online = validated_data['is_online']
        instance.created = validated_data['created']
        instance.save()
        return instance