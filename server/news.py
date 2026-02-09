"""
ArtemisOps News Aggregation Service
Aggregates NASA and space news from multiple RSS feeds.

Separate from ISS-specific news in iss.py — this provides broader
coverage of Artemis program, NASA announcements, and commercial crew.

Feeds:
- NASA Breaking News
- NASA Artemis Blog
- NASA ISS Blog
- Spaceflight Now (general)
- SpaceNews
"""
import asyncio
import xml.etree.ElementTree as ET
import httpx
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

# === Feed Configuration ===

FEEDS = [
    {
        "id": "nasa-breaking",
        "name": "NASA Breaking News",
        "url": "https://www.nasa.gov/news-release/feed/",
        "source_label": "NASA",
        "priority": 1,
    },
    {
        "id": "nasa-artemis",
        "name": "NASA Artemis Blog",
        "url": "https://blogs.nasa.gov/artemis/feed/",
        "source_label": "NASA Artemis",
        "priority": 1,
    },
    {
        "id": "nasa-commercial-crew",
        "name": "NASA Commercial Crew Blog",
        "url": "https://blogs.nasa.gov/commercialcrew/feed/",
        "source_label": "NASA Crew",
        "priority": 1,
    },
    {
        "id": "nasa-iss",
        "name": "NASA ISS Blog",
        "url": "https://blogs.nasa.gov/spacestation/feed/",
        "source_label": "NASA ISS Blog",
        "priority": 2,
    },
    {
        "id": "spaceflight-now",
        "name": "Spaceflight Now",
        "url": "https://spaceflightnow.com/feed/",
        "source_label": "Spaceflight Now",
        "priority": 2,
    },
    {
        "id": "spaceflight-now-iss",
        "name": "Spaceflight Now ISS",
        "url": "https://spaceflightnow.com/category/iss/feed/",
        "source_label": "Spaceflight Now",
        "priority": 2,
    },
]

# === Cache ===

NEWS_CACHE_TTL = 900  # 15 minutes

_news_cache: Dict[str, Any] = {
    "data": None,
    "timestamp": None,
}


def _is_cache_valid() -> bool:
    if not _news_cache["data"] or not _news_cache["timestamp"]:
        return False
    age = (datetime.now(timezone.utc) - _news_cache["timestamp"]).total_seconds()
    return age < NEWS_CACHE_TTL


def _cache_age() -> Optional[float]:
    if not _news_cache["timestamp"]:
        return None
    return (datetime.now(timezone.utc) - _news_cache["timestamp"]).total_seconds()


# === RSS Parsing ===

def _parse_rss_date(date_str: str) -> Optional[datetime]:
    """Parse common RSS date formats."""
    if not date_str:
        return None
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%a, %d %b %Y %H:%M:%S GMT",
        "%a, %d %b %Y %H:%M:%S +0000",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None


def _format_time_ago(dt: datetime) -> str:
    """Format datetime as relative time string."""
    if not dt:
        return ""
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    diff = now - dt
    hours = diff.total_seconds() / 3600
    days = diff.days
    if hours < 1:
        return f"{int(diff.total_seconds() / 60)} min ago"
    elif hours < 24:
        return f"{int(hours)}h ago"
    elif days == 1:
        return "Yesterday"
    elif days < 7:
        return f"{days} days ago"
    elif days < 30:
        return f"{days // 7} weeks ago"
    else:
        return dt.strftime("%b %d")


def _clean_html(text: str) -> str:
    """Strip HTML tags from RSS description text."""
    if not text:
        return ""
    import re
    clean = re.sub(r'<[^>]+>', '', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean


async def _fetch_feed(client: httpx.AsyncClient, feed: dict) -> List[dict]:
    """Fetch and parse a single RSS feed."""
    items = []
    try:
        response = await client.get(feed["url"])
        response.raise_for_status()

        root = ET.fromstring(response.text)

        # Handle both RSS 2.0 and Atom feeds
        channel = root.find("channel")
        if channel is not None:
            # RSS 2.0
            for item_el in channel.findall("item"):
                title = item_el.find("title")
                pub_date = item_el.find("pubDate")
                link = item_el.find("link")
                description = item_el.find("description")

                pub_dt = _parse_rss_date(
                    pub_date.text if pub_date is not None else None
                )
                desc_text = _clean_html(
                    description.text if description is not None else None
                )

                items.append({
                    "title": title.text.strip() if title is not None and title.text else "Untitled",
                    "time": pub_dt.isoformat() if pub_dt else None,
                    "time_ago": _format_time_ago(pub_dt),
                    "link": link.text.strip() if link is not None and link.text else None,
                    "source": feed["source_label"],
                    "feed_id": feed["id"],
                    "summary": desc_text[:200] + "..." if len(desc_text) > 200 else desc_text if desc_text else None,
                    "priority": feed["priority"],
                })

        logger.info(f"Fetched {len(items)} items from {feed['name']}")

    except Exception as e:
        logger.warning(f"Failed to fetch {feed['name']}: {e}")

    return items


# === Public API ===

async def get_news(
    limit: int = 20,
    source: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetch aggregated space news from all configured RSS feeds.

    Args:
        limit: Max number of items to return (default 20).
        source: Optional filter — only return items from this source
                (e.g. "nasa-artemis", "spaceflight-now").

    Returns cached data if within TTL (15 min).
    """
    # Check cache
    if _is_cache_valid() and source is None:
        data = _news_cache["data"]
        filtered = data["news"][:limit]
        return {
            "news": filtered,
            "count": len(filtered),
            "total_available": data["total_available"],
            "sources": data["sources"],
            "timestamp": data["timestamp"],
            "cached": True,
            "cache_age_seconds": round(_cache_age(), 1),
        }

    now = datetime.now(timezone.utc)

    # Fetch all feeds in parallel
    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        tasks = [_fetch_feed(client, feed) for feed in FEEDS]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    # Flatten results
    all_items: List[dict] = []
    sources_found = set()
    for result in results:
        if isinstance(result, list):
            all_items.extend(result)
            for item in result:
                sources_found.add(item["source"])

    # Deduplicate by title similarity (exact match)
    seen_titles = set()
    unique_items = []
    for item in all_items:
        title_key = item["title"].lower().strip()
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            unique_items.append(item)

    # Sort: newest first, with priority as tiebreaker
    unique_items.sort(
        key=lambda x: (x.get("time") or "0000", -x.get("priority", 99)),
        reverse=True,
    )

    # Cache full result set
    cache_data = {
        "news": unique_items,
        "total_available": len(unique_items),
        "sources": sorted(sources_found),
        "timestamp": now.isoformat(),
    }
    _news_cache["data"] = cache_data
    _news_cache["timestamp"] = now

    # Apply filters
    filtered = unique_items
    if source:
        filtered = [i for i in filtered if i["feed_id"] == source]

    filtered = filtered[:limit]

    return {
        "news": filtered,
        "count": len(filtered),
        "total_available": len(unique_items),
        "sources": sorted(sources_found),
        "timestamp": now.isoformat(),
        "cached": False,
    }
