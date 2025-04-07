# Video Chat

- 
- MAVI API
- Video Chat
# Video Chat

Developer could interact with an LLM AI assistant based on the context of one or multiple videos. By simply providing the videoNos, developers can request the LLM to analyze, summarize, annotate, and more for all uploaded videos. Additionally, this API supports streaming these responses to minimize latency during response generation.

`videoNos`## Prerequisites​

- You have created a MAVI API key.
- At least one video has been uploaded to MAVI and is currently in the PARSE status.
## Language Limitations​

- Currently, only English searches are supported. Please ensure your query parameters are in English.
- Chinese, French, Spanish, and other languages are not supported.
## Host URL​

- https://mavi-backend.openinterx.com
POST /api/serve/video/chat

`/api/serve/video/chat`## Request Example​

```codeBlockLines_e6Vv
import requests  headers = {"Authorization": "<API_KEY>"}  # API key  data = {      "videoNos": <list of videoNos>,  # List of video IDs to chat about      "message": "<your prompt>",  # User query or prompt      "history": [],  # Chat history (leave empty for new conversations)      "stream": False  # Set to True for streaming responses  }  response = requests.post(      "https://mavi-backend.openinterx.com/api/serve/video/chat",      headers=headers,      json=data  )  print(response.text)
```

## Request Body​

```codeBlockLines_e6Vv
{  "videoNos": [    "string"  ],  "message": "string",  "history": [    {      "robot": "string",      "user": "string"    }  ],  "stream": true}
```

## Request Parameters​

## Response Example​

Status code 200

```codeBlockLines_e6Vv
{  "code": "string",  "msg": "string",  "data": {    "msg": "string"  }}
```

## Response Result​

## Response Structure​

Status code 200

- Prerequisites
- Language Limitations
- Host URL
- Request Example
- Request Body
- Request Parameters
- Response Example
- Response Result
- Response Structure


*Source: https://docs.openinterx.com/MAVI-API/Video-Chat/*
