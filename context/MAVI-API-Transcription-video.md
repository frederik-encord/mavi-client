# Transcription video

- 
- MAVI API
- Transcription video
# Transcription video

Transcription API converts visual and autio context of the video into text representations. You could transcribe an uploaded vidoe in two ways:

- AUDIO: Transcribing the video's audio content into text.
`AUDIO`- VIDEO: Transcribing the video's visual content into text.
`VIDEO`## Prerequisites​

- You have created a MAVI API key.
- At least one video has been uploaded to MAVI and is currently in the PARSE status.
## Host URL​

- https://mavi-backend.openinterx.com
## Submit Transcription Task​

You can submit a transcription task through this interface with the following options:

- Choose between AUDIO or VIDEO transcription.
- Specify a callback address to receive the transcription results automatically.
- Opt not to use a callback—in this case, you can retrieve the transcription results using the query interface.
POST /api/serve/video/subTranscription

`/api/serve/video/subTranscription`## Request Example​

```codeBlockLines_e6Vv
import requests  headers = {"Authorization": "<API_KEY>"}  # API key  data = {      "videoNo": "<VIDEO_NO>",  # The video ID to transcribe      "type": "AUDIO/VIDEO",  # Specify "AUDIO" for audio-only, "VIDEO" for video-only, or "AUDIO/VIDEO" for both      "callBackURI": "<CALLBACK>"  # Optional callback URL for status notifications  }  response = requests.post(      "https://mavi-backend.openinterx.com/api/serve/video/subTranscription",      headers=headers,      json=data  )  print(response.json())
```

Replace the placeholders in the code above with your actual values:

- API_KEY: Your API key.
`API_KEY`- VIDEO_NO: The unique video number.
`VIDEO_NO`- AUDIO or VIDEO: The transcription type (choose one).
`AUDIO``VIDEO`- CALLBACK: (Optional) A publicly accessible URL endpoint,
`CALLBACK`## Request Body​

```codeBlockLines_e6Vv
{  "videoNo": "string",  "type": "string",  "callBackURI": "string"}
```

`AUDIO``VIDEO`## Response Example​

Status code 200

```codeBlockLines_e6Vv
{  "code": "string",  "msg": "string",  "data": {    "taskNo": "string"  }}
```

## GET Transcription Content​

You can get the transcription content of the video through this interface, you need to provide the video number.

GET /api/serve/video/getTranscription

`/api/serve/video/getTranscription`## Request Example​

```codeBlockLines_e6Vv
import requests  headers = {"Authorization": "<API_KEY>"}  # API key  # Task number associated with the transcription request  params = {"taskNo": "<TASK_NO>"}  response = requests.get(      "https://mavi-backend.openinterx.com/api/serve/video/getTranscription",      headers=headers,      params=params  )  print(response.json())
```

Replace the API_KEY in the above code as your API key, TASK_NO as your task number, you can get the transcription content of the video through the task number.

`API_KEY``TASK_NO`## Request Parameters​

## Response Example​

If you provide a callback URL when submitting the task, a mesage containing content inside data in the following example will be sent to  callback URL automatically to notify the status of the task.

Status code 200

```codeBlockLines_e6Vv
{  "code": "string",  "msg": "string",  "data": {    "status": "FINISH",    "type": "AUDIO",    "videoNo": "videoNo_fd30e4c3700c",    "taskNo": "taskNo_0a3f11298b9e",    "transcriptions": [      {        "id": 0,        "startTime": 0,        "endTime": 0,        "content": "content_0e5150607a47"      }    ]  }}
```

```codeBlockLines_e6Vv

```

`FINISH``UNFINISHED`- Prerequisites
- Host URL
- Submit Transcription Task
- Request Example
- Request Body
- Response Example
- GET Transcription Content
- Request Example
- Request Parameters
- Response Example


*Source: https://docs.openinterx.com/MAVI-API/Transcription-video*
