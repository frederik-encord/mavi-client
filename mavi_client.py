import os
from pathlib import Path
import requests
import json
from typing import (
    List,
    Dict,
    Any,
    Optional,
    Union,
    Literal,
    overload,
    Callable,
    TypeVar,
    Type,
    ParamSpec,
)
from functools import wraps
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime, timezone

from enums import VideoStatus, TranscriptionType, TranscriptionStatus
# Pydantic models for API responses


class BaseResponse(BaseModel):
    code: str = Field(..., description="Status code")
    msg: str = Field(..., description="Status message")


RT = TypeVar("RT", bound=BaseResponse)
P = ParamSpec("P")


class VideoInfo(BaseModel):
    """Basic information about a video."""

    videoNo: str = Field(..., description="Unique video identifier")
    videoName: str = Field(..., description="Name of the video")
    videoStatus: VideoStatus = Field(..., description="Status of the video processing")
    uploadTime: datetime = Field(..., description="Time when the video was uploaded")
    duration: Optional[float] = Field(
        None, description="Duration of the video in seconds"
    )


class UploadResponse(BaseResponse):
    """Response from video upload endpoint."""

    data: VideoInfo = Field(..., description="Video information")


class VideoListData(BaseModel):
    """Data model for video list response."""

    videos: List[VideoInfo] = Field([], description="List of videos")
    total: int = Field(..., description="Total number of videos")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Number of items per page")


class VideoListResponse(BaseResponse):
    """Response from video list endpoint."""

    data: VideoListData = Field(..., description="Paginated video list data")


class MetadataVideoInfo(BaseModel):
    """Video information in metadata search results."""

    videoNo: str = Field(..., description="Unique video identifier")
    videoName: str = Field(..., description="Name of the video")
    videoStatus: VideoStatus = Field(..., description="Status of the video processing")
    uploadTime: datetime = Field(..., description="Time when the video was uploaded")


class MetadataSearchData(BaseModel):
    """Data model for metadata search response."""

    page: int = Field(..., description="Current page number")
    current: int = Field(..., description="Current number of items")
    total: int = Field(..., description="Total number of videos")
    pageSize: int = Field(..., description="Number of items per page")
    videoData: List[MetadataVideoInfo] = Field(
        default_factory=list, description="List of video data"
    )


class MetadataSearchResponse(BaseResponse):
    """Response from metadata search endpoint."""

    data: MetadataSearchData = Field(..., description="Metadata search results")


class TranscriptionItem(BaseModel):
    """Individual transcription item."""

    startTime: int = Field(..., description="Start time in milliseconds")
    endTime: int = Field(..., description="End time in milliseconds")
    content: str = Field(..., description="Transcription content")


class TranscriptionData(BaseModel):
    """Data model for transcription response."""

    status: TranscriptionStatus = Field(..., description="Status of transcription task")
    type: TranscriptionType = Field(..., description="Type of transcription")
    videoNo: str = Field(..., description="Video identifier")
    taskNo: str = Field(..., description="Task identifier")
    transcriptions: List[TranscriptionItem] = Field(
        default_factory=list, description="List of transcription items"
    )


class TranscriptionResponse(BaseResponse):
    """Response from transcription endpoint."""

    data: TranscriptionData = Field(..., description="Transcription data")


class TranscriptionJobData(BaseModel):
    """Response from transcription job submission endpoint."""

    taskNo: str = Field(..., description="Job ID")


class TaskResponse(BaseResponse):
    """Response from task submission endpoint."""

    data: TranscriptionJobData = Field(..., description="Task data including taskNo")


class SearchResultsData(BaseModel):
    """Data model for search results."""

    videos: List[VideoInfo] = Field(
        default_factory=list, description="List of matching videos"
    )


class SearchResponse(BaseResponse):
    """Response from search endpoint."""

    data: SearchResultsData = Field(..., description="Search results data")


class ChatHistoryItem(BaseModel):
    """Chat history item for video chat."""

    robot: str = Field(..., description="Assistant response")
    user: str = Field(..., description="User message")


class VideoChatMessage(BaseModel):
    msg: str = Field(..., description="Robot Message")


