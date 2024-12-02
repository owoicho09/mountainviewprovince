from .models import Hostel, Block, Room, HostelType
from rest_framework import serializers


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['id', 'name']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_number']

class HostelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelType
        fields = '__all__'


class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = ['hid', 'name']  # Add other relevant fields as needed
