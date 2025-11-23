import yt_dlp
import asyncio
from concurrent.futures import ProcessPoolExecutor
import os

POOL = ProcessPoolExecutor(max_workers=8)
import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
COOKIES_PATH = os.path.join(BASE_DIR, "cookies.txt")

COOKIES_PATH = "cookies.txt"

def is_url(text: str):
    return text.startswith("http://") or text.startswith("https://")


def build_video_dict(info):
    if not info:
        raise ValueError("Empty info received")

    thumbnail = None
    thumbs = info.get("thumbnails", [])
    preferred_keys = ["maxres", "sd", "hq", "mq"]

    for key in preferred_keys:
        for t in thumbs:
            url = t.get("url", "")
            if key in url and "webp" not in url:
                thumbnail = url
                break
        if thumbnail:
            break

    if not thumbnail:
        for t in thumbs:
            url = t.get("url", "")
            if url and "webp" not in url:
                thumbnail = url
                break

    if not thumbnail:
        thumbnail = info.get("thumbnail")

    formats = info.get("formats", [])
    stream_url = None
    preferred_res = ["720", "480", "360", "240"]

    for res in preferred_res:
        for f in formats:
            height = f.get("height")
            url = f.get("url")
            if height and url and res in str(height):
                if "m3u8" in (f.get("protocol") or "") or ".m3u8" in url:
                    stream_url = url
                    break
        if stream_url:
            break

    if not stream_url:
        for f in formats:
            if "m3u8" in (f.get("protocol") or "") and f.get("url"):
                stream_url = f["url"]
                break

    if not stream_url:
        raise ValueError("No playable m3u8 stream found")

    return {
        "id": info.get("id"),
        "url": info.get("webpage_url"),
        "title": info.get("title"),
        "duration": info.get("duration"),
        "thumbnail": thumbnail,
        "stream_url": stream_url,
    }


def extract_from_query(query: str):
    try:
        opts = {
            "quiet": True,
            "noplaylist": True,
            "skip_download": True,
            "cookiefile": COOKIES_PATH,
        }

        with yt_dlp.YoutubeDL(opts) as ydl:
            data = ydl.extract_info(f"ytsearch1:{query}", download=False)

        if not data or not data.get("entries"):
            raise ValueError("No search results found")

        return build_video_dict(data["entries"][0])

    except Exception as e:
        raise RuntimeError(f"Search extract failed: {e}")


def extract_from_url(url: str):
    try:
        opts = {
            "quiet": True,
            "noplaylist": True,
            "skip_download": True,
            "cookiefile": COOKIES_PATH,
        }

        with yt_dlp.YoutubeDL(opts) as ydl:
            data = ydl.extract_info(url, download=False)

        if not data:
            raise ValueError("Failed to extract URL info")

        return build_video_dict(data)

    except Exception as e:
        raise RuntimeError(f"URL extract failed: {e}")


def _router(text: str):
    return extract_from_url(text) if is_url(text) else extract_from_query(text)


async def search_video(text: str):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(POOL, _router, text)