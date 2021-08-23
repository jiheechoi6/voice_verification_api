from django.http.response import HttpResponse, JsonResponse
from django.db import IntegrityError
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.parsers import *
from django.conf import settings
import logging

import requests
import json
import numpy as np
import base64

# model
from VoiceVerifier.models.voiceprint import Voiceprint
from VoiceVerifier.serializers.voiceprint import VoiceprintSerializer

# swagger
from drf_yasg.utils import swagger_auto_schema
from VoiceVerifier.swagger_doc.verifier import VerifierViewSetSwagger

SPEECHBRAIN_BASE_URL = "http://speechbrain:3000/"
GET_VP_URL = SPEECHBRAIN_BASE_URL + "http_stream/voiceprint/{uuid}"
COMPARE_VP_URL = SPEECHBRAIN_BASE_URL + "speakeridt/compare_vp"

activitylogger = logging.getLogger("enrollverify")

class VerifierViewSet(ViewSet):
    @swagger_auto_schema(**VerifierViewSetSwagger.enroll)
    def enroll(self, request, *args, **kwargs):
        '''
        200: ok
        400: external_id or uuid was not passed over
        404: Stream with this uuid doesn't exists
        409: user_id already exists
        500: Internal server error
        '''
        # check if all required info is passed
        if not "external_id" in request.data or not "uuid" in request.data:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
         
        user_id = request.data["external_id"]
        uuid = request.data["uuid"]

        # get voiceprint of stream with the uuid
        res = requests.get(GET_VP_URL.format(uuid=uuid))
        stat = res.status_code
        if stat == 200:
            voiceprint = res.json()['voiceprint']
        elif stat == 404:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        else:
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # save voiceprint to db
        voiceprintstr = base64.b64encode(np.array(voiceprint)).decode('utf-8')  # stringify voiceprint
        newVP = Voiceprint(username=user_id, voiceprint=voiceprintstr)
        try: 
            newVP.save()
        except IntegrityError as e:
            if 'UNIQUE constraint' in e.args[0]:  #### This is subject to change with version control
                return HttpResponse(status=status.HTTP_409_CONFLICT)

        activitylogger.info("Enrolled " + user_id)  # log to file (found in logs/activity_log/)

        return HttpResponse(status=status.HTTP_200_OK)

    @swagger_auto_schema(**VerifierViewSetSwagger.verify)
    def verify(self, request, *args, **kwargs):
        '''
        200: ok
        460: no enrolled user with this username
        461: no stream found with this uuid
        500: Internal server error
        '''
        # check if all required info is passed
        if not "external_id" in request.data or not "uuid" in request.data:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
         
        user_id = request.data["external_id"]
        uuid = request.data["uuid"]
        
        # get enrolled voiceprint from db
        enrolledvp = Voiceprint.objects.filter(username=user_id)
        if not enrolledvp:  # no saved voiceprint for the user_id
            return JsonResponse({"detail": "A user with this external ID doesn't exist"}, status=460)
        # convert fetched binary voiceprint to python list
        serializer = VoiceprintSerializer(enrolledvp, many=True)
        enrolledvp = base64.decodebytes(serializer.data[0]["voiceprint"].encode('utf-8')) 
        enrolledvp = np.frombuffer(enrolledvp, dtype=np.float64).tolist()

        # get voiceprint from stream with the uuid
        res = requests.get(GET_VP_URL.format(uuid=uuid))
        stat = res.status_code
        if stat == 404:
            return JsonResponse({"detail": "A stream with this uuid doesn't exist"}, status=461)
        elif stat != 200:
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        curvp = res.json()['voiceprint']

        # compare voiceprints
        res = requests.post(COMPARE_VP_URL, data=json.dumps({"voiceprint1":enrolledvp, "voiceprint2": curvp}), headers={'Content-Type':'application/json'})
        if res.status_code != 200: 
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        score = res.json()['score']
        result = "True" if score >= settings.THRESHOLD else "False"

        activitylogger.info("Verified " + user_id + " (result: " + result + ", score: " + str(score) + ")")

        return JsonResponse({"result": result, "score": score}, status=200)

    @swagger_auto_schema(**VerifierViewSetSwagger.get_voiceprint)
    def get_voiceprint(self, request, *args, **kwargs):
        '''
        200: voiceprint successfully returned
        460: no user is enrolled under this username'''
        user_id = kwargs['id']

        # get enrolled voiceprint from db
        enrolledvp = Voiceprint.objects.filter(username=user_id)
        if not enrolledvp:  # no saved voiceprint for the user_id
            return HttpResponse(status=460)
        serializer = VoiceprintSerializer(enrolledvp, many=True)
        enrolledvp = base64.decodebytes(serializer.data[0]["voiceprint"].encode('utf-8'))
        # np.set_printoptions(precision=15)
        enrolledvp = np.frombuffer(enrolledvp, dtype=np.float64).tolist()        

        return JsonResponse({"voiceprint": enrolledvp}, status=200)

    @swagger_auto_schema(**VerifierViewSetSwagger.list_enrollements)
    def list_enrollments(self, request, *arg, **kwardgs):
        '''
        200: successfully returned all user IDs
        '''
        try:
            lst = list(Voiceprint.objects.values_list("username", flat=True))
            return JsonResponse({"ids": lst}, status=200)
        except:
            return HttpResponse(status=500)
        
    @swagger_auto_schema(**VerifierViewSetSwagger.delete_all_enrollment)
    def delete_all_enrollment(self, request, *args, **kwargs):
        '''
        200: successfuly deleted. Returns the number of removed users
        '''
        users = Voiceprint.objects.all()
        num = users.delete()[0]

        return JsonResponse({"deleted_count": num}, status=200)
    
    @swagger_auto_schema(**VerifierViewSetSwagger.delete_enrollment)
    def delete_enrollment(self, request, *args, **kwargs):
        '''
        200: successfully deleted
        400: no user with this id
        500: Internal Server Error'''
        user_id = kwargs["id"]
        try:
            deleted = Voiceprint.objects.filter(username=user_id)[0].delete()
            if deleted[0] == 0:
                return HttpResponse(400)
        except:
            return HttpResponse(500)

        return HttpResponse(200)
