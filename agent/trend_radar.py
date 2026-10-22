"""Trend radar: scores topics by hook / numbers / CTA potential."""
import json, re
from pathlib import Path

HOOK_WORDS = ["فوری","جدید","جنجالی","شوک","اولین","رکورد","breaking","new","first","exclusive","vs","مقایسه"]
CTA_WORDS = ["؟","?","کدوم","کدام","بهتره","یا","vs","نظر"]

def load_topics(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return data.get("topics", [])
    return data

def _count_numbers(text):
    return len(re.findall(r"\d+", text or ""))

def score_topic(topic):
    """Higher is better. Numbers + hook words + question/versus (CTA potential) + facts."""
    title = topic.get("title","")
    facts = topic.get("facts",[]) or []
    text = title + " " + " ".join(map(str,facts))
    score = 0.0
    score += _count_numbers(text) * 10          # numbers-heavy facts perform best
    score += len(facts) * 5                      # more concrete facts
    low = text.lower()
    for w_ in HOOK_WORDS:
        if w_.lower() in low:
            score += 8
    for w_ in CTA_WORDS:
        if w_ in text:
            score += 6                               # question / versus invites comments & follows
    for w_ in topic.get("hook_words",[]) or []:
        if w_:
            score += 4
    if 20 <= len(title) <= 90:
        score += 5
    return round(score, 2)

def rank_topics(topics):
    ranked = sorted(topics, key=score_topic, reverse=True)
    return [{"score": score_topic(t), "topic": t} for t in ranked]
