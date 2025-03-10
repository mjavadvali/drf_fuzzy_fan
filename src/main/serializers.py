from rest_framework import serializers

class ServerDataSerializer(serializers.Serializer):
    serverroom_temperature = serializers.CharField()
    softwareroom_temperature = serializers.CharField()
    serverroom_humidity = serializers.CharField()