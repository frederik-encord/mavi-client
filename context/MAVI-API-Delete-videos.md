# Delete Videos

- 
- MAVI API
- Delete Videos
# Delete Videos

To free up cloud storage or remove unused videos from the MAVI database, developers can call this API to delete all raw and derived data associated with specified videoNos in the request. Once the API is successfully completed, no data related to deleted videos will be retained.

`videoNos`## Prerequisites​

- You have created a MAVI API key.
## Host URL​

- https://mavi-backend.openinterx.com
DELETE /api/serve/video/delete

`/api/serve/video/delete`- Rate limit: max 500 videos each call.
## Request Example​

```codeBlockLines_e6Vv
import requests  headers = {"Authorization": "<API_KEY>"}  # API key  # List of video IDs to delete  data = ["<list of videoNos>"]  response = requests.delete(      "https://mavi-backend.openinterx.com/api/serve/video/delete",      headers=headers,      json=data  )  print(response.json())
```

## Request Body​

```codeBlockLines_e6Vv
[    "string"  ]
```

## Request Parameters​

## Response Example​

Status code 200

```codeBlockLines_e6Vv
{  "code": "string",  "msg": "string"}
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


*Source: https://docs.openinterx.com/MAVI-API/Delete-videos*
