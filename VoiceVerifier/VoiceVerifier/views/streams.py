from django.http.response import HttpResponse, JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.parsers import *

import requests
import json

# swagger
from drf_yasg.utils import swagger_auto_schema
from VoiceVerifier.swagger_doc.stream import HttpStreamViewSetSwagger

SPEECHBRAIN_STREAM_BASE_URL = "http://speechbrain:3000/http_stream"
UPLOAD_TO_STREAM_URL = SPEECHBRAIN_STREAM_BASE_URL + "/{uuid}"
DELETE_STREAM_URL = SPEECHBRAIN_STREAM_BASE_URL + "/{uuid}"
# GET_VP_URL = SPEECHBRAIN_BASE_URL + "http_stream/voiceprint/{uuid}"
# COMPARE_VP_URL = SPEECHBRAIN_BASE_URL + "speakeridt/compare_vp"

class HttpStreamViewSet(ViewSet):
    @swagger_auto_schema(**HttpStreamViewSetSwagger.start)
    def start_stream(self, request, *args, **kwargs):
        '''
        200: success
        500: Internal Server Error
        '''
        resp = requests.post(SPEECHBRAIN_STREAM_BASE_URL)
        stat = resp.status_code
        if stat != 200:
            return HttpResponse(status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # if start stream was successful
        new_uuid = resp.json()["uuid"]
        return JsonResponse({"uuid": new_uuid}, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(**HttpStreamViewSetSwagger.upload)
    def upload_stream_data(self, request, *arg, **kwargs):
        '''
        200: upload successful
        400: data was not passed in request body
        404: Stream with this uuid doesn't exists
        500: internal server error
        '''
        uuid = kwargs['uuid']

        # data was not passed over in body
        if not "data" in request.data:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data["data"]
        
        res = requests.post(UPLOAD_TO_STREAM_URL.format(uuid=uuid), data=json.dumps({"data":data}), headers={'Content-Type':'application/json'})

        if res.status_code == 200:
            return HttpResponse(status=status.HTTP_200_OK)
        elif res.status_code == 404:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        else:
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(**HttpStreamViewSetSwagger.get_streams)
    def get_all_streams(self, request, *arg, **kwargs):
        '''
        200: successfully returned uuid list
        500: internal server error'''
        
        res = requests.get(SPEECHBRAIN_STREAM_BASE_URL)

        if res.status_code == 200:
            return JsonResponse(res.json(), status=200)
        else:
            return HttpResponse(status=500)
