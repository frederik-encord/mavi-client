from mavi_client import MaviClient
import typer
from datetime import datetime
from click import confirm
from utils import select_videos, print_table


def main(
    start: datetime | None = typer.Option(None, help="Start upload time to filter by"),
    end: datetime | None = typer.Option(None, help="End upload time to filter by"),
    video_name: str | None = typer.Option(None, help="Video name to filter by"),
):
    client = MaviClient()
    videos = client.search_metadata(
        page=1, page_size=1000, start_time=start, end_time=end, video_name=video_name
    ).data.videoData
    videos_found = len(videos)
    if not videos_found:
        print("No videos found")
        raise typer.Exit()

    print(f"Found {len(videos)} videos:")
    print_table(videos)

    if not confirm("Are you sure you want to delete these videos?"):
        if not confirm("Select from the list of videos?"):
            raise typer.Abort()
        videos = select_videos(client, videos=videos, return_all=True)
        if not confirm("Are you sure you want to delete these videos?"):
            raise typer.Abort()

    print("Deleting videos...")
    print("")
    for i, video in enumerate(videos):
        print(
            f"\rDeleting [{i}/{len(videos)}] {video.videoName} ({video.videoNo})",
            end="",
        )
        client.delete_videos([video.videoNo])
    print("")
    print("Done!")


if __name__ == "__main__":
    typer.run(main)
