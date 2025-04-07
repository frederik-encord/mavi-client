# Search Video

- 
- MAVI API
- Search
- Search Video
# Search Video

Using a natural language query, this API will search through all processed videos and ranks the results within milliseconds. MAVI retrieves and ranks videos based on visual information in a manner similar to human perception. With this API, developers can access the most relevant videos from their entire library.

## Prerequisites​

- You have created a MAVI API key.
- At least one video has been uploaded to MAVI and is currently in the PARSE status.
## Host URL​

- https://mavi-backend.openinterx.com
POST /api/serve/video/searchAI

`/api/serve/video/searchAI`## Request Example​

```codeBlockLines_e6Vv
import requests  headers = {"Authorization": "<API_KEY>"}  # API key  data = {      "searchValue": "<YOUR_PROMPT>"  # The search query  }  response = requests.post(      "https://mavi-backend.openinterx.com/api/serve/video/searchAI",      headers=headers,      json=data  )  print(response.json())
```

Replace API_KEY in the code above with your actual API key and YOUR_PROMPT with your search query. You can search for relevant videos you've uploaded using natural language.

`API_KEY``YOUR_PROMPT`## Request Body​

```codeBlockLines_e6Vv
{  "searchValue": "string"}
```

## Request Parameters​

## Response Example​

Status code 200

```codeBlockLines_e6Vv
{  "code": "string",  "msg": "string",  "data": {    "videos": [      {        "videoNo": "string",        "videoName": "string",        "videoStatus": "string",        "uploadTime": "string"      }    ]  }}
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


*Source: https://docs.openinterx.com/MAVI-API/Search/Search-video*
