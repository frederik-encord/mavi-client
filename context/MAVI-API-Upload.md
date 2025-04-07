# Upload Video

- 
- MAVI API
- Upload Video
# Upload Video

Use this API to upload your video to MAVI! Once the video is uploaded, it enters the MAVI video processing pipeline, and you can query the status of video processing at any time. Additionally, by providing a callback URI in the request body, MAVI can automatically notify you about the status, saving you hassle of waiting in front your screen!

## Prerequisites​

- You’re familiar with the concepts described on the Platform overview page.
- You have created a MAVI API key.
- The videos must meet the following requirements to ensure successful encoding process:

Video and audio formats: The video files must be encoded in h264, h265, vp9 or hevc.
Audio track: If you intend to use audio transcription feature, the video you are uploading must contain an audio track.
- Video and audio formats: The video files must be encoded in h264, h265, vp9 or hevc.
`h264``h265``vp9``hevc`- Audio track: If you intend to use audio transcription feature, the video you are uploading must contain an audio track.
## Host URL​

- https://mavi-backend.openinterx.com
## Endpoint​

POST /api/serve/video/upload

`/api/serve/video/upload`## Request Example​

```python
import requests  
headers = {"Authorization": "<API_KEY>"}  # API key  # Video file details  
data = {      "file": ("<MY_VIDEO_NAME>", open("<VIDEO_FILE_PATH>", "rb"), "video/mp4")  }  # Optional callback URL for task status notifications  
params = {"callBackUri": "<YOUR_CALLBACK_URI>"}  
response = requests.post(
    "https://mavi-backend.openinterx.com/api/serve/video/upload", 
    files=data, 
    params=params,      
    headers=headers
) 
print(response.json())
```

Replace API_KEY in the code above with your actual API key, MY_VIDEO_NAME with your video's name (including the file extension, e.g., .mp4), VIDEO_FILE_PATH with the path to your video file, and YOUR_CALLBACK_URI with your public callback URL. Ensure that the callback URL is publicly accessible, as the resolution results will be sent to this address via a POST request with the following request body:
Replace API_KEY in the code above with your actual API key, MY_VIDEO_NAME with your video's name (including the file extension, e.g., .mp4), VIDEO_FILE_PATH with the path to your video file, and YOUR_CALLBACK_URI with your public callback URL. Ensure that the callback URL is publicly accessible, as the resolution results will be sent to this address via a POST request with the following request body:

```json
{  "videoNo": "mavi_video_554046065381212160",  "clientId": "d7a7427b502df6c8e31de003675b7b77",  "status": "PARSE"}
```

The callback request body includes the following fields:

- videoNo: The unique video number.
- clientId: Identifies the client that is being used to upload the video.
- status: The processing status of the video.
The status field can have one of the following values:

- "PARSE" – The video is being processed.
`"PARSE"`- "UNPARSE" – The video has not been processed.
`"UNPARSE"`- "FAIL" – The video processing failed.
`"FAIL"`## Request Body​

```codeBlockLines_e6Vv
file: ""
```

## Request Parameters​

## Response Example​

Status code 200

```codeBlockLines_e6Vv
{  "code": "string",  "msg": "string",  "data": {    "videoNo": "string",    "videoName": "string",    "videoStatus": "string",    "uploadTime": "string"  }}
```

## Response Structure​

Note: The callBackUri field will actively notify you of the task status after the video upload is complete and the parsing task is finished.

- Prerequisites
- Host URL
- Endpoint
- Request Example
- Request Body
- Request Parameters
- Response Example
- Response Structure


*Source: https://docs.openinterx.com/MAVI-API/Upload*
