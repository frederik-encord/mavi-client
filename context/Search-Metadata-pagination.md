# Pagination

- 
- MAVI API
- Search
- Search Metadata
- Pagination
# Pagination

Endpoints that return a list of items support pagination. You can manage pagination using the following parameters:

- page – The page number to retrieve (default: 1).
`1`- pageSize – The number of items per page (default: 20, maximum: 200).
`20``200`## Prerequisites​

- You have created a MAVI API key.
## Examples​

When calling the Search Metadata API, you can specify page and pageSize parameters to control pagination. The example below sets pageSize to 30 and retrieves page number 2, returning results from 31 to 60.

`page``pageSize``pageSize``page````codeBlockLines_e6Vv
import requests  headers = {"Authorization": "<YOUR_APP_KEY>"}  # API key  params = {"page": 2, "pageSize": 30}  response = requests.get("https://mavi-backend.openinterx.com/api/serve/video/searchDB",                          params=params,                          headers=headers)  print(response.json())
```

- Prerequisites
- Examples


*Source: https://docs.openinterx.com/MAVI-API/Search/Search-Metadata/pagination*
