# Voice Verification API

## Introduction
This project is built with 2 Django applications: SpeechEngine and VoiceVerifier. 
* **SpeechEngine**  
SpeechEngine takes care of handling streams of audio data, feeding the data to different models and fetching results. Currently, the application only uses one voice verification model (ECAPA TDNN) implemented by Speechbrain.  
More information on the open-source code can be found in this link: https://github.com/speechbrain/speechbrain  

* **VoiceVerifier**  
VoiceVerifier is the API with routes exposed to end-users. It uses SpeechEngine API to enroll users using their user IDs, storing and handling user voiceprints, and verifying new audio streams against enrolled users.  

## Python Environment
Both SpeechEngine and VoiceVerifier uses Python 3.8 and pip3. Python environment is already set up in Docker images given as .tar files.

## Docker Environment
The project uses docker-compose to run SpeechEngine and VoiceVerifier in parallel. 
### Images
Before building the docker-compose project, you must load the docker images included as voiceverifier.tar and speechbrain.tar files in the project folder.  
### IP Address 
SpeechEngine and VoiceVerifier are given fixed ip addresses of 172.19.0.2 and 172.19.0.3. Only VoiceVerifier (172.19.0.3) can be accessed from outside the local server through port 3000.  
  
### Configuration
All docker-compose configurations can be found in docker-compose.yml. 
```yml
version: '3.5'
services:
  speechbrain: 
    image: speechbrain
    container_name: speechbrain_compose
    tty: true
    volumes: 
      - "{local folder directory for ./SpeechEngine}:/home/SpeechEngine"
    command: 
      bash /home/SpeechEngine/run.sh
    networks: 
      voice_verifier_net:
        ipv4_address: 172.19.0.2

  voice_verifier:
    image: voice_verifier
    container_name: voice_verifier_compose
    tty: true
    ports: 
      - 3000:3000
    volumes: 
      - "{local folder directory for ./VoiceVerifier}:/home/VoiceVerifier"
    command:
      bash /home/VoiceVerifier/run.sh
    networks: 
      voice_verifier_net:
        ipv4_address: 172.19.0.3

networks: 
  voice_verifier_net:
    ipam:
      driver: default
      config:
        - subnet: 172.19.0.0/16
```

## Configure
All settings for SpeechEngine and VoiceVerifier can be found in "/SpeechEngine/SpeechEngine/settings.py" and "/VoiceVerifier/VoiceVerifier/settings.py".

## Running

* **Install Docker and Docker Compose**  
Install Docker: https://docs.docker.com/engine/install/  
Install Docker Compose: https://docs.docker.com/compose/install/

* **Configure Volumes**  
Edit "volumes: " sections in docker-compose.yml to create volumes to local directories.

* **Load images**
    ```sh
    docker load < speechbrain.tar
    docker load < voice_verifier.tar
    ```
* **Run application**
    ```
    docker-compose up
    ```
    Configuration in docker-compose.yml is set to automatically execute run.sh in SpeechEngine and VoiceVerifier at start of the application.


## Documentation

SpeechEngine and VoiceVerifier have separate Swagger documentation.  
SpeechEngine: http://172.19.0.2:3000/swagger/  
VoiceVerifier: http://171.19.0.3:3000/swagger/

## Logging

**Logs for SpeechEngine:**  
All logs are stored "./SpeechEngine/logs/"
* request_log  
    Logs all incoming request and any error messages incurred if applicable
    ```log
    2021-08-20 04:46:52,537 "POST /http_stream HTTP/1.1" 200 48
    2021-08-20 04:46:52,553 "POST /http_stream HTTP/1.1" 200 48
    2021-08-20 04:46:52,567 "POST /http_stream HTTP/1.1" 200 48
    2021-08-20 04:46:52,584 "POST /http_stream/242e10f5-1a00-46a8-85ab-5fc41d36e6ee HTTP/1.1" 200 0
    2021-08-20 04:46:52,599 "POST /http_stream/242e10f5-1a00-46a8-85ab-5fc41d36e6ee HTTP/1.1" 200 0
    ```
* system_log  
    Any other logs incurred by SpeechEngine application

**Logs for VoiceVerifier:**  
* request_log  
Same as SpeechEngine
* system_log  
Same as SpeechEngine
* activity_log  
    Logs all enrollment, deletion of enrollment and verification or any failures. 
    ```
    2021-08-20 06:21:36,975 Enrolled test
    2021-08-20 06:21:37,143 Verified test (result: True, score: 0.6239156723022461)
    2021-08-20 06:25:56,782 Enrolled test1
    2021-08-20 06:25:56,861 Enrolled test2
    2021-08-20 06:25:56,929 Verified test1 (result: True, score: 0.9999998807907104)
    2021-08-20 06:26:21,842 Enrolled test1
    2021-08-20 06:26:21,933 Enrolled test2
    2021-08-20 06:26:22,000 Verified test1 (result: True, score: 1.0)
    ```

## API Routes

