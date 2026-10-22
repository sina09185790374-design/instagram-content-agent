"""Caption builder: Persian news-first caption."""
CATEGORY_EMOJI = {"gaming":"🎮","ai":"🤖","hardware":"🖥️","xbox":"🟢","playstation":"🔵","tech":"📱","wow":"⚔️"}
DEFAULT_HASHTAGS = ["#gaming","#tech","#ai","#sarzamin_game"]
FOLLOW_REASONS = {
 "gaming":"هر روز جنجالی‌ترین خبرهای بازی اینجاست",
 "ai":"هر روز مهم‌ترین خبرهای هوش مصنوعی و ایجنت‌ها اینجاست",
 "hardware":"هر روز خفن‌ترین اسمبل‌ها و اخبار سخت‌افزار اینجاست",
}
DEFAULT_REASON = "هر روز خبرهای داغ بازی، تکنولوژی و هوش مصنوعی اینجاست"

def _hashtags(topic):
    tags = list(topic.get("hashtags",[]) or [])
    for t in DEFAULT_HASHTAGS:
        if len(tags) >= 5:
            break
        if t not in tags:
            tags.append(t)
    return tags[:5] if len(tags)>=3 else (tags+DEFAULT_HASHTAGS)[:3]

def build_caption(topic):
    emoji = CATEGORY_EMOJI.get((topic.get("category") or "").lower(), "🔥")
    title = topic.get("title","").strip()
    facts = topic.get("facts",[]) or []
    reason = FOLLOW_REASONS.get((topic.get("category") or "").lower(), DEFAULT_REASON)
    lines = [f"{emoji} {title}", ""]
    for f in facts:
        lines.append(f"🔹 {f}")
    lines.append("")
    lines.append(f"👉 فالو کن چون {reason} — از دستش نده!")
    lines.append("💬 نظرت رو کامنت کن و بفرست برای رفیقت")
    lines.append("")
    lines.append(" ".join(_hashtags(topic)))
    return "\n".join(lines)
