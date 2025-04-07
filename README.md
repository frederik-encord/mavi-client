# MAVI API Client

A Python client for interacting with the MAVI API, which provides video processing, transcription, and search capabilities.

## Features

- Complete API client for the MAVI platform
- Strong typing with Pydantic models
- Input validation and response parsing
- Detailed documentation
- Comprehensive error handling

## Installation

1. Clone this repository:
```
git clone <repository-url>
cd mavi
```

2. Set up a virtual environment and install dependencies:
```
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
pip install -e .
```

## Configuration

Create a `.env` file in the root directory with your MAVI API key:

```
MAVI_API_KEY=your-api-key-here
```

## Usage

### Initialize the client

```python
from mavi_client import MaviClient

# Initialize with API key from .env file
client = MaviClient()

# Or provide API key directly
client = MaviClient(api_key="your-api-key")
```

### Upload a video

```python
# Upload a video with optional progress tracking
response = client.upload_video(
    file_path="path/to/your/video.mp4", 
    custom_name="My Video.mp4",  # Optional
    callback_uri="https://your-callback-url.com/webhook",  # Optional
    progress_callback=lambda progress: print(f"Upload progress: {progress}%")  # Optional
)

# Access the response with proper typing
video_no = response.data.videoNo
video_name = response.data.videoName
status = response.data.videoStatus
```

The video must meet the following requirements:
- Encoded in h264, h265, vp9, or hevc format
- Must contain an audio track if you plan to use audio transcription

### Transcription

```python
from mavi_client import TranscriptionType

# Submit transcription task
transcription_task = client.submit_transcription(
    video_no=video_no,
    transcription_type=TranscriptionType.AUDIO,  # Or TranscriptionType.VIDEO
    callback_uri="https://your-callback-url.com/endpoint"  # Optional
)

# Get task number
task_no = transcription_task.data.taskNo

# Retrieve transcription result (when task is complete)
transcription = client.get_transcription(task_no)

# Access the transcription items
for item in transcription.data.transcriptions:
    start_time = item.startTime / 1000  # Convert to seconds
    end_time = item.endTime / 1000  # Convert to seconds
    print(f"{start_time:.2f} - {end_time:.2f}: {item.content}")
```

### Search videos

```python
# Search across all videos using natural language
search_results = client.search_videos("people talking at conference")

# Access the results
videos = search_results.data.videos
print(f"Found {len(videos)} matching videos")

# Search for specific clips within videos
clip_results = client.search_video_clips(
    video_nos=["video123", "video456"],
    search_value="person explaining charts"
)

# Access video clip results
for clip in clip_results.data.videos:
    print(f"Video: {clip.videoName}")
    print(f"Clip: {clip.fragmentStartTime:.2f}s - {clip.fragmentEndTime:.2f}s")
```

### Search by metadata

```python
from datetime import datetime, timezone
from mavi_client import VideoStatus

# Search for videos with metadata filtering
metadata_results = client.search_metadata(
    start_time=datetime(2023, 1, 1, tzinfo=timezone.utc),  # Optional
    end_time=datetime(2023, 12, 31, tzinfo=timezone.utc),  # Optional
    video_status=VideoStatus.PARSE,  # Optional
    video_name="Conference",  # Optional
    page=1,
    page_size=50
)

# Access the metadata search results
total_videos = metadata_results.data.total
for video in metadata_results.data.videoData:
    print(f"Video: {video.videoName} (ID: {video.videoNo})")
    print(f"Status: {video.videoStatus}, Uploaded: {video.uploadTime}")
```

### Delete videos

```python
# Delete one or more videos (max 500 per call)
delete_response = client.delete_videos(["video123", "video456"])
print(f"Delete status: {delete_response.code} - {delete_response.msg}")
```

### Chat with videos

```python
# Chat about videos (non-streaming)
from mavi_client import ChatHistoryItem

chat_response = client.video_chat(
    video_nos=["video123"],
    message="What is discussed in this video?",
    history=None,  # Optional chat history
    stream=False   # Get complete response
)

print(f"Assistant: {chat_response.data.msg}")

# Chat with streaming response
streaming_response = client.video_chat(
    video_nos=["video123"],
    message="Summarize the key points",
    history=[
        ChatHistoryItem(
            user="What is discussed in this video?",
            robot="The video discusses machine learning applications."
        )
    ],
    stream=True
)

# Process streaming response
for line in streaming_response.iter_lines():
    if line:
        # Handle streaming data
        # Format: data: {"data":{"msg":"I'm the assistant's partial response"}}
        print(line.decode('utf-8'))
```

## Video Status Codes

Video processing status can be one of:
- `PARSE`: Video is being processed or processing succeeded
- `UNPARSE`: Video has not been processed 
- `PARSE_ERROR` or `FAIL`: Video processing failed

## Pydantic Models

The client uses Pydantic models for request and response validation:

- `VideoInfo`: Basic information about a video
- `UploadResponse`: Response from video upload endpoint
- `VideoListResponse`: Response from video list endpoint
- `MetadataVideoInfo`: Video information in metadata search results
- `MetadataSearchResponse`: Response from metadata search endpoint
- `TranscriptionItem`: Individual transcription item
- `TranscriptionResponse`: Response from transcription endpoint
- `TaskResponse`: Response from task submission endpoint
- `SearchResponse`: Response from search endpoint

These models provide:
- Runtime type checking
- Data validation
- IDE autocompletion support
- Clear documentation of expected data structures

## Examples

Check the `main.py` file for more comprehensive examples of how to use the client.

## API Status Codes

- `PARSE`: Video processing successful/in progress
- `UNPARSE`: Video processing pending
- `PARSE_ERROR` or `FAIL`: Video processing failed

## Feedback (prioritized)

### High
- [ ] No org features. I cannot have separate datasets for separate customers/projects. 
- [ ] Query results seem to come back in an unsorted fashion (actually sorted by date added it seems)
    - [ ] I don't see a score for how good a search result is. As such, I cannot sort them on my end.
- [ ] I cannot upload from cloud storage. I have to have the file in my local file system

### Medium
- [ ] I cannot choose how many results I want in a query so I end up getting way too much.
- [ ] The `searchDB` endpoint actually supports searching for video names but it's not docummented. A proper documentation for what's allows would be necessary. Would also like to be able to search via `videoNo` which does not seem to work.
- [ ] The `CallBackUri` for video upload and transcription doesn't seem to work. See `upload_with_callback.py`

### Low
- [ ] `VIDEO/AUDIO` transcription type doesn't seem to work for transcription. Only the uni-modal `AUDIO` and `VIDEO`. `VIDEO/AUDIO` is listed in the [docs](https://docs.openinterx.com/MAVI-API/Transcription-video#request-example) as an option.
- [ ] [Documentation](https://docs.openinterx.com/MAVI-API/Transcription-video#response-example-1) says that there's an `id` property on transcriptions wich is not correct.
- [ ] It's generally very hard to figure out what I am allowed to do and what I'm not allowed to do. A more structured API documentation would be nice. Like building it with swagger or whatever.
- [ ] There are many typos in the documentation.

Certainly feels like the underlying "AI-tech" is solid. Will put it to the test soon.