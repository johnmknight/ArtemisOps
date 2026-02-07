"""
ISS Crew Enrichment Service

Two-phase crew data approach:
  Phase 1: Open Notify API → crew names and craft (fast, always available)
  Phase 2: NASA Station Blog → agency affiliations (scraped, cached 24h)

NASA's ISS blog consistently tags agency before every crew mention:
  "NASA astronaut Chris Williams"
  "Roscosmos cosmonaut Sergey Kud-Sverchkov"  
  "JAXA (Japan Aerospace Exploration Agency) astronaut Kimiya Yui"
  "ESA (European Space Agency) astronaut Sophie Adenot"
  "CSA (Canadian Space Agency) astronaut Jeremy Hansen"

This module parses those patterns to build a name→agency lookup dict.
Falls back gracefully if scraping fails — crew just won't have agency tags.
"""
import re
import httpx
import logging
from datetime import datetime, timezone
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# NASA ISS Blog — richest structured source for crew/agency data
# Try multiple RSS URL patterns (NASA has restructured URLs over time)
NASA_BLOG_RSS_URLS = [
    "https://www.nasa.gov/blogs/spacestation/feed/",
    "https://blogs.nasa.gov/spacestation/feed/",
    "https://www.nasa.gov/feed/blog-iss/",
]
# Fallback: scrape the blog listing page directly
NASA_BLOG_PAGE_URL = "https://www.nasa.gov/blogs/spacestation/"

# Cache: name → agency lookup
_agency_cache: Dict[str, any] = {
    "data": {},        # { "Chris Williams": "NASA", "Sergey Kud-Sverchkov": "Roscosmos", ... }
    "timestamp": None,
    "source": None,
}
CACHE_TTL = 86400  # 24 hours — crew rotations happen every ~6 months

# ============================================================================
# AGENCY EXTRACTION PATTERNS
# NASA blogs use consistent patterns we can match reliably
# ============================================================================

# Pattern: "AGENCY astronaut/cosmonaut NAME"
# Captures agency keyword + following proper name (2-4 capitalized words)
AGENCY_PATTERNS = [
    # "NASA astronaut Chris Williams" / "NASA Flight Engineer Chris Williams"
    # Note: No re.IGNORECASE — we rely on [A-Z] to detect proper name boundaries
    (r'NASA\s+(?:[Aa]stronauts?|[Ff]light\s+[Ee]ngineers?|[Cc]ommander)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+))', 'NASA'),
    # "Roscosmos cosmonaut Sergey Kud-Sverchkov" / "Roscosmos Flight Engineer Sergei Mikaev"
    (r'Roscosmos\s+(?:[Cc]osmonauts?|[Ff]light\s+[Ee]ngineers?|[Cc]ommander)\s+([A-Z][a-z]+\s+[A-Z][a-z]+(?:-[A-Z][a-z]+)?)', 'Roscosmos'),
    # "JAXA (Japan Aerospace Exploration Agency) astronaut Kimiya Yui"
    (r'JAXA\s*(?:\([^)]+\))?\s*(?:[Aa]stronauts?|[Ff]light\s+[Ee]ngineers?)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+))', 'JAXA'),
    # "ESA (European Space Agency) astronaut Sophie Adenot"
    (r'ESA\s*(?:\([^)]+\))?\s*(?:[Aa]stronauts?|[Ff]light\s+[Ee]ngineers?)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+))', 'ESA'),
    # "CSA (Canadian Space Agency) astronaut Jeremy Hansen"
    (r'CSA\s*(?:\([^)]+\))?\s*(?:[Aa]stronauts?|[Ff]light\s+[Ee]ngineers?)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+))', 'CSA'),
    # Also match "of Roscosmos" / "of JAXA" patterns: "Oleg Platonov of Roscosmos"
    (r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:-[A-Z][a-z]+)?)\s+of\s+Roscosmos', 'Roscosmos'),
    (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+))\s+of\s+JAXA', 'JAXA'),
    (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+))\s+of\s+ESA', 'ESA'),
    (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+))\s+of\s+CSA', 'CSA'),
]

# Cleanup: trim trailing common words that get captured accidentally
TRAILING_NOISE = {'and', 'has', 'was', 'will', 'who', 'the', 'both', 'set', 'led',
                  'back', 'is', 'are', 'on', 'in', 'for', 'to', 'at', 'from'}


def _clean_name(name: str) -> str:
    """Clean extracted name — remove trailing noise words and extra spaces."""
    parts = name.strip().split()
    while parts and parts[-1].lower() in TRAILING_NOISE:
        parts.pop()
    return ' '.join(parts)


# Pattern for "and FirstName LastName" continuation after a matched name
# e.g. "Roscosmos Flight Engineers Sergey Kud-Sverchkov and Sergei Mikaev"
#   → first match gets Kud-Sverchkov, continuation gets Mikaev with same agency
AND_CONTINUATION = re.compile(
    r'and\s+([A-Z][a-z]+\s+[A-Z][a-z]+(?:-[A-Z][a-z]+)?)'
)