class VideoChatResponse(BaseModel):
    """Response from video chat endpoint."""

    data: VideoChatMessage = Field(
        ..., description="Chat response data containing 'msg' field"
    )


class VideoClip(BaseModel):
    """Individual video clip from fragment search."""

    videoNo: str = Field(..., description="Unique video identifier")
    videoName: str = Field(..., description="Name of the video")
    videoStatus: VideoStatus = Field(..., description="Status of video processing")
    uploadTime: datetime = Field(..., description="Time when the video was uploaded")
    fragmentStartTime: float = Field(
        ..., description="Start time of the clip in seconds"
    )
    fragmentEndTime: float = Field(..., description="End time of the clip in seconds")
    duration: float = Field(..., description="Duration of the clip in seconds")


class VideoClipData(BaseModel):
    """Data model for video clip search results."""

    videos: List[VideoClip] = Field(
        default_factory=list, description="List of video clips"
    )


class VideoClipResponse(BaseResponse):
    """Response from video clip search endpoint."""

    data: VideoClipData = Field(..., description="Video clip search results")


class VideoDeleteResponse(BaseResponse):
    """Response from video delete endpoint."""

    ...


class ErrorResponse(BaseResponse):
    """Response from error endpoint."""

    ...


class MaviError(Exception):
    """Exception for MAVI API errors."""

    def __init__(self, response: ErrorResponse):
        self.message = f"{response.code}: {response.msg}"
        super().__init__(self.message)


def _handle_response(response: requests.Response) -> Dict[str, Any]:
    """
    Handle API responses and errors.

    Args:
        response: Response object from requests.

    Returns:
        Dictionary with the response data.

    Raises:
        Exception: If the response indicates an error.
    """
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code} - {response.text}")

    # Check if the response text starts with "data:" and remove it
    response_text = response.text
    if response_text.startswith("data:"):
        response_text = response_text[5:]

    try:
        data = json.loads(response_text)
        return data
    except json.JSONDecodeError as e:
        raise Exception(
            f"Failed to parse JSON response: {response_text[:100]}... - Error: {e}"
        )


def _try_model_validate(
    response: dict[str, Any], type_: Type[RT]
) -> RT | ErrorResponse:
    try:
        return type_.model_validate(response)
    except ValidationError:
        return ErrorResponse.model_validate(response)


def client_models(
    out_type: Type[RT],
) -> Callable[[Callable[P, requests.Response]], Callable[P, RT]]:
    def wrapper(func: Callable[P, requests.Response]) -> Callable[P, RT]:
        @wraps(func)
        def inner(*args: P.args, **kwargs: P.kwargs) -> RT:
            response = func(*args, **kwargs)
            json_response = _handle_response(response)
            parsed = _try_model_validate(json_response, out_type)
            if isinstance(parsed, ErrorResponse):
                raise MaviError(parsed)
            return parsed

        return inner

    return wrapper


