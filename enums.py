from enum import Enum


class VideoStatus(Enum):
    """Video processing status in the MAVI API."""

    PARSE = "PARSE"  # Success/Processing
    UNPARSE = "UNPARSE"  # Pending
    PARSE_ERROR = "PARSE_ERROR"  # Failure
    FAIL = "FAIL"  # Failure (alternative name in documentation)


class TranscriptionType(Enum):
    """Type of transcription to perform."""

    AUDIO = "AUDIO"
    VIDEO = "VIDEO"
    AUDIO_VIDEO = "AUDIO/VIDEO"


class TranscriptionStatus(Enum):
    """Status of transcription task."""

    FINISH = "FINISH"
    UNFINISHED = "UNFINISHED"
