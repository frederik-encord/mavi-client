from mavi_client import MaviClient
from dotenv import load_dotenv
import typer
from rich import print as rprint
from utils import select_videos, print_clips


def main(query: str):
    client = MaviClient()
    videos = select_videos(client)
    response = client.search_video_clips(videos, query)
    clips = response.data.videos
    rprint(f"Found [blue]{len(clips)}[/blue] clips for query: [cyan]{query}[/cyan]")
    print_clips(clips)


if __name__ == "__main__":
    load_dotenv()
    typer.run(main)
