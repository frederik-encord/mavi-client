"""
Example endpoint hosted on Modal for simplicity.
"""

import modal
from enums import VideoStatus
from pydantic import BaseModel

image = modal.Image.debian_slim().pip_install(
    "fastapi[standard]",
    "pydantic",
)
app = modal.App(name="mavi-callback-endpoint", image=image)


class CallbackRequest(BaseModel):
    videoNo: str
    clientId: str
    status: VideoStatus


@app.function()
@modal.fastapi_endpoint(
    docs=True,  # adds interactive documentation in the browser
    method="POST",
)
def callback(request: CallbackRequest):
    print(f"{request=}")
