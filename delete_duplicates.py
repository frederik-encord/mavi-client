from mavi_client import MaviClient, MetadataVideoInfo
import typer
from click import confirm

from utils import select_videos


def main():
    client = MaviClient()
    first_page = client.search_metadata(page=1, page_size=1000).data
    total = first_page.total
    videos = first_page.videoData
    while len(videos) < total:
        next_page = client.search_metadata(
            page=len(videos) // 1000 + 1, page_size=1000
        ).data
        videos.extend(next_page.videoData)

    duplicates: dict[str, list[MetadataVideoInfo]] = {}
    for video in videos:
        duplicates.setdefault(video.videoName, []).append(video)

    to_select_from = []
    for video_name, videos in duplicates.items():
        if len(videos) > 1:
            to_select_from.extend(videos[1:])

    if not to_select_from:
        print("No duplicates found")
        return

    selected_videos = select_videos(client, videos=to_select_from, return_all=True)
    if not confirm(f"Are you sure you want to delete {len(selected_videos)} videos?"):
        raise typer.Abort()

    print("Deleting videos...")
    print("")
    for video in selected_videos:
        print(f"\rDeleting {video.videoName} ({video.videoNo})", end="")
        client.delete_videos([video.videoNo])
    print("")
    print("Done!")


if __name__ == "__main__":
    typer.run(main)
