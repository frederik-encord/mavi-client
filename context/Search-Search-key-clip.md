# Search Key Clip

- 
- MAVI API
- Search
- Search Key Clip
# Search Key Clip

While the Search-Video API retrieves the most relevant videos, this API identifies and ranks the most relevant clips within one or multiple videos. The output is sorted by the relevance of the clips. With this API, developers can quickly pinpoint moments of interest across all uploaded videos in just milliseconds.

## Prerequisites​

- You have created a MAVI API key.
- At least one video has been uploaded to MAVI and is currently in the PARSE status.
## Host URL​

- https://mavi-backend.openinterx.com
POST /api/serve/video/searchVideoFragment

`/api/serve/video/searchVideoFragment`## Request Example​

```codeBlockLines_e6Vv
import requests  headers = {"Authorization": "<API_KEY>"}  # API key  data = {      "videoNos": ["<video_no>", "video_no", ...],  # List of specific video IDs (you need at least 1 video_no to do the search)      "searchValue": "<your prompt>"  # The search query  }  response = requests.post(      "https://mavi-backend.openinterx.com/api/serve/video/searchVideoFragment",      headers=headers,      json=data  )  print(response.json())
```

## Request Body​

```codeBlockLines_e6Vv
{  "videoNos": [],  "searchValue": "string"}
```

## Request Parameters​

## Response Example​

```codeBlockLines_e6Vv
{  "code": "string",  "msg": "string",  "data": {    "videos": [      {        "videoNo": "string",        "videoName": "string",        "videoStatus": "string",        "uploadTime": "string",        "duration": "string"      }    ]  }}
```

## Response Result​

## Response Structure​

Status code 200

- Prerequisites
- Host URL
- Request Example
- Request Body
- Request Parameters
- Response Example
- Response Result
- Response Structure


*Source: https://docs.openinterx.com/MAVI-API/Search/Search-key-clip*
