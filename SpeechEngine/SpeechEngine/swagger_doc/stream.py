from drf_yasg import openapi
from SpeechEngine.serializers.stream import *
from SpeechEngine.swagger_doc.generic import GenericResponse
from SpeechEngine.serializers.voiceprint import *

class HttpStreamDataViewSetSwagger():
    start = {
        "operation_description":
        """
        Starts an http stream and returns a unique uuid
        """,
        "operation_summary": "Starts stream.",
        "responses": {
            200: openapi.Response("Stream creation was successful. Returns uuid of the new stream",
                                    schema=CreateStreamResponseSerializer()),
            500: GenericResponse.swagger_500_response,
        },
        "tags": ["Streams"]
    }

    upload = {
        "operation_description":
        """
        Sends audio data to existing stream. wav file converted to base64 string (latin-1) is accepted.
        Audio data is lost when stream is deleted.
        """,
        "operation_summary": "Uploads data to stream",
        "request_body": UploadRequestSerializer,
        "responses": {
            200: openapi.Response("Audio data is successfully uploaded."),
            400: GenericResponse.swagger_400_response,
            404: GenericResponse.swagger_404_response,
            500: GenericResponse.swagger_500_response,
            512: openapi.Response("Something went wrong connecting to Redis database")
        },
        "tags": ["Streams"]
    }

    delete = {
        "operation_description":
        """
        Deletes stream with the given uuid
        """,
        "operation_summary": "Deletes stream",
        "responses": {
            200: openapi.Response("Stream successfully deleted."),
            400: GenericResponse.swagger_400_response,
            404: GenericResponse.swagger_404_response,
            500: GenericResponse.swagger_500_response,
            512: openapi.Response("Something went wrong connecting to Redis database")
        },
        "tags": ["Streams"]
    }

    get_all_streams = {
        "operation_description":
        """
        Fetches uuid list of all ongoing stream(s)
        """,
        "operation_summary": "Get all stream uuids",
        "responses": {
            200: openapi.Response("Successfully returned uuid list"),
            500: GenericResponse.swagger_500_response,
        },
        "tags": ["Streams"]
    }

    get_voiceprint = {
        "operation_description":
        """
        Gets voiceprint of a stream in float array format. 
        """,
        "operation_summary": "Gets voiceprint of a stream",
        "responses": {
            200: openapi.Response("Successfully obtained voiceprint of a stream",
                                    schema=GetVoiceprintResponseSerializer()),
            404: GenericResponse.swagger_404_response,
            500: GenericResponse.swagger_500_response,
        },
        "tags": ["Voicprint"]
    }

    compare = {
        "operation_description":
        """
        Compares two voiceprints and returns similarity score
        """,
        "operation_summary": "Gives similarity score of two voiceprints",
        "request_body": CompareVoiceprintRequestSerializer,
        "responses": {
            200: openapi.Response("Successfully calculated similarity score of voiceprints",
                                    schema=CompareVoiceprintResponseSerializer()),
            500: GenericResponse.swagger_500_response,
        },
        "tags": ["Voicprint"]
    }

    