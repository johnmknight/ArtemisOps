# ArtemisOps Data Flow & API Optimization Guide

## Overview

This document maps when data is loaded, cached, and refreshed throughout the ArtemisOps application.

---

## Server-Side Data Flow

### On Server Startup

| Order | Action | Source | Cached |
|-------|--------|--------|--------|
| 1 | Initialize SQLite database | Local | N/A |
| 2 | Ensure default missions exist | Local DB | N/A |
| 3 | **Sync all missions** | Space Devs API | → SQLite |
| 4 | Fetch mission patches/logos | Wikipedia/Space Devs | → SQLite |
| 5 | Fetch crew data | Space Devs API | → SQLite |
| 6 | Start scheduler | N/A | N/A |

### Scheduled Syncs

| Job | Interval | External API | Notes |
|-----|----------|--------------|-------|
| Mission data sync | **12 hours** | Space Devs API | Crew, milestones, patches |
| Weather cache clear | On sync | N/A | Forces fresh fetch on next request |

---

## Server-Side Caching (In-Memory)

| Data Type | Cache TTL | External API | Notes |
|-----------|-----------|--------------|-------|
| ISS Position | **3 sec** | Where The ISS At | Very short - position changes constantly |
| ISS Crew | **1 hour** | Open Notify | Crew changes rarely |
| Location Name | **30 sec** | Where The ISS At geocoder | Rounded to 0.1° for cache key |
| ISS News | **15 min** | Spaceflight Now RSS | RSS feeds update slowly |
| Weather | **30 min** | Open-Meteo | Only fetched if launch is today |

---

## Client-Side Polling

### Main App (index.html)

| Event | Action | API Endpoint |
|-------|--------|--------------|
| Page load | Load missions list | `GET /api/missions` |
| Page load | Load current mission | `GET /api/missions/{id}` |
| Page load | Load weather (if applicable) | `GET /api/missions/{id}/weather` |
| WebSocket | Real-time mission updates | `WS /ws` |
| Mission switch | Reload mission + weather | 2 API calls |

### ISS Tracker (iss-tracker.html)

| Interval | Action | API Endpoint |
|----------|--------|--------------|
| **5 sec** | Update ISS position | `GET /api/iss/position` |
| **5 sec** | Update location name | `GET /api/iss/location/{coords}` |
| **1 min** | Update day/night terminator | Client-side calculation |
| **15 min** | Refresh ISS news | `GET /api/iss/news` |
| **1 sec** | Update clock | Client-side |
| Real-time | NASA telemetry | **Direct to NASA Lightstreamer** (not via server) |

### Other Tabs

| Tab | Interval | Action |
|-----|----------|--------|
| Mission | 1 sec | Update countdown timer (client-side) |
| Crew | 1 sec | Update EVA timer (client-side) |

---

## External API Calls Summary

### From Server (Proxied)

| API | Endpoint | When Called | Rate |
|-----|----------|-------------|------|
| Space Devs | `ll.thespacedevs.com` | Server startup + every 12h | ~2-4 calls/sync |
| Where The ISS At | `api.wheretheiss.at` | Every 5 sec (if not cached) | ~12/min max |
| Open Notify | `api.open-notify.org` | ISS crew requests | ~1/hour |
| Open-Meteo | `api.open-meteo.com` | Weather requests (launch day only) | Rare |
| NASA RSS feeds | `blogs.nasa.gov` | Every 15 min | ~4/hour |

### From Client (Direct)

| API | Endpoint | When Called | Rate |
|-----|----------|-------------|------|
| NASA Lightstreamer | `push.lightstreamer.com` | Continuous WebSocket | Real-time stream |
| NASA GIBS | `gibs.earthdata.nasa.gov` | Map tile requests | On map pan/zoom |

---

## 🔧 Optimization Opportunities

### HIGH IMPACT

