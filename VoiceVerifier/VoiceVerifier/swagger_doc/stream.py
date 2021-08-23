from drf_yasg import openapi
from VoiceVerifier.serializers.streams import CreateStreamResponseSerializer, UploadRequestSerializer
from .generic import GenericResponse

class HttpStreamViewSetSwagger():
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
        Sends audio data to existing stream. wav data converted to base64 string (latin-1) is accepted
        Audio data is lost when stream is deleted.
        """,
        "operation_summary": "Uploads data to stream",
        "request_body": UploadRequestSerializer,
        "responses": {
            200: openapi.Response("Audio data is successfully uploaded."),
            400: GenericResponse.swagger_400_response,
            404: GenericResponse.swagger_404_response,
            500: GenericResponse.swagger_500_response,
        },
        "tags": ["Streams"]
    }

    get_streams = {
        "operation_description":
        """
        Gets all stream uuids
        """,
        "operation_summary": "Gets all streams",
        "responses": {
            200: openapi.Response("Successfully fetched all stream uuids."),
            500: GenericResponse.swagger_500_response,
        },
        "tags": ["Streams"]
    }