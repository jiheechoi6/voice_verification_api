from rest_framework import serializers

class GetVoiceprintResponseSerializer(serializers.Serializer):
    voiceprint = serializers.ListField(child=serializers.FloatField(), help_text="Voiceprint extracted from stream (float array)")

class CompareVoiceprintResponseSerializer(serializers.Serializer):
    score = serializers.FloatField(help_text="Similarity score")

class CompareVoiceprintRequestSerializer(serializers.Serializer):
    voiceprint1 = serializers.ListField(child=serializers.FloatField(), help_text="voiceprint to compare (float array)")
    voiceprint2 = serializers.ListField(child=serializers.FloatField(), help_text="voiceprint to compare (float array)")
 