#### 1. **Combine ISS Position + Location into Single Endpoint**
**Current:** 2 API calls every 5 seconds
```
GET /api/iss/position  → returns lat/lng
GET /api/iss/location/{lat},{lng}  → returns location name
```
**Proposed:** 1 API call every 5 seconds
```
GET /api/iss/position?include_location=true
```
**Savings:** 50% reduction in ISS tracking API calls (720 → 360 calls/hour)

#### 2. **Increase ISS Position Cache TTL**
**Current:** 3 second cache, 5 second poll = often cache miss
**Proposed:** 5 second cache = always cache hit on second request
**Risk:** Minimal - ISS moves ~40km in 5 seconds, acceptable for display

#### 3. **Reduce Location Lookup Frequency**
**Current:** Every 5 seconds
**Proposed:** Every 15-30 seconds (location name doesn't change that fast)
**Savings:** 66-83% reduction in geocoder API calls

### MEDIUM IMPACT

#### 4. **Batch Initial Data Load**
**Current:** 3 separate calls on page load
```
GET /api/missions
GET /api/missions/{id}
GET /api/missions/{id}/weather
```
**Proposed:** Single combined endpoint
```
GET /api/init?mission={id}
```
Returns: missions list + current mission + weather in one response

#### 5. **Server-Side NASA Telemetry**
**Current:** Client connects directly to NASA Lightstreamer
**Proposed:** Server maintains single Lightstreamer connection, broadcasts to clients via WebSocket
**Benefit:** Reduces NASA API load, centralizes telemetry handling
**Complexity:** HIGH - requires Lightstreamer Python client

### LOW IMPACT (Nice to Have)

#### 6. **News Feed Deduplication**
Currently fetches from multiple RSS feeds with potential duplicates
Could merge and dedupe on server side

#### 7. **WebSocket for ISS Position**
Replace polling with server push
**Benefit:** Lower latency, fewer HTTP connections
**Complexity:** Moderate - need to add ISS position to WebSocket broadcast

---

## Recommended Implementation Order

| Priority | Change | Effort | Impact |
|----------|--------|--------|--------|
| 1 | Combine position + location endpoint | 1 hour | High |
| 2 | Increase position cache to 5 sec | 5 min | Medium |
| 3 | Reduce location poll to 15 sec | 10 min | Medium |
| 4 | Batch initial data load | 2 hours | Medium |
| 5 | WebSocket for ISS position | 4 hours | Medium |
| 6 | Server-side Lightstreamer | 8+ hours | Low (complex) |

---

## Current Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              EXTERNAL APIs                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  Space Devs    Where The ISS At    Open Notify    Open-Meteo    NASA RSS    │
│  (12h sync)    (3s cache)          (1h cache)     (30m cache)   (15m cache) │
└──────┬─────────────┬───────────────────┬──────────────┬─────────────┬───────┘
       │             │                   │              │             │
       ▼             ▼                   ▼              ▼             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ArtemisOps SERVER (FastAPI)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐│
│  │   SQLite    │  │  In-Memory  │  │   WebSocket  │  │    Static Files     ││
│  │  Database   │  │    Cache    │  │   Broadcast  │  │  (HTML/JS/Assets)   ││
│  └─────────────┘  └─────────────┘  └──────────────┘  └─────────────────────┘│
└──────┬─────────────────┬───────────────────┬────────────────────────────────┘
       │                 │                   │
       │    HTTP/REST    │                   │ WebSocket
       ▼                 ▼                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            CLIENT (Browser)                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  index.html          │  iss-tracker.html        │  Other Tabs               │
│  - Mission data      │  - Position (5s poll)    │  - Countdown (1s client)  │
│  - Weather           │  - Location (5s poll)    │  - EVA timer (1s client)  │
│  - WebSocket conn    │  - News (15m poll)       │                           │
│                      │  - NASA Lightstreamer ◄──┼── Direct to NASA          │
│                      │  - GIBS map tiles ◄──────┼── Direct to NASA          │
└──────────────────────┴──────────────────────────┴───────────────────────────┘
```

---

*Last Updated: February 1, 2026*
