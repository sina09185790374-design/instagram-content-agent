#!/usr/bin/env python3
"""CLI. --demo runs with sample data, no network/tokens."""
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from agent.trend_radar import rank_topics
from agent.caption_builder import build_caption
from agent.scheduler import cycle_times, publish_cycle, PUBLISH_ORDER

SAMPLE = [
 {"title":"آپدیت جدید وارزون با 120 فریم منتشر شد","category":"gaming","facts":["نقشه جدید با 150 بازیکن","حجم آپدیت 28 گیگابایت"],"hashtags":["#gaming","#warzone","#ps5"],"hook_words":["جدید"]},
 {"title":"خبر معمولی بدون عدد","category":"gaming","facts":["یک خبر ساده"],"hashtags":["#gaming"]},
]

def main():
    ap = argparse.ArgumentParser(description="Instagram Content Agent (demo, no network)")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--topics", default=None, help="path to topics.json")
    args = ap.parse_args()
    topics = SAMPLE
    if args.topics:
        from agent.trend_radar import load_topics
        topics = load_topics(args.topics)
    ranked = rank_topics(topics)
    print(f"Cycles (Tehran): {', '.join(cycle_times())} | Order: {' -> '.join(PUBLISH_ORDER)}")
    for i, item in enumerate(ranked, 1):
        print(f"\n#{i} score={item['score']} title={item['topic'].get('title')}")
    if ranked:
        print("\n--- Caption for top topic ---")
        print(build_caption(ranked[0]["topic"]))
        print("\n--- Simulated publish (stops on 429 demo) ---")
        def fake(kind, payload):
            print(f"publish {kind}: OK (200)")
            return 200
        print(publish_cycle({"reel":"r1","post":"p1","stories":"s1"}, fake))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
