# Search Video Metadata

- 
- MAVI API
- Search
- Search Metadata
# Search Video Metadata

MAVI stores metadata of uploaded videos to simplify developers' workflows. Developers can retrieve the metadata for all videos at once or flexibly fetch a subset of video metadata by using filtering parameters in their requests.

## Prerequisites​

- You have created a MAVI API key.
## Host URL​

- https://mavi-backend.openinterx.com
## Endpoint​

GET /api/serve/video/searchDB

`/api/serve/video/searchDB`## Request Example​

```codeBlockLines_e6Vv
import requests  headers = {"Authorization": "<API_KEY>"}  # API key  # Uncomment the following line to apply filters:  # This filter retrieves parsed videos uploaded between timestamps 1740995860114 and 1740995860115,  # returning up to 100 results on the first page.  # params = {"startTime": 1740995860114, "endTime": 1740995860115, "videoStatus": "PARSE", "page": 1, "pageSize": 100}  response = requests.get(      "https://mavi-backend.openinterx.com/api/serve/video/searchDB",      # params=params,      headers=headers  )  print(response.json())
```

Replace API_KEY in the code above with your actual API key.

`API_KEY`You can add filter conditions to the params, with the following available parameters:

`params`- startTime (ms): Timestamp of the uploaded video (start time).
- endTime (ms): Timestamp of the uploaded video (end time).
- videoStatus (PARSE, UNPARSE, FAIL): The processing status of the video.
`PARSE``UNPARSE``FAIL`- page: The page number for pagination — i.e. which range of results to retrieve
- pageSize: The number of elements per page.
## Request Parameters​

## Response Example​

Status code 200

```codeBlockLines_e6Vv
{  "code": "string",  "msg": "string",  "data": {    "page": 0,    "current": 0,    "total": 0,    "pageSize": 0,    "videoData": [      {        "videoNo": "string",        "videoName": "string",        "videoStatus": "string",        "uploadTime": "string",      }    ]  }}
```

## Response Result​

## Response Structure​

Status code 200

- Prerequisites
- Host URL
- Endpoint
- Request Example
- Request Parameters
- Response Example
- Response Result
- Response Structure


*Source: https://docs.openinterx.com/MAVI-API/Search/Search-Metadata/*
