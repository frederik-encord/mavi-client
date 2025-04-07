from mavi_client import MaviClient
from dotenv import load_dotenv
import typer
from rich import print as rprint
from rich.table import Table


def main(query: str):
    client = MaviClient()
    videos = client.search_videos(query).data.videos
    rprint(f"Found [blue]{len(videos)}[/blue] videos for query: [cyan]{query}[/cyan]")
    table = Table(title="Search Results")
    table.add_column("Video Name")
    table.add_column("Upload Time")

    for video in videos:
        table.add_row(video.videoName, video.uploadTime.strftime("%Y-%m-%d %H:%M:%S"))

    rprint(table)


if __name__ == "__main__":
    load_dotenv()
    typer.run(main)
