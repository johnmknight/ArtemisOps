"""
ArtemisOps YouTube Streams Service
Scrapes YouTube channel /streams pages for live and upcoming streams.
Supports multiple channels (NASA, Spaceflight Now, etc.)
Returns structured data with video IDs, titles, status, and embed URLs.

Cache: 30 minutes
"""
import asyncio
import re
import json
import httpx
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# === Configuration ===

CHANNELS = [
    {"key": "nasa",     "label": "NASA",             "url": "https://www.youtube.com/@NASA/streams"},
    {"key": "sfnow",    "label": "Spaceflight Now",  "url": "https://www.youtube.com/@SpaceflightNowVideo/streams"},
]

CACHE_TTL_SECONDS = 1800  # 30 minutes
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

# === In-memory cache ===

_cache: Dict[str, Any] = {
    "streams": None,
    "fetched_at": None,
}


def _is_cache_valid() -> bool:
    if _cache["streams"] is None or _cache["fetched_at"] is None:
        return False
    age = (datetime.now(timezone.utc) - _cache["fetched_at"]).total_seconds()
    return age < CACHE_TTL_SECONDS


# === YouTube page parser ===

def _extract_initial_data(html: str) -> Optional[dict]:
    """
    YouTube embeds all page data in a var ytInitialData = {...}; block.
    Extract and parse it.
    """
    # Pattern 1: var ytInitialData = {...};
    match = re.search(r'var\s+ytInitialData\s*=\s*(\{.*?\});\s*</script>', html, re.DOTALL)
    if not match:
        # Pattern 2: window["ytInitialData"] = {...};
        match = re.search(r'window\["ytInitialData"\]\s*=\s*(\{.*?\});\s*</script>', html, re.DOTALL)
    if not match:
        logger.warning("Could not find ytInitialData in page HTML")
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse ytInitialData JSON: {e}")
        return None


