import base64
from urllib import error
from speechbrain.pretrained.interfaces import SpectralMaskEnhancement
import redis
import uuid
from rest_framework import status

import time

HTTPSTREAM_EXPIRATION = 50
HEADER_LENGTH = 44  # length in bytes of wav file header

class StreamManager:
    @staticmethod
    def start():
        pool = redis.ConnectionPool(host="localhost", port=6379, db=0, decode_responses=True)
        return redis.Redis(connection_pool=pool)

    @staticmethod
    def create_stream():
        '''Creates uuid and makes entry in redis server with uuid as key
        Stream expires in HTTPSTREAM EXPIRATION if no data is written

        Returns
        -------
        string
            newly formed uuid
        '''
        # create random uuid
        new_uuid = str(uuid.uuid4())

        # insert uuid key in redis db
        r = StreamManager.start()
        r.set(new_uuid, "")

        # set the stream to expire 
        r.expire(new_uuid, HTTPSTREAM_EXPIRATION)

        return new_uuid

    @staticmethod
    def write_to_stream(data, uuid):
        '''
        Arguments
        ---------
        data : base64 string in latin-1 encoding
        uuid : uuid of the stream to write to
        Returns
        -------
        int
            status code. If stream with uuid doesn't exist, returns 404 not found.
            Otherwise returns 200 OK.
        '''
        try:
            r = StreamManager.start()
        except:
            raise SystemError("Unable to start Redis database server")

        if not r.exists(uuid):  # stream uuid doesn't exist
            raise ValueError("There is no stream with such uuid")

        data = base64.b64decode(data.encode('utf-8')).decode('latin-1')
        # print(data[:80])
        r.expire(uuid, HTTPSTREAM_EXPIRATION)  # reset expiration

        # remove header if not the first time appending
        # if len(r.get(uuid)) != 0:
        #     print("remove header")
        #     data = StreamManager.remove_header(data)

        data = StreamManager.remove_header(data)
        r.append(uuid, data)

        return status.HTTP_200_OK

    @staticmethod
    def get_audio_string(uuid):
        '''Get voiceprint of stream with the uuid
        Argument
        --------
        uuid : uuid of stream
        Returns
        _______
        List
            bytes object that contains latin-1 encoded audio data string'''
        r = StreamManager.start()
        audio = r.get(uuid)

        if not audio:
            return status.HTTP_404_NOT_FOUND

        return audio

    @staticmethod
    def delete_stream(uuid):
        '''Deletes a stream given uuid of the stream'''
        try:
            r = StreamManager.start()
        except:
            raise SystemError("Redis server couldn't be connected")
        
        if not r.exists(uuid):
            raise ValueError("No stream with such uuid was found")

        r.delete(uuid)
        return True

    @staticmethod
    def remove_header(data):
        '''Helper method that removes file header
        Argument
        --------
        data:
            latin-1 encoded string containing audio data
        Returns
        -------
            The same audio data without header
        '''
        # check if there's header
        if "RIFF" in data[:HEADER_LENGTH]:
            return data[HEADER_LENGTH:]
        else:
            return data

    @staticmethod
    def get_all_streams():
        '''Fetches uuid(s) of all ongoing streams'''
        try:
            r = StreamManager.start()
        except:
            raise SystemError("Redis server couldn't be connected")

        return r.keys()
