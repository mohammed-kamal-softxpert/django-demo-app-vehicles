from django.db import models


class Vehicle(models.Model):
    vin = models.IntegerField()
    model = models.CharField(max_length=20, blank=True, default='')
    make = models.CharField(max_length=20, blank=True, default='')
    is_online = models.BooleanField(blank=True, default=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Vehicle with id={self.id} vin={self.vin}, model={self.model}, make={self.make}, is_online={self.is_online}, created={self.created}, user_id={self.user.id}'