def _parse_streams(data: dict) -> List[Dict[str, Any]]:
    """
    Walk ytInitialData to extract video entries from the streams tab.
    Returns list of stream dicts with id, title, status, viewers, scheduled time.
    """
    streams = []

    try:
        # Navigate: contents > twoColumnBrowseResultsRenderer > tabs
        tabs = (data.get("contents", {})
                .get("twoColumnBrowseResultsRenderer", {})
                .get("tabs", []))

        # Find the streams/live tab content
        grid_contents = None
        for tab in tabs:
            tab_renderer = tab.get("tabRenderer", {})
            tab_content = tab_renderer.get("content", {})

            # Could be richGridRenderer directly
            rgr = tab_content.get("richGridRenderer", {})
            if rgr.get("contents"):
                grid_contents = rgr["contents"]
                break

            # Or nested in sectionListRenderer
            slr = tab_content.get("sectionListRenderer", {})
            for section in slr.get("contents", []):
                isr = section.get("itemSectionRenderer", {})
                for item in isr.get("contents", []):
                    rgr = item.get("richGridRenderer", {}) or item.get("gridRenderer", {})
                    if rgr.get("contents") or rgr.get("items"):
                        grid_contents = rgr.get("contents") or rgr.get("items")
                        break
                if grid_contents:
                    break

        if not grid_contents:
            logger.warning("No grid contents found in ytInitialData")
            return streams

        for item in grid_contents:
            # richItemRenderer > content > videoRenderer
            renderer = (item.get("richItemRenderer", {})
                        .get("content", {})
                        .get("videoRenderer"))

            if not renderer:
                # Try gridVideoRenderer (older layout)
                renderer = item.get("gridVideoRenderer")

            if not renderer:
                continue

            video_id = renderer.get("videoId")
            if not video_id:
                continue

            # Title
            title_runs = renderer.get("title", {}).get("runs", [])
            title = title_runs[0].get("text", "") if title_runs else ""
            if not title:
                title = renderer.get("title", {}).get("simpleText", "")

            # Status: check badges and overlays for LIVE / UPCOMING
            status = "vod"  # default: past stream
            viewer_count = None
            scheduled_time = None

            # Check thumbnail overlays for live badge
            for overlay in renderer.get("thumbnailOverlays", []):
                style = (overlay.get("thumbnailOverlayTimeStatusRenderer", {})
                         .get("style", ""))
                if style == "LIVE":
                    status = "live"
                elif style == "UPCOMING":
                    status = "upcoming"

            # Check badges array
            for badge in renderer.get("badges", []):
                badge_style = (badge.get("metadataBadgeRenderer", {})
                               .get("style", ""))
                badge_label = (badge.get("metadataBadgeRenderer", {})
                               .get("label", ""))
                if "LIVE" in badge_style or "LIVE" in badge_label.upper():
                    status = "live"

            # Viewer count (for live streams)
            view_text = renderer.get("viewCountText", {})
            if view_text.get("runs"):
                viewer_str = "".join(r.get("text", "") for r in view_text["runs"])
                if "watching" in viewer_str.lower():
                    status = "live"  # confirm live
                    nums = re.findall(r'[\d,]+', viewer_str)
                    if nums:
                        viewer_count = int(nums[0].replace(",", ""))
            elif view_text.get("simpleText", ""):
                vt = view_text["simpleText"]
                if "waiting" in vt.lower():
                    status = "upcoming"
                    nums = re.findall(r'[\d,]+', vt)
                    if nums:
                        viewer_count = int(nums[0].replace(",", ""))

            # Upcoming scheduled time
            upcoming_info = renderer.get("upcomingEventData", {})
            if upcoming_info.get("startTime"):
                try:
                    ts = int(upcoming_info["startTime"])
                    scheduled_time = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
                    status = "upcoming"
                except (ValueError, OSError):
                    pass

            # Published time text (relative)
            published = renderer.get("publishedTimeText", {}).get("simpleText", "")

            # Thumbnail
            thumbs = renderer.get("thumbnail", {}).get("thumbnails", [])
            thumbnail = thumbs[-1].get("url", "") if thumbs else ""

            # Length (live = no length or "0")
            length_text = ""
            for overlay in renderer.get("thumbnailOverlays", []):
                ltr = overlay.get("thumbnailOverlayTimeStatusRenderer", {})
                length_text = ltr.get("text", {}).get("simpleText", "")

            stream_entry = {
                "video_id": video_id,
                "title": title,
                "status": status,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "embed_url": f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&rel=0",
                "thumbnail": thumbnail,
            }

            if viewer_count is not None:
                stream_entry["viewers"] = viewer_count
            if scheduled_time:
                stream_entry["scheduled"] = scheduled_time
            if published:
                stream_entry["published"] = published
            if length_text and length_text != "LIVE":
                stream_entry["duration"] = length_text

            streams.append(stream_entry)

    except Exception as e:
        logger.error(f"Error parsing streams data: {e}", exc_info=True)

    return streams


# === Fetch and cache ===

