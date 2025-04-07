from typing import overload, Literal
from mavi_client import MaviClient, MetadataVideoInfo, VideoClip, VideoInfo
from rich.table import Table
from InquirerPy import inquirer as i
from InquirerPy.base.control import Choice
from rich import print as rprint


@overload
def select_videos(
    client: MaviClient,
    *,
    videos: list[MetadataVideoInfo] | None = None,
    return_all: Literal[False] = False,
) -> list[str]: ...


@overload
def select_videos(
    client: MaviClient,
    *,
    videos: list[MetadataVideoInfo] | None = None,
    return_all: Literal[True] = True,
) -> list[MetadataVideoInfo]: ...


def select_videos(
    client: MaviClient,
    *,
    videos: list[MetadataVideoInfo] | None = None,
    return_all: bool = False,
) -> list[str] | list[MetadataVideoInfo]:
    """Select videos for chat"""
    if videos is None:
        videos = client.search_metadata(page=1, page_size=1000).data.videoData

    selected = i.fuzzy(
        message="Select videos",
        choices=[
            Choice(video if return_all else video.videoNo, video.videoName)
            for video in videos
        ],
        multiselect=True,
        vi_mode=True,
    ).execute()
    return selected


def print_table(videos: list[MetadataVideoInfo] | list[VideoInfo]):
    table = Table(title="Videos")
    table.add_column("Video Name")
    table.add_column("Uploaded At")
    table.add_column("Video No")
    table.add_column("Video Status")
    for video in videos:
        table.add_row(
            f"[bold]{video.videoName}[/bold]",
            f"[green]{video.uploadTime.strftime('%Y-%m-%d %H:%M:%S')}[/green]",
            f"[blue]{video.videoNo}[/blue]",
            f"[purple]{video.videoStatus.value}[/purple]",
        )
    rprint(table)


def print_clips(clips: list[VideoClip]):
    table = Table(title="Video Clips")
    table.add_column("Video Name")
    table.add_column("Upload Time")
    table.add_column("Start Time")
    table.add_column("End Time")
    table.add_column("Duration")

    for clip in clips:
        table.add_row(
            clip.videoName,
            clip.uploadTime.strftime("%Y-%m-%d %H:%M:%S"),
            f"{clip.fragmentStartTime:.2f}",
            f"{clip.fragmentEndTime:.2f}",
            f"{clip.duration:,.2f}",
        )

    rprint(table)
