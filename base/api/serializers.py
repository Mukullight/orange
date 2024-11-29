from rest_framework.serializers import ModelSerializer
from base.models import Room
from rest_framework import serializers

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


