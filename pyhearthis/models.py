from typing import NamedTuple
from urllib.parse import urlencode


def is_not_empty(item) -> bool:
    if item is None:
        return ""

    if isinstance(item, str):
        return len(item.strip()) > 0

    return True


def as_query_param(item: NamedTuple) -> str:
    dictionary = {k: v for (k, v) in item._asdict().items() if is_not_empty(v)}
    return urlencode(dictionary)


def get_value(key, value):
    if key == "downloadable":
        return True if (value == 1) or value == "1" else False

    if key == "bpm":
        return float(value)

    if (
        key == "id"
        or key == "user_id"
        or key == "duration"
        or key == "release_timestamp"
        or key == "track_id"
        or key == "set"
        or key == "set_id"
        or "_count" in key
    ):
        # TODO handle counts field
        if value is None:
            return int(0)

        return int(value)

    return value


def cast_dict(items: dict, omit_empty: bool = False) -> dict:
    if omit_empty:
        return {k: get_value(k, v) for (k, v) in items.items() if is_not_empty(v)}

    return {k: get_value(k, v) for (k, v) in items.items()}


def cast_list(items: dict) -> list:
    return list(map(cast_dict, items))


class LoggedinUser(NamedTuple):
    id: str
    permalink: str
    username: str
    caption: str
    uri: str
    permalink_url: str
    thumb_url: str
    avatar_url: str
    p_url: str
    background_url: str
    description: str
    geo: str
    track_count: str
    playlist_count: str
    likes_count: str
    followers_count: str
    following_count: str
    counts: dict
    following: bool
    premium: bool
    allow_push: int
    is_fan: bool
    featured_sound: str
    email: str
    locale: str
    secret: str
    key: str


class User(NamedTuple):
    id: int
    permalink: str
    username: str
    uri: str
    permalink_url: str
    avatar_url: str
    caption: str = ""


class Category(NamedTuple):
    id: str
    name: str
    url: str
    api_url: str


class SingleTrack(NamedTuple):
    id: str
    private: str
    created_at: str
    release_date: str
    release_timestamp: int
    unix_created_at: int
    update_timestamp: int
    user_id: str
    duration: str
    permalink: str
    description: str
    geo: str
    geopoint: list[float]
    tags: str
    tags_arr: list[str]
    taged_artists: str
    taged_artists_arr: list[str]
    subcategories_arr: list[str]
    bpm: str
    key: str
    license: str
    version: str
    type: str
    downloadable: str
    genre: str
    genre_slush: str
    genre_own: str
    title: str
    uri: str
    permalink_url: str
    thumb: str
    thumb_hires: str
    artwork_url: str
    artwork_url_retina: str
    background_url: str
    waveform_data: str
    waveform_data_json: str
    waveform_url: str
    user: dict
    counts: dict
    stream_url: str
    preview_url: str
    download_url: str
    download_filename: str
    transcript: str
    features: str
    related: str
    playback_count: str
    download_count: str
    favoritings_count: str
    reshares_count: str
    comment_count: str
    played: bool
    favorited: bool
    liked: bool
    reshared: bool
    is_fan: bool
    fan_exclusive_play: int
    fan_exclusive_download: int
    is_live: bool
    is_live_video: bool
    video_stream: str


class Playlist(NamedTuple):
    id: int
    user_id: int
    permalink: str
    title: str
    description: str
    privat: bool
    uri: str
    permalink_url: str
    thumb: str
    artwork_url: str
    track_count: int
    user: User


class SingleArtist(NamedTuple):
    id: int
    permalink: str
    username: str
    uri: str
    permalink: str
    permalink_url: str
    avatar_url: str
    background_url: str
    description: str
    track_count: int
    playlist_count: int
    likes_count: int
    followers_count: int
    following: bool
    following_count: int
    premium: bool
    allow_push: int
    geo: str
    p_url: str
    avatar_url: str
    thumb_url: str
    caption: str
