from rest_framework import serializers
from rest_framework.fields import empty
from .repositories import VehicleRepository

class VehicleSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    vin = serializers.IntegerField(required=True)
    model = serializers.CharField(max_length=20, allow_blank=True)
    make = serializers.CharField(max_length=20, allow_blank=True)
    is_online = serializers.BooleanField()
    created = serializers.DateTimeField(required=False)
    
    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        self._repo = VehicleRepository()
    
    def _getCurrentUser(self):
        request = self.context.get('request', None)
        if request:
            return request.user

    def create(self, validated_data):
        user = self._getCurrentUser()
        return self._repo.create_vehicle(**validated_data, user_id=user.id)
    
    def update(self, instance, validated_data):
        return self._repo.update_vehicle(
            id=instance.id,
            user_id=instance.user_id,
            vin=validated_data.get('vin', instance.vin),
            model=validated_data.get('model', instance.model),
            make=validated_data.get('make', instance.make),
            is_online=validated_data.get('is_online', instance.is_online),
            created=validated_data.get('created', instance.created)
        )
        
    def validate_vin(self, value):
        # Check if the vin number is a valid integer and is a 4 digit
        if not isinstance(value, int):
            raise serializers.ValidationError('Vin is not a number')
        elif len(str(value)) != 4:
            raise serializers.ValidationError('Vin is not a valid vin number')
        return value