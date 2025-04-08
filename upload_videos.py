from mavi_client import MaviClient, VideoInfo
import os
import time
from dotenv import load_dotenv
from pathlib import Path
import typer
from datetime import datetime, timezone, timedelta
from rich.progress import Progress

from utils import print_table


def upload_example(client: MaviClient, video_path: Path, video_name: str) -> VideoInfo:
    """
    Example function to demonstrate video upload and processing.

    Args:
        client: An initialized MaviClient instance
        video_path: Path to the video file to upload
    """
    if not os.path.exists(video_path):
        raise ValueError(f"Error: Video file not found at {video_path}")

    with Progress() as progress:
        task = progress.add_task("Uploading video", total=100)
        upload_response = client.upload_video(
            file_path=video_path,
            custom_name=video_name,
            progress_callback=lambda p: progress.update(task, completed=p),
        )
        return upload_response.data


def main(
    video_dir: Path = typer.Argument(
        ..., help="Path to the directory containing videos"
    ),
    limit_per_minute: int = typer.Option(
        10, help="Limit the number of videos uploaded per minute"
    ),
):
    """
    Demonstrate how to use the MAVI API client to upload videos from directory.
    """
    video_dir = video_dir.expanduser().resolve()

    # Initialize client with API key from .env file
    client = MaviClient()
    start_time = datetime.now(timezone.utc)

    # Get total number of videos first
    page_size = 100
    initial_response = client.search_metadata(page=1, page_size=page_size)
    total_videos = initial_response.data.total

    # Calculate number of pages needed
    total_pages = (total_videos + page_size - 1) // page_size

    # Collect all video names across pages
    latest_upload = datetime.now(tz=timezone.utc) - timedelta(seconds=60)
    existing_video_names: set[str] = set()
    for page in range(1, total_pages + 1):
        videos = client.search_metadata(page=page, page_size=page_size).data.videoData
        if not videos:
            break
        existing_video_names.update(v.videoName for v in videos)
        latest_upload = max(
            latest_upload, max(videos, key=lambda v: v.uploadTime).uploadTime
        )

    new_videos: list[VideoInfo] = []
    limit_count = 0
    for video in video_dir.glob("*.mp4"):
        if Path(video.name).stem in existing_video_names:
            print(f"Skipping {video.name} because it already exists")
            continue
        time_since_limit = datetime.now(tz=timezone.utc) - latest_upload

        if limit_count >= limit_per_minute:
            print(f"Sleeping for {60 - time_since_limit.seconds} seconds")
            time.sleep(60 - time_since_limit.seconds)
            limit_count = 0
            latest_upload = datetime.now(tz=timezone.utc)

        try:
            new_videos.append(upload_example(client, video, video.name))
        except Exception as e:
            to_sleep = 60 - time_since_limit.seconds
            print(
                f"Error uploading {video.name}: {e} waiting for {to_sleep} seconds and trying again"
            )
            time.sleep(to_sleep)
            limit_count = 0
            continue

        limit_count += 1

    # List all videos with pagination
    print(f"Listing videos since {start_time}")
    videos_response = client.search_metadata(
        page=1, page_size=100, start_time=start_time
    )
    print(f"Total videos: {videos_response.data.total}")
    print(f"Current page: {videos_response.data.page}")
    print_table(videos_response.data.videoData)


if __name__ == "__main__":
    load_dotenv(".env")
    typer.run(main)
