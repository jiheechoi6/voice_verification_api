from email.message import Message
from rest_framework.viewsets import ViewSet
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import *
from drf_yasg.utils import swagger_auto_schema
from SpeechEngine.swagger_doc.stream import HttpStreamDataViewSetSwagger
from io import BytesIO
import torch
import time
import numpy as np


from SpeechEngine.speechbrain.pretrained import EncoderClassifier
from SpeechEngine.service.stream_manager import StreamManager


encoder = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")

class HttpStreamDataViewSet(ViewSet):
    def __init__(self):
        self.get_similarity = torch.nn.CosineSimilarity(dim=-1, eps=1e-6)

    @swagger_auto_schema(**HttpStreamDataViewSetSwagger.start)
    def start_stream(self, request, *args, **kwargs):
        '''Creates a stream entry and the uuid.

        :response
            200: Stream was created successfully 
                uuid: uuid of the stream created
            500: Internal Server Error
        '''
        uuid = StreamManager.create_stream()

        # check if uuid creation was successful
        if uuid != None and len(uuid) != 0:
            return JsonResponse({'uuid': uuid}, status=status.HTTP_200_OK)
        
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(**HttpStreamDataViewSetSwagger.upload)
    def upload_data(self, request, *args, **kwargs):
        '''uploads wav data passed as base64 string (latin-1 encoding) to stream. 
        This appends the existing stream entry in redis db
        
        :param
            uuid: uuid of the stream to add data to
        :body
            { data: data to be uploaded to stream in base64 string form (latin-1 encoded)}
        :response
            200: Data sucessfully uploaded to stream
            400: Data is missing from request
            404: No stream found with this uuid
            500: Internal server error
            512: Something went wrong connecting to Redis database
        '''
        # get uuid passed as parameter

        uuid = kwargs['uuid']
        data = request.data["data"]

        if not uuid or not data:  # no audio data passed
            return HttpResponse(status.HTTP_400_BAD_REQUEST)
        try:
            success = StreamManager.write_to_stream(data, uuid)  # append to stream
            return HttpResponse(status=success)
        except SystemError:
            return JsonResponse({"detail":"Something went wrong when starting database server"}, status=512)
        except ValueError:
            return HttpResponse({"detail":"Stream with this uuid doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
        except:
            return HttpResponse(status=500)

    # def test(self, request, *args, **kwargs):
    #     file1 = request.data['file1']
    #     read = file1.read()
    #     data = read.decode('utf-16').encode("utf-16")[2:]
    #     file1.seek(0)
    #     print(BytesIO(data))
    #     wavform1 = self.encoder.load_audio_stream(BytesIO(data))
    #     wavform2 = self.encoder.load_audio_stream(request.data['file2'])
    #     # wavform1 = encoder.load_audio("/home/speechbrain/recipes/VoxCeleb/SpeakerRec/flask/audio_dataset/1/01.wav")
    #     # wavform2 = encoder.load_audio("/home/speechbrain/recipes/VoxCeleb/SpeakerRec/flask/audio_dataset/2/03.wav")
    #     embedding1 = self.encoder.encode_batch(wavform1, None, normalize=True)
    #     embedding2 = self.encoder.encode_batch(wavform2, None, normalize=True)

    #     print(self.get_similarity(embedding1, embedding2))

    #     return HttpResponse(status=200)

    @swagger_auto_schema(**HttpStreamDataViewSetSwagger.get_voiceprint)
    def get_voiceprint(self, request, *args, **kwargs):
        '''returns voiceprint of audio stream
        :param 
            uuid: uuid of the audio to extract voiceprint from
        :response
            200: voiceprint successfully created
            400: Data is missing from request
            404: No stream found with this uuid
            500: Internal server error
            512: Something went wrong connecting to Redis database
        '''
        uuid = kwargs['uuid']
        audio = StreamManager.get_audio_string(uuid)

        if isinstance(audio, int):
            return HttpResponse(status=audio)
 
        # print(np.frombuffer(audio.encode("latin-1")[44:], dtype=np.int16)/32767)
        # waveform = encoder.load_audio_stream(BytesIO(audio.encode("latin-1")))
        waveform = encoder.load_audio_stream(audio)
        embedding = encoder.encode_batch(waveform, None, normalize=True).tolist()[0][0]

        return JsonResponse({"voiceprint": embedding}, status=200)

    @swagger_auto_schema(**HttpStreamDataViewSetSwagger.compare)
    def compare_voiceprint(self, request):
        '''Compares voiceprints and sends back similarity score

        :body
            voiceprint1: voiceprint to be compared with voiceprint2 in float list
            voiceprint2: voiceprint to be compared with voiceprint1 in float list
        '''
        try:
            vp1 = torch.Tensor(request.data['voiceprint1'])
            vp2 = torch.Tensor(request.data['voiceprint2'])
            score = self.get_similarity(vp1, vp2).tolist()
        except:
            return HttpResponse(status=500)
            
        return JsonResponse({"score": score}, status=200)

    @swagger_auto_schema(**HttpStreamDataViewSetSwagger.delete)
    def delete(self, request, *args, **kwargs):
        '''Deletes an audio stream corresponding to uuid passed
        :param
            uuid of audio stream to delete
        '''
        uuid = kwargs['uuid']
        if not uuid:  # uuid was not passed
            return JsonResponse({"detail":"uuid must be indicated"}, status=400)
        
        try:
            StreamManager.delete_stream(uuid)
            return HttpResponse(status=200)
        except ValueError as e:
            return JsonResponse({"detail":"No stream with such uuid"}, status=404)
        except  SystemError:
            return HttpResponse({"detail":"Could not connect to Redis database server"}, status=512)
        except:
            return HttpResponse(status=500)

    @swagger_auto_schema(**HttpStreamDataViewSetSwagger.get_all_streams)
    def get_all_streams(self, request, *args, **kwargs):
        '''
        Fetches uuid list of all ongoing streams
        200: success
        500: Internal Server Error '''
        try:
            streams = StreamManager.get_all_streams()
        except SystemError:
            return HttpResponse(status=500)

        return JsonResponse({"streams": streams}, status=200)