def _extract_agencies_from_text(text: str) -> Dict[str, str]:
    """
    Extract name→agency mappings from a block of text (blog post, RSS item, etc.)
    Returns dict like {"Chris Williams": "NASA", "Sergey Kud-Sverchkov": "Roscosmos"}
    """
    results = {}
    for pattern, agency in AGENCY_PATTERNS:
        for match in re.finditer(pattern, text):
            name = _clean_name(match.group(1))
            if len(name.split()) >= 2:
                results[name] = agency
            
            # Check for "and [Name]" continuation after match
            after_match = text[match.end():match.end()+80]
            cont = AND_CONTINUATION.match(after_match.lstrip(', '))
            if cont:
                cont_name = _clean_name(cont.group(1))
                if len(cont_name.split()) >= 2:
                    results[cont_name] = agency
    return results


def _parse_rss_feed(xml_text: str) -> str:
    """Extract all text content from RSS feed items for agency parsing."""
    # Simple extraction — pull text from <title>, <description>, <content:encoded>
    # We don't need a full XML parser for this
    all_text = []
    
    # Get content from <description> tags (usually has the richest text)
    for match in re.finditer(r'<description><!\[CDATA\[(.*?)\]\]></description>', xml_text, re.DOTALL):
        all_text.append(match.group(1))
    
    # Also try <content:encoded> tags
    for match in re.finditer(r'<content:encoded><!\[CDATA\[(.*?)\]\]></content:encoded>', xml_text, re.DOTALL):
        all_text.append(match.group(1))
    
    # Fallback: just get everything between item tags
    for match in re.finditer(r'<item>(.*?)</item>', xml_text, re.DOTALL):
        all_text.append(match.group(1))
    
    # Strip HTML tags from extracted content
    combined = ' '.join(all_text)
    clean = re.sub(r'<[^>]+>', ' ', combined)
    clean = re.sub(r'&[a-z]+;', ' ', clean)
    clean = re.sub(r'\s+', ' ', clean)
    return clean


async def fetch_crew_agencies() -> Dict[str, str]:
    """
    Phase 2: Fetch NASA ISS blog and extract crew agency affiliations.
    Returns a name→agency dict. Cached for 24 hours.
    """
    # Check cache
    if (_agency_cache["timestamp"] and _agency_cache["data"] and
            (datetime.now(timezone.utc) - _agency_cache["timestamp"]).total_seconds() < CACHE_TTL):
        return _agency_cache["data"]
    
    agencies = {}
    
    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        # Try RSS feeds first (structured, reliable)
        for rss_url in NASA_BLOG_RSS_URLS:
            try:
                resp = await client.get(rss_url)
                if resp.status_code == 200 and '<item>' in resp.text:
                    text = _parse_rss_feed(resp.text)
                    agencies = _extract_agencies_from_text(text)
                    if agencies:  # Only cache if we found something
                        logger.info(f"Crew enrichment: {len(agencies)} mappings from {rss_url}")
                        _agency_cache.update({
                            "data": agencies,
                            "timestamp": datetime.now(timezone.utc),
                            "source": rss_url
                        })
                        return agencies
            except Exception as e:
                logger.debug(f"RSS feed {rss_url} failed: {e}")
                continue
        
        # Fallback: scrape the blog listing page directly
        try:
            resp = await client.get(NASA_BLOG_PAGE_URL)
            if resp.status_code == 200:
                clean_text = re.sub(r'<[^>]+>', ' ', resp.text)
                agencies = _extract_agencies_from_text(clean_text)
                if agencies:
                    logger.info(f"Crew enrichment: {len(agencies)} mappings from blog page")
                    _agency_cache.update({
                        "data": agencies,
                        "timestamp": datetime.now(timezone.utc),
                        "source": "nasa-blog-page"
                    })
                    return agencies
        except Exception as e:
            logger.warning(f"Blog page fetch failed: {e}")
    
    # Return stale cache if available
    if _agency_cache["data"]:
        logger.info("Crew enrichment: using stale cache")
        return _agency_cache["data"]
    
    return {}


def enrich_crew_with_agencies(crew_list: list, agency_lookup: Dict[str, str]) -> list:
    """
    Merge agency info into crew list from Open Notify.
    Uses fuzzy matching — handles "Sergei" vs "Sergey", "Kud-Sverchkov" partial matches.
    
    Args:
        crew_list: [{"name": "Chris Williams", "craft": "ISS"}, ...]
        agency_lookup: {"Chris Williams": "NASA", ...}
    
    Returns:
        Enriched list with agency field added where found.
    """
    enriched = []
    for member in crew_list:
        person = dict(member)  # copy
        name = person.get("name", "")
        
        # Exact match
        if name in agency_lookup:
            person["agency"] = agency_lookup[name]
        else:
            # Fuzzy: try matching by last name
            last_name = name.split()[-1] if name else ""
            matched_agency = None
            for lookup_name, agency in agency_lookup.items():
                # Last name match (handles first name spelling variations)
                if last_name and lookup_name.split()[-1] == last_name:
                    matched_agency = agency
                    break
                # Substring match (handles hyphenated names)
                if last_name and last_name in lookup_name:
                    matched_agency = agency
                    break
            if matched_agency:
                person["agency"] = matched_agency
        
        enriched.append(person)
    
    return enriched


def get_cache_status() -> dict:
    """Return current enrichment cache status for diagnostics."""
    return {
        "has_data": bool(_agency_cache["data"]),
        "crew_count": len(_agency_cache["data"]),
        "source": _agency_cache.get("source"),
        "age_seconds": (
            round((datetime.now(timezone.utc) - _agency_cache["timestamp"]).total_seconds(), 1)
            if _agency_cache["timestamp"] else None
        ),
        "mappings": _agency_cache["data"] if _agency_cache["data"] else {}
    }
