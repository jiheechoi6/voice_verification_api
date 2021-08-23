import django
from rest_framework import serializers
from VoiceVerifier.models.voiceprint import Voiceprint

class VoiceprintSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    voiceprint = serializers.CharField()
    date = serializers.DateTimeField()

    def create(self, validated_data):
        return Voiceprint.objects.create(username=validated_data["username"], voiceprint=validated_data["voiceprint"])

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.voiceprint = validated_data.get('voiceprint', instance.voiceprint)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance

