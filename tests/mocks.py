import asyncio
import os
import json
from urllib.parse import urlencode
from pyhearthis.models import Category, LoggedinUser, Playlist, SingleTrack


class RequestContextManagerMock:

    return_values = dict()
    post_values = dict()

    def __init__(self, query, data=None) -> None:
        self.query = query
        RequestContextManagerMock.post_values[query] = data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.query in RequestContextManagerMock.return_values:
            RequestContextManagerMock.return_values.pop(self.query, None)

    async def text(self) -> str:
        await asyncio.sleep(0)
        if self.query in RequestContextManagerMock.return_values:
            data = RequestContextManagerMock.return_values[self.query]
            if isinstance(data, dict):
                return json.dumps(data)
            if isinstance(data, list):
                return json.dumps(data)

            return data

        return ""

    async def json(self) -> str:
        await asyncio.sleep(0)
        if self.query in RequestContextManagerMock.return_values:
            return RequestContextManagerMock.return_values[self.query]

        return dict()

    @property
    def status(self) -> int:
        return 200

    @property
    def content_type(self) -> str:
        return "text/html"

    @staticmethod
    def with_return_value(url: str, response, **kwargs):
        params = ""
        if len(kwargs) > 0:
            params = urlencode(kwargs)
            url = f"{url}?{params}"

        RequestContextManagerMock.return_values[url] = response
        return RequestContextManagerMock

    @staticmethod
    def with_json_response(url: str, json_file: str, **kwargs):
        file = os.path.abspath(os.path.join(os.path.dirname(__file__), "response_data", json_file))
        with open(file, 'r') as json_data:
            data = json_data.read()

        response = json.loads(data)
        return RequestContextManagerMock.with_return_value(url, response, **kwargs)

    @staticmethod
    def pop_post_data_for_url(url: str) -> dict:
        return RequestContextManagerMock.post_values.pop(url, None)


def replace_key(dictionary: dict, old_key: str, new_key: str) -> None:
    if old_key not in dictionary:
        return

    data = dictionary[old_key]
    dictionary.pop(old_key, None)
    dictionary[new_key] = data


def create_logged_in_user():
    file = os.path.abspath(os.path.join(os.path.dirname(__file__), "response_data", 'login_response.json'))
    with open(file, 'r') as json_data:
        data = json_data.read()

    response = json.loads(data)
    replace_key(response, "720p_url", "p_url")
    return LoggedinUser(**response)


def create_single_track() -> SingleTrack:
    file = os.path.abspath(os.path.join(os.path.dirname(__file__), "response_data", 'single_track.json'))
    with open(file, 'r') as json_data:
        data = json_data.read()

    response = json.loads(data)
    return SingleTrack(**response)


def create_playlist() -> Playlist:
    file = os.path.abspath(os.path.join(os.path.dirname(__file__), "response_data", 'single_playlist.json'))
    with open(file, 'r') as json_data:
        data = json_data.read()

    response = json.loads(data)
    return Playlist(**response)


def create_category() -> Category:
    file = os.path.abspath(os.path.join(os.path.dirname(__file__), "response_data", 'single_category.json'))
    with open(file, 'r') as json_data:
        data = json_data.read()

    response = json.loads(data)
    return Category(**response)