### **SpeechEngine**
### Stream Routes
<table>
<td> Method </td> <td> Route </td> <td> Body </td><td> Response </td>
<tr>
<td>GET</td><td>/http_stream</td><td>NA</td>
<td>
200: OK
<pre>
{
  "streams": [
    "4d038bd4-8d92-4d16-8697-36770463c4d8",
    "8af9b39d-7830-4215-9244-fc2027730639"
  ]
}
</pre>
500: Internal Server Error
</td>
</tr>
<tr>
<td>POST</td> <td> /http_stream </td> <td>NA</td> 
<td> 
200: OK
<pre>
{
    "uuid": "4d038bd4-8d92-4d16-8697-36770463c4d8"
}
</pre>
500: Internal Server Error
</td> 
</tr>
<tr>
<td>POST</td> <td>/http_stream/{uuid}</td> <td>
<pre>
{ "data": "..."}
</pre>
</td> <td>
200: OK <br>
400: Malformed request <br>
404: No such UUID <br>
500: Internal Server Error <br>
512: Something went wrong connecting to Redis database
</td> 
</tr>
<tr>
<td>DELETE</td> <td>/http_stream/{uuid}</td> <td> NA </td> <td>
200: OK <br>
400: Malformed request <br>
404: No such UUID <br>
500: Internal Server Error <br>
512: Something went wrong connecting to Redis database
</td> 
</tr>
</table>

### Voiceprint Routes
<table>
<td> Method </td> <td> Route </td> <td> Body </td><td> Response </td>
<tr>
<td> GET </td> <td> /http_stream/voiceprint/{uuid} </td> <td> NA </td><td>
200: OK
<pre>
{ "voiceprint": [29.842374801635742, -15.604244232177734, 1.7878642082214355, ...] }
</pre>
404: No stream found with this UUID <br>
500: Internal Server Error
</td>
</tr>
<tr>
<td> POST </td> <td> /speakeridt/compare_vp </td> <td> <pre>
{  "voiceprint1": [29.842374801635742, 1.7878642082214355, ...], "voiceprint2": [-7.919283866882324, 2.2755887508392334, ...]}
</pre>
</td><td>
200: OK
<pre>
{ "score": 0.678 }
</pre>
500: Internal Server Error
</td>
</tr>
</table>

### **VoiceVerifier**
### Stream Routes
<table>
<td> Method </td> <td> Route </td> <td> Body </td><td> Response </td>
<tr>
<td>GET</td><td>/get_all_streams</td><td>NA</td>
<td>
200: OK
<pre>
{
  "streams": [
    "4d038bd4-8d92-4d16-8697-36770463c4d8",
    "8af9b39d-7830-4215-9244-fc2027730639"
  ]
}
</pre>
500: Internal Server Error
</td>
</tr>
<tr>
<td>POST</td> <td> /start_stream </td> <td>NA</td> 
<td> 
200: OK
<pre>
{
    "uuid": "4d038bd4-8d92-4d16-8697-36770463c4d8"
}
</pre>
500: Internal Server Error
</td> 
</tr>
<tr>
<td>POST</td> <td>/upload_stream_data/{uuid}</td> <td>
<pre>
{ "data": "..."}
</pre>
</td> <td>
200: OK <br>
400: Malformed request <br>
404: No such UUID <br>
500: Internal Server Error
</td> 
</tr>
</table>

### Verifier Routes
<table>
<td> Method </td> <td> Route </td> <td> Body </td><td> Response </td>
<tr>
<td>DELETE</td><td>/vv/delete_all_enrollment</td><td>NA</td>
<td>
200: OK
<pre>
{ "deleted_count": 21 }
</pre>
500: Internal Server Error
</td>
</tr>
<td>DELETE</td><td>/vv/delete_enrollment/{uuid}</td><td>NA</td>
<td>
200: Deleted <br>
400: A user with this external ID was not found <br>
500: Internal Server Error <br>
</td>
</tr>
<tr>
<td>POST</td> <td> /vv/enroll </td> <td> <pre>
{
  "uuid": "4d038bd4-8d92-4d16-8697-36770463c4d8",
  "external_id": "test"
}
</pre>
</td> 
<td> 
200: OK <br>
400: uuid or external ID was not passed over <br>
404: Stream with this uuid doesn't exist <br>
409: user_id already exists <br>
500: Internal Server Error <br>
</td> 
</tr>
<tr>
<td>GET</td><td>/vv/get_voiceprint/{id}</td><td>NA</td>
<td>
200: OK
<pre>
{ "voiceprint": [29.842374801635742, -15.604244232177734, 1.7878642082214355, ...] }
</pre>
460: No user enrolled with this external ID <br>
500: Internal Server Error
</td>
</tr>
<tr>
<td>GET</td><td>/vv/list_enrollments/{id}</td><td>NA</td>
<td>
200: OK
<pre>
{
  "ids": [
    "test1",
    "test2"
  ]
}
</pre>
500: Internal Server Error
</td>
</tr>
<tr>
<td>POST</td> <td>/vv/verify/{id}</td> <td>
<pre>
{ "uuid": "4d038bd4-8d92-4d16-8697-36770463c4d8",
"external_id": "test1"}
</pre>
</td> <td>
200: OK 
<pre>
{ "score": 0.678 }
</pre>
460: A user with this external ID doesn't exist <br>
461: A stream with this uuid doesn't exist <br>
500: Internal Server Error
</td> 
</tr>
</table>


