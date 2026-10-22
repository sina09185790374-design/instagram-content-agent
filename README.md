# Instagram Content Agent 🎮

A practical Python agent that turns trending topics into publish-ready Persian Instagram content: **trend scoring → news-first caption → scheduled publishing plan**.

Built from a real production workflow running a gaming page daily (4 cycles/day). Demo mode needs **no network, no tokens**.

## Features
- **Trend Radar** — scores topics by numbers in facts, hook words, and comment/CTA potential (questions & versus)
- **Caption Builder** — Persian news-first format: emoji lead, bullet facts, follow CTA *with a reason*, 3–5 hashtags
- **Scheduler** — 4 Tehran cycles `12:51 / 15:30 / 18:00 / 20:30`, publish order `reel → post → stories`, **stops immediately on HTTP 429**

## Quick Start
```bash
python3 main.py --demo
python3 main.py --topics topics.example.json
python3 -m unittest discover -s tests -v
```
Stdlib only. Copy `.env.example` to `.env` for your own deployment — never commit real tokens.

## Structure
```
agent/trend_radar.py     scoring & ranking
agent/caption_builder.py Persian caption format
agent/scheduler.py       cycles, order, 429 stop
main.py                  CLI demo
```

## License
MIT

---
## فارسی
ایجنت تولید محتوای اینستاگرام: موضوعات ترند رو امتیاز می‌ده، کپشن خبری فارسی با CTA فالو + دلیل می‌سازه و برنامه انتشار ۴ چرخه روزانه تهران رو مدیریت می‌کنه. روی ۴۲۹ بلافاصله متوقف می‌شه. حالت دمو بدون اینترنت و توکن کار می‌کنه: `python3 main.py --demo`
