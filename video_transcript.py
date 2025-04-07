from mavi_client import MaviClient, TranscriptionType, TranscriptionStatus
import typer
from rich import print as rprint
from rich.progress import Progress, TextColumn, TimeElapsedColumn, SpinnerColumn
from utils import select_videos
import time


def main():
    client = MaviClient()
    videos = select_videos(client, return_all=True)
    video = videos[0]
    submit_response = client.submit_transcription(
        video.videoNo, TranscriptionType.AUDIO
    )
    task_no = submit_response.data.taskNo

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task("Waiting for transcription", total=1)
        while True:
            response = client.get_transcription(task_no)
            if response.data.status == TranscriptionStatus.FINISH:
                break
            time.sleep(1)
        progress.update(task, advance=1)

    rprint(response.data.transcriptions)


if __name__ == "__main__":
    typer.run(main)
