from rest_framework import serializers

class CreateStreamResponseSerializer(serializers.Serializer):
    uuid = serializers.CharField(help_text="Stream uuid")

class UploadRequestSerializer(serializers.Serializer):
    data = serializers.CharField(help_text="Base64 audio string (latin-1 encoding)")