class MaviClient:
    """Client for interacting with the MAVI API."""

    BASE_URL = "https://mavi-backend.openinterx.com"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the MAVI API client.

        Args:
            api_key: Optional API key. If not provided, it will be loaded from environment variables.
        """
        load_dotenv()  # Load environment variables from .env file
        self.api_key = api_key or os.getenv("MAVI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "API key is required. Provide it as an argument or set MAVI_API_KEY in .env file."
            )

        self.headers = {"Authorization": self.api_key}

    @client_models(out_type=UploadResponse)
    def upload_video(
        self,
        file_path: str | Path,
        custom_name: Optional[str] = None,
        callback_uri: Optional[str] = None,
        progress_callback: Optional[Callable[[int], None]] = None,
    ) -> requests.Response:
        """
        Upload a video to the MAVI platform.

        Args:
            file_path: Path to the video file.
            custom_name: Optional custom name for the video.
            callback_uri: Optional callback URL for receiving status notifications.
                          Must be publicly accessible.
            progress_callback: Optional callback function that receives upload progress (0-100).

        Returns:
            UploadResponse: Validated response containing video information.

        Note:
            The video must be encoded in h264, h265, vp9, or hevc format.
            If you intend to use audio transcription, the video must contain an audio track.
        """
        url = f"{self.BASE_URL}/api/serve/video/upload"

        # Prepare file data
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Video file not found: {file_path}")

        # Determine file name if custom name is not provided
        if custom_name is None:
            custom_name = os.path.basename(file_path)

        # Prepare request parameters
        # Open file for upload
        with open(file_path, "rb") as file:
            # Get file size for progress tracking
            file_size = os.path.getsize(file_path)

            # Create a custom monitor class for tracking upload progress
            class ProgressMonitor:
                def __init__(self, file_obj, total_size, callback):
                    self.file_obj = file_obj
                    self.total_size = total_size
                    self.callback = callback
                    self.bytes_read = 0

                def read(self, size=-1) -> bytes:
                    chunk = self.file_obj.read(size)
                    if chunk:
                        self.bytes_read += len(chunk)
                        if self.callback:
                            progress = int((self.bytes_read / self.total_size) * 100)
                            self.callback(progress)
                    return chunk

            # Create monitored file object if progress callback provided
            if progress_callback:
                file_monitor = ProgressMonitor(file, file_size, progress_callback)
                files: dict[str, tuple[str, Any, str]] = {
                    "file": (custom_name, file_monitor, "video/mp4")
                }
            else:
                files = {"file": (custom_name, file, "video/mp4")}

            # Set up parameters if callback_uri is provided
            params = {}
            if callback_uri:
                params["callBackUri"] = callback_uri

            # Make the API request
            response = requests.post(
                url,
                headers=self.headers,
                files=files,
                json=params,
                params=params,
            )
        return response

    @client_models(out_type=TaskResponse)
    def submit_transcription(
        self,
        video_no: str,
        transcription_type: Union[TranscriptionType, str],
        callback_uri: Optional[str] = None,
    ) -> requests.Response:
        """
        Submit a transcription task for a video.

        Args:
            video_no: The unique identifier of the video.
            transcription_type: Type of transcription (AUDIO, VIDEO, or AUDIO/VIDEO).
            callback_uri: Optional URL for receiving results via callback.

        Returns:
            TaskResponse: Validated response containing task information.
        """
        url = f"{self.BASE_URL}/api/serve/video/subTranscription"

        # Convert enum to string if needed
        if isinstance(transcription_type, TranscriptionType):
            transcription_type = transcription_type.value

        data = {"videoNo": video_no, "type": transcription_type}

        if callback_uri:
            data["callBackURI"] = callback_uri

        return requests.post(url, headers=self.headers, json=data)

    @client_models(out_type=TranscriptionResponse)
    def get_transcription(self, task_no: str) -> requests.Response:
        """
        Get the transcription content for a completed task.

        Args:
            task_no: The unique identifier of the transcription task.

        Returns:
            TranscriptionResponse: Validated response containing transcription data.
        """
        url = f"{self.BASE_URL}/api/serve/video/getTranscription"
        params = {"taskNo": task_no}

        return requests.get(url, headers=self.headers, params=params)

    # Search
    @client_models(out_type=SearchResponse)
    def search_videos(self, search_value: str) -> requests.Response:
        """
        Search for videos using natural language.

        Args:
            search_value: Natural language search query.

        Returns:
            SearchResponse: Validated response containing search results.
        """
        url = f"{self.BASE_URL}/api/serve/video/searchAI"
        data = {"searchValue": search_value}

        return requests.post(url, headers=self.headers, json=data)

    @client_models(out_type=VideoClipResponse)
    def search_video_clips(
        self, video_nos: List[str], search_value: str
    ) -> requests.Response:
        """
        Search for specific clips within videos.

        Args:
            video_nos: List of video identifiers to search within.
            search_value: Natural language search query.

        Returns:
            VideoClipResponse: Validated response containing video clip search results.
        """
        url = f"{self.BASE_URL}/api/serve/video/searchVideoFragment"
        data = {"videoNos": video_nos, "searchValue": search_value}

        return requests.post(url, headers=self.headers, json=data)

    # Metadata filtering and pagination
    @client_models(out_type=MetadataSearchResponse)
    def search_metadata(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        video_status: Optional[Union[VideoStatus, str]] = None,
        video_name: Optional[str] = None,
        page: int = 1,
        page_size: int = 100,
    ) -> requests.Response:
        """
        Search for video metadata using filtering parameters.

        Args:
            start_time: Optional timestamp (in milliseconds) for filtering by upload time (start).
            end_time: Optional timestamp (in milliseconds) for filtering by upload time (end).
            video_status: Optional status filter (PARSE, UNPARSE, FAIL).
            video_name: Optional video name for filtering by video name.
            page: Page number for pagination (default: 1).
            page_size: Number of results per page (default: 100).

        Returns:
            MetadataSearchResponse: Validated response containing metadata search results.
        """
        url = f"{self.BASE_URL}/api/serve/video/searchDB"

        # Prepare parameters
        params: dict[str, str | int] = {
            "page": page,
            "pageSize": page_size,
        }

        # Add optional filters if provided
        if start_time is not None:
            # Make sure the datetime is timezone-aware (UTC)
            if start_time.tzinfo is None:
                start_time = start_time.replace(tzinfo=timezone.utc)
            else:
                start_time = start_time.astimezone(timezone.utc)

            params["startTime"] = str(int(start_time.timestamp() * 1000))

        if end_time is not None:
            # Make sure the datetime is timezone-aware (UTC)
            if end_time.tzinfo is None:
                end_time = end_time.replace(tzinfo=timezone.utc)
            else:
                end_time = end_time.astimezone(timezone.utc)

            params["endTime"] = str(int(end_time.timestamp() * 1000))

        if video_status is not None:
            # Convert enum to string if needed
            if isinstance(video_status, VideoStatus):
                video_status = video_status.value
            params["videoStatus"] = video_status

        if video_name is not None:
            params["videoName"] = video_name

        # Make the API request
        return requests.get(url, headers=self.headers, params=params)

    @client_models(out_type=VideoDeleteResponse)
    def delete_videos(self, video_nos: List[str]) -> requests.Response:
        """
        Delete videos and all associated data from the MAVI platform.

        Args:
            video_nos: List of video identifiers to delete.

        Returns:
            VideoDeleteResponse: Validated response containing operation status.

        Note:
            This operation permanently deletes all raw and derived data for the specified videos.
            There is a rate limit of maximum 500 videos per call.
        """
        if len(video_nos) > 500:
            raise ValueError(
                "Cannot delete more than 500 videos in a single call due to API rate limits."
            )

        url = f"{self.BASE_URL}/api/serve/video/delete"

        return requests.delete(url, headers=self.headers, json=video_nos)

    @overload
    def video_chat(
        self,
        video_nos: List[str],
        message: str,
        history: Optional[List[ChatHistoryItem]] = None,
        stream: Literal[True] = True,
    ) -> requests.Response: ...

    @overload
    def video_chat(
        self,
        video_nos: List[str],
        message: str,
        history: Optional[List[ChatHistoryItem]] = None,
        stream: Literal[False] = False,
    ) -> VideoChatResponse: ...

    def video_chat(
        self,
        video_nos: List[str],
        message: str,
        history: Optional[List[ChatHistoryItem]] = None,
        stream: bool = False,
    ) -> Union[VideoChatResponse, requests.Response]:
        """
        Interact with an LLM AI assistant based on the context of one or multiple videos.

        Args:
            video_nos: List of video identifiers to chat about
            message: User query or prompt
            history: Optional chat history for context (empty for new conversations)
            stream: Whether to stream the response (True) or get a complete response (False)

        Returns:
            If stream=False: VideoChatResponse object containing the assistant's response
            If stream=True: Raw response object for streaming (caller must handle streaming)
        """
        url = f"{self.BASE_URL}/api/serve/video/chat"

        # Prepare request data
        data = {
            "videoNos": video_nos,
            "message": message,
            "history": [h.model_dump() for h in history] if history else [],
            "stream": stream,
        }
        # Make API request
        try:
            response = requests.post(url, headers=self.headers, json=data)
        except Exception as e:
            import traceback

            traceback.print_exc()
            raise e

        # If streaming, return the raw response for the caller to handle
        if stream:
            return response

        # Otherwise, process and validate the response
        json_response = _handle_response(response)
        return VideoChatResponse.model_validate(json_response)
