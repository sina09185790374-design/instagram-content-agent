import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent.caption_builder import build_caption
from agent.trend_radar import score_topic, rank_topics
from agent.scheduler import publish_cycle, CYCLES, PUBLISH_ORDER

TOPIC = {"title":"آپدیت جدید با 120 فریم و 150 بازیکن","category":"gaming","facts":["حجم 28 گیگابایت","120 فریم"],"hashtags":["#gaming","#ps5","#warzone"]}

class TestCaption(unittest.TestCase):
    def test_caption_has_cta_and_reason(self):
        c = build_caption(TOPIC)
        self.assertIn("فالو کن چون", c)
        self.assertIn("🎮", c)
    def test_hashtags_3_to_5(self):
        c = build_caption(TOPIC)
        tags = [w for w in c.split() if w.startswith("#")]
        self.assertGreaterEqual(len(tags), 3)
        self.assertLessEqual(len(tags), 5)
    def test_numbers_score_higher(self):
        low = {"title":"خبر ساده","category":"gaming","facts":["ساده"]}
        self.assertGreater(score_topic(TOPIC), score_topic(low))
        self.assertEqual(rank_topics([low, TOPIC])[0]["topic"], TOPIC)
    def test_scheduler_order_and_429_stop(self):
        self.assertEqual(CYCLES, [(12,51),(15,30),(18,0),(20,30)])
        self.assertEqual(PUBLISH_ORDER, ["reel","post","stories"])
        calls=[]
        def fn(kind,payload):
            calls.append(kind)
            return 429 if kind=="post" else 200
        res = publish_cycle({"reel":1,"post":2,"stories":3}, fn)
        self.assertEqual(calls, ["reel","post"])  # stories never attempted after 429
        self.assertEqual(res[-1]["reason"], "rate_limited")

if __name__ == "__main__":
    unittest.main()