async def _fetch_streams_page(url: str) -> Optional[str]:
    """Fetch a YouTube channel streams page HTML."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml",
    }
    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            return resp.text
    except httpx.HTTPError as e:
        logger.error(f"Failed to fetch streams page {url}: {e}")
        return None


async def _fetch_channel_streams(channel: dict) -> List[Dict[str, Any]]:
    """Fetch and parse streams for a single YouTube channel."""
    html = await _fetch_streams_page(channel["url"])
    if not html:
        return []

    initial_data = _extract_initial_data(html)
    if not initial_data:
        return []

    streams = _parse_streams(initial_data)

    # Tag each stream with its source channel
    for s in streams:
        s["channel"] = channel["label"]
        s["channel_key"] = channel["key"]

    return streams


async def fetch_nasa_streams(force: bool = False) -> Dict[str, Any]:
    """
    Main entry point. Scrapes all configured YouTube channels concurrently.
    Uses cache unless force=True or cache is stale.
    """
    if not force and _is_cache_valid():
        return _cache["streams"]

    logger.info(f"Fetching streams from {len(CHANNELS)} YouTube channels...")

    # Scrape all channels concurrently
    tasks = [_fetch_channel_streams(ch) for ch in CHANNELS]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Merge all streams, skip errors
    all_streams = []
    seen_ids = set()
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"Channel {CHANNELS[i]['label']} failed: {result}")
            continue
        for stream in result:
            if stream["video_id"] not in seen_ids:
                seen_ids.add(stream["video_id"])
                all_streams.append(stream)

    if not all_streams and _cache["streams"]:
        logger.warning("All channels failed, using stale cache")
        return _cache["streams"]

    if not all_streams:
        return _build_response([], error="Failed to fetch streams from all channels")

    # Separate by status
    live = [s for s in all_streams if s["status"] == "live"]
    upcoming = sorted(
        [s for s in all_streams if s["status"] == "upcoming"],
        key=lambda s: s.get("scheduled", "9999")
    )
    recent = [s for s in all_streams if s["status"] == "vod"][:10]

    result = _build_response(all_streams, live=live, upcoming=upcoming, recent=recent)

    # Update cache
    _cache["streams"] = result
    _cache["fetched_at"] = datetime.now(timezone.utc)

    ch_names = ", ".join(ch["label"] for ch in CHANNELS)
    logger.info(f"Streams [{ch_names}]: {len(live)} live, {len(upcoming)} upcoming, {len(recent)} recent")
    return result


def _build_response(
    all_streams: List,
    live: List = None,
    upcoming: List = None,
    recent: List = None,
    error: str = None,
) -> Dict[str, Any]:
    """Build the API response structure."""
    result = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "sources": [ch["url"] for ch in CHANNELS],
        "live": live or [],
        "upcoming": upcoming or [],
        "recent": recent or [],
        "total": len(all_streams),
    }
    # Pick the best default stream: first live, else first upcoming
    if live:
        result["recommended"] = live[0]
    elif upcoming:
        result["recommended"] = upcoming[0]
    elif all_streams:
        result["recommended"] = all_streams[0]
    else:
        result["recommended"] = None

    if error:
        result["error"] = error

    return result


# === Fallback sources (always available) ===

FALLBACK_SOURCES = [
    {
        "video_id": None,
        "title": "NASA TV — Public",
        "status": "always-on",
        "type": "ustream",
        "embed_url": "https://video.ibm.com/embed/nasahdtv?autoplay&mute",
        "url": "https://video.ibm.com/nasahdtv",
    },
    {
        "video_id": None,
        "title": "NASA TV — Media",
        "status": "always-on",
        "type": "ustream",
        "embed_url": "https://video.ibm.com/embed/nasatv?autoplay&mute",
        "url": "https://video.ibm.com/nasatv",
    },
    {
        "video_id": None,
        "title": "ISS — Live Views",
        "status": "always-on",
        "type": "ustream",
        "embed_url": "https://video.ibm.com/embed/live-iss-stream?autoplay&mute",
        "url": "https://video.ibm.com/channel/live-iss-stream",
    },
    {
        "video_id": None,
        "title": "ISS — HD Earth",
        "status": "always-on",
        "type": "ustream",
        "embed_url": "https://video.ibm.com/embed/iss-hdev-payload?autoplay&mute",
        "url": "https://video.ibm.com/channel/iss-hdev-payload",
    },
]


async def get_all_sources(force: bool = False) -> Dict[str, Any]:
    """
    Combined endpoint: YouTube live/upcoming + always-on fallbacks.
    Frontend uses this to build the full source dropdown.
    """
    yt_data = await fetch_nasa_streams(force=force)
    return {
        **yt_data,
        "fallback": FALLBACK_SOURCES,
    }
