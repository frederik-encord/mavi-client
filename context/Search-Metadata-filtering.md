# Filtering

- 
- MAVI API
- Search
- Search Metadata
- Filtering
# Filtering

The endpoints that return lists of items support filtering.

## Prerequisites​

- You have created a MAVI API key.
## Example​

This example demonstrates how to filter uploaded videos within the date range from March 3, 2025, 09:57 (1740995860114) to March 10, 2025, 09:57 (1741600632000), and only include videos that have been successfully parsed (PARSE status).

`March 3, 2025, 09:57``1740995860114``March 10, 2025, 09:57``1741600632000``PARSE````codeBlockLines_e6Vv
import requests  headers = {"Authorization": "<API_KEY>"}  # API key  params = {      "startTime": 1740995860114,      "endTime": 1741600632000,      "videoStatus": "PARSE"  }  response = requests.get("https://mavi-backend.openinterx.com/api/serve/video/searchDB",                          params=params,                          headers=headers)  print(response.json())
```

- Prerequisites
- Example


*Source: https://docs.openinterx.com/MAVI-API/Search/Search-Metadata/filtering*
