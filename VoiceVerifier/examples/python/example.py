import base64
import requests
import time
# from io import BytesIO
import json
import numpy as np
import os

BASE = "http://172.19.0.3:3000/"

TEST_FILE_PATH_BASE = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/test_audio/"

f1_1 = TEST_FILE_PATH_BASE + 'speaker_1/01.wav'
f1_2 = TEST_FILE_PATH_BASE + 'speaker_1/02.wav'
f1_3 = TEST_FILE_PATH_BASE + 'speaker_1/03.wav'
f1_4 = TEST_FILE_PATH_BASE + 'speaker_1/04.wav'
f1_5 = TEST_FILE_PATH_BASE + 'speaker_1/05.wav'
f1_6 = TEST_FILE_PATH_BASE + 'speaker_1/06.wav'
f1_7 = TEST_FILE_PATH_BASE + 'speaker_1/07.wav'
f2_1 = TEST_FILE_PATH_BASE + 'speaker_2/01.wav'
f2_2 = TEST_FILE_PATH_BASE + 'speaker_2/02.wav'
f2_3 = TEST_FILE_PATH_BASE + 'speaker_2/03.wav'
f2_4 = TEST_FILE_PATH_BASE + 'speaker_2/04.wav'
f3_1 = TEST_FILE_PATH_BASE + 'speaker_3/04.wav'

######### Create Streams #########
resp = requests.post(BASE + "start_stream")  # stream 1
uuid1 = resp.json()['uuid'] 
resp = requests.post(BASE + "start_stream")  # stream 2
uuid2 = resp.json()['uuid']
resp = requests.post(BASE + "start_stream")  # stream x
uuidx = resp.json()['uuid']

######### Send Data to Stream 1 #########
with open(f1_1, "rb") as file:
    while True:
        data = file.read(30000) # send chunks
        if not data:
            break
        
        data = base64.b64encode(data).decode('utf-8')
        response = requests.post(BASE + "upload_stream_data/" + uuid1, data=json.dumps({"data":data}), headers={'Content-Type': 'application/json'})

######### Send Data to Stream 2 #########
with open(f2_3, "rb") as file:
    while True:
        data = file.read(30000)
        if not data:
            break
        
        # t1 = time.time()
        data = base64.b64encode(data).decode('utf-8')
        response = requests.post(BASE + "upload_stream_data/" + uuid2, data=json.dumps({"data":data}), headers={'Content-Type': 'application/json'})
        # print(time.time() - t1)

######### Send Data to Stream x #########
with open(f1_3, "rb") as file:
    while True:
        data = file.read(30000)
        if not data:
            break

        data = base64.b64encode(data).decode('utf-8')
        response = requests.post(BASE + "upload_stream_data/" + uuidx, data=json.dumps({"data":data}), headers={'Content-Type': 'application/json'})

######### Enroll User #########
res = requests.post(BASE + "vv/enroll", data=json.dumps({'external_id': "test1", "uuid": uuid1}),  # enroll user "test1"
                    headers={'Content-Type': 'application/json'})
res = requests.post(BASE + "vv/enroll", data=json.dumps({'external_id': "test2", "uuid": uuid2}),  # enroll user "test2"
                    headers={'Content-Type': 'application/json'})

######## Verify User #########
res = requests.post(BASE + "vv/verify", data=json.dumps({'external_id': "test1", "uuid": uuidx}),  # compare "test1" and stream x
                    headers={'Content-Type': 'application/json'})
print("score: {}".format(res.json()["score"]))

res = requests.post(BASE + "vv/verify", data=json.dumps({'external_id': "test2", "uuid": uuidx}),  # compare "test2" and stream x
                    headers={'Content-Type': 'application/json'})
print("score: {}".format(res.json()["score"]))

######## Delete enrollemnt by ID ########
# res = requests.delete(BASE + 'vv/delete_enrollment/test2')

######## Delete all enrollments ########
res = requests.delete(BASE + 'vv/delete_all_enrollment')
