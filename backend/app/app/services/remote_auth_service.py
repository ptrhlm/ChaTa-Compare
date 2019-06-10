import requests

from typing import Optional
from pydantic import BaseModel
from app.core import config


class RemoteUser(BaseModel):
    id: int
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    is_annotator: bool
    is_superannotator: bool
    token: str


def remote_authenticate(username: str, password: str) -> Optional[RemoteUser]:
    auth_endpoint = config.REMOTE_AUTH_ENDPOINT
    credentials = {
        "username": username,
        "password": password,
    }

    response = requests.post(
        f"{auth_endpoint}",
        json=credentials,
    )
    user = response.json()
    if response.status_code == 200:
        user = RemoteUser(**user)
        return user  # type: ignore
    else:
        return None
