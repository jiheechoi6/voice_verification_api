import django
from rest_framework import serializers

class EnrollRequestSerializer(serializers.Serializer):
    uuid = serializers.CharField(help_text="Stream uuid")
    external_id = serializers.CharField(help_text="External ID")

class VerifyRequestSerializer(serializers.Serializer):
    uuid = serializers.CharField(help_text="Stream uuid")
    external_id = serializers.CharField(help_text="External ID of the user being verified against")
    
class GetVoiceprintResponseSerializer(serializers.Serializer):
    voiceprint = serializers.ListField(child=serializers.FloatField())

class ListEnrollmentsResponseSerializer(serializers.Serializer):
    ids = serializers.ListField("External ID list of all enrolled users")

class VerifyResponseSerializer(serializers.Serializer):
    score = serializers.FloatField(help_text="Similarity score")

class DeleteAllResponseSerializer(serializers.Serializer):
    delete_count = serializers.FloatField(help_text = "Number of deleted user")

