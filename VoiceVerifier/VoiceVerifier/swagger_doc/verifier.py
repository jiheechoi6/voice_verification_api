from drf_yasg import openapi
from VoiceVerifier.serializers.streams import CreateStreamResponseSerializer, UploadRequestSerializer
from .generic import GenericResponse
from VoiceVerifier.serializers.verifier import *

class VerifierViewSetSwagger():
    enroll = {
        "operation_description":
        """
        Enrolls user by external_id. The voiceprint extracted from the stream indicated in body will be stored.
        """,
        "operation_summary": "Enroll User",
        "request_body": EnrollRequestSerializer,
        "responses": {
            200: openapi.Response("Enrollment was successful"),
            400: openapi.Response("external_id or uuid was not passed over"),
            404: openapi.Response("Stream with this uuid doesn't exists"),
            409: openapi.Response("user_id already exists"),
            500: GenericResponse.swagger_500_response,
        },
        "tags": ["Speaker verification"]
    }

    verify = {
        "operation_description":
        """
        Gives similarity score of current audio data in a stream with a previously enrolled voiceprint under external_id.
        """,
        "operation_summary": "Gives similarity score",
        "request_body": VerifyRequestSerializer,
        "responses": {
            200: openapi.Response("Successfully obtained similarity score",
                                    schema=VerifyResponseSerializer()),
            460: openapi.Response("A user with this external ID doesn't exist"),
            461: openapi.Response("A stream with this uuid doesn't exist"),
            500: GenericResponse.swagger_500_response,
        },
        "tags": ["Speaker verification"]
    }

    get_voiceprint = {
        "operation_description":
        """
        Fetches enrolled voiceprint of a user by external ID
        """,
        "operation_summary": "Get voiceprint by ID",
        "responses": {
            200: openapi.Response("Successfully obtained voiceprint",
                                    schema=GetVoiceprintResponseSerializer()),
            460: openapi.Response("No user enrolled with this external ID"),
            500: GenericResponse.swagger_500_response,
        },
        "tags": ["Speaker verification"]
    }

    list_enrollements = {
        "operation_description":
        """
        List all external IDs of users who enrolled their voiceprints
        """,
        "operation_summary": "List all enrolled user IDs",
        "responses": {
            200: openapi.Response("Successfully obtained ID list",
                                    schema=GetVoiceprintResponseSerializer()),
            500: GenericResponse.swagger_500_response,
        },
        "tags": ["Speaker verification"]
    }

    delete_all_enrollment = {
        "operation_description":
        """
        Delete all voiceprint enrollments
        """,
        "operation_summary": "Delete all enrollment ",
        "responses": {
            200: openapi.Response("Successfully deleted all enrollments",
                                    schema=DeleteAllResponseSerializer()),
            500: GenericResponse.swagger_500_response,
        },
        "tags": ["Speaker verification"]
    }

    delete_enrollment = {
        "operation_description":
        """
        Delete a voiceprint enrollment by external ID 
        """,
        "operation_summary": "Delete enrollment by ID ",
        "responses": {
            200: openapi.Response("Successfully deleted enrollment"),
            400: openapi.Response("A user with this external ID was not found"),
            500: GenericResponse.swagger_500_response,
        },
        "tags": ["Speaker verification"]
    }
