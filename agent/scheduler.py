"""Scheduler: 4 daily cycles Tehran, order reel->post->stories, stop on 429."""
from datetime import datetime, timedelta

try:
    from zoneinfo import ZoneInfo
    TEHRAN = ZoneInfo("Asia/Tehran")
except Exception:
    TEHRAN = None

CYCLES = [(12,51),(15,30),(18,0),(20,30)]
PUBLISH_ORDER = ["reel","post","stories"]

def cycle_times():
    return [f"{h:02d}:{m:02d}" for h,m in CYCLES]

def next_cycle(now=None):
    now = now or (datetime.now(TEHRAN) if TEHRAN else datetime.now())
    candidates = []
    for h,m in CYCLES:
        t = now.replace(hour=h, minute=m, second=0, microsecond=0)
        if t <= now:
            t = t + timedelta(days=1)
        candidates.append(t)
    return min(candidates)

def publish_cycle(items, publish_fn):
    """items: dict type->payload. publish_fn(type,payload)->status int.
    Iterates PUBLISH_ORDER, stops immediately on 429. Returns list of results."""
    results = []
    for kind in PUBLISH_ORDER:
        if kind not in items:
            continue
        status = publish_fn(kind, items[kind])
        results.append({"type": kind, "status": status})
        if status == 429:
            results.append({"type": "stopped", "status": 429, "reason": "rate_limited"})
            break
    return results
