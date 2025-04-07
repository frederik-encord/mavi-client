from mavi_client import MaviClient, VideoStatus, MetadataVideoInfo
from dotenv import load_dotenv
from collections import defaultdict
import typer
from datetime import datetime

from utils import print_table


def main(
    start_time: datetime | None = typer.Option(
        None, "--start", help="Start upload time for filtering videos"
    ),
    end_time: datetime | None = typer.Option(
        None, "--end", help="End upload time for filtering videos"
    ),
    video_name: str | None = typer.Option(
        None, "--name", help="Video name for filtering videos"
    ),
    video_status: VideoStatus | None = typer.Option(
        None, "--status", help="Video status for filtering videos"
    ),
    page_size: int = typer.Option(
        100, "--page-size", help="Page size for filtering videos"
    ),
    page: int = typer.Option(1, "--page", help="Page number for filtering videos"),
):
    client = MaviClient()
    response = client.search_metadata(
        page=page,
        page_size=page_size,
        video_name=video_name,
        start_time=start_time,
        end_time=end_time,
        video_status=video_status,
    )
    videos = response.data.videoData
    status_dict: dict[VideoStatus, list[MetadataVideoInfo]] = defaultdict(list)

    for video in videos:
        status_dict[video.videoStatus].append(video)

    for status, videos in status_dict.items():
        print(f"Videos with status: {status.value}")
        print_table(videos)


if __name__ == "__main__":
    load_dotenv()
    typer.run(main)
