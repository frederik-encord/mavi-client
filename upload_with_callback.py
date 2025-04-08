from mavi_client import MaviClient, TranscriptionType
import time
import typer


def main():
    client = MaviClient()

    CALLBACK_URI = "https://frederik--mavi-callback-endpoint-callback-dev.modal.run/"
    res = client.upload_video(
        file_path="/Users/fhv/data/originals/panda-70m/test_split/0000000_00000.mp4",
        custom_name="test.mp4",
        callback_uri=CALLBACK_URI,
    ).data

    time.sleep(3)

    res2 = client.submit_transcription(
        res.videoNo,
        TranscriptionType.VIDEO,
        callback_uri=CALLBACK_URI,
    ).data

    print(res)
    print(res2)

    time.sleep(3)

    transcription_res = client.get_transcription(res2.taskNo).data

    print(transcription_res)


if __name__ == "__main__":
    typer.run(main)
