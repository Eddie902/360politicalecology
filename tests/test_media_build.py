"""Build-time media discovery tests. All synthetic media lives in temp directories."""
import tempfile
import unittest
from pathlib import Path
import yaml

from scripts.build_media import generate, load_public, GENERATED


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for path in ["_data/media", "articles/sample", "topics/sample-topic"]:
            (self.root / path).mkdir(parents=True)
        (self.root / "_data/topics.yml").write_text(yaml.safe_dump({"topics": [{"id": "MIN", "label": "Critical Minerals", "slug": "sample-topic"}]}), encoding="utf-8")
        (self.root / "_data/media-types.yml").write_text(yaml.safe_dump({
            "media_types": [{"id": x} for x in ["short_video", "long_video", "interview", "audio", "carousel", "infographic"]],
            "platforms": ["youtube", "linkedin", "instagram", "facebook", "tiktok"],
            "statuses": ["planned", "draft", "in_review", "approved", "published", "corrected", "withdrawn", "archived"],
        }), encoding="utf-8")
        (self.root / "_data/social-platforms.yml").write_text(yaml.safe_dump({
            "accounts": [{"platform": p, "verified": False, "url": None, "verified_on": None} for p in ["youtube", "linkedin", "instagram", "facebook", "tiktok"]]
        }), encoding="utf-8")
        (self.root / "articles/sample/index.qmd").write_text(
            "---\ntitle: Sample Research\ncontent_id: 360PE-REV-2026-001\nstatus: advance_online\n---\n", encoding="utf-8")
        (self.root / "notes.md").write_text("Evidence sources", encoding="utf-8")
        (self.root / "transcript.md").write_text("Accessible transcript", encoding="utf-8")

    def record(self, status="draft", slug="example-video"):
        return {
            "media_id": "360PE-MED-2026-001",
            "slug": slug,
            "title": "Illustrative video",
            "summary": "A research-grounded explanation.",
            "media_type": "short_video",
            "status": status,
            "published_at": "2026-10-18" if status in {"published", "corrected"} else None,
            "canonical_url": "https://360politicalecology.org/media/" + slug + "/" if status in {"published", "corrected"} else None,
            "source_content_ids": ["360PE-REV-2026-001"],
            "primary_topic": "MIN",
            "secondary_topics": [],
            "source_notes_path": "notes.md",
            "transcript_path": "transcript.md",
            "editorial": {k: status in {"published", "corrected"} for k in ["factual_check", "rights_check", "accessibility_check", "approved"]},
            "distribution": [],
        }

    def write_record(self, record, name="record.yml"):
        (self.root / "_data/media" / name).write_text(yaml.safe_dump(record), encoding="utf-8")

    def test_empty_registry_generates_honest_empty_state(self):
        self.assertEqual(0, generate(self.root))
        archive = (self.root / "_generated_media/archive.md").read_text()
        self.assertIn("No media products have been released", archive)
        self.assertFalse((self.root / "media").exists())

    def test_drafts_and_approved_unreleased_are_hidden(self):
        for status in ("planned", "draft", "in_review", "approved"):
            self.write_record(self.record(status))
            self.assertEqual(0, generate(self.root))
            self.assertFalse((self.root / "media/example-video/index.qmd").exists())
            self.assertNotIn("Illustrative video", (self.root / "_generated_media/archive.md").read_text())

    def test_published_item_is_linked_bidirectionally(self):
        self.write_record(self.record("published"))
        self.assertEqual(1, generate(self.root))
        page = (self.root / "media/example-video/index.qmd").read_text()
        self.assertIn("Sample Research", page)
        self.assertIn("advance online; final issue checks pending", page)
        self.assertIn("transcript.md", page)
        self.assertIn("Illustrative video", (self.root / "_generated_media/archive.md").read_text())
        self.assertIn("Illustrative video", (self.root / "_generated_media/articles/sample.md").read_text())
        self.assertIn("Illustrative video", (self.root / "_generated_media/topics/sample-topic.md").read_text())

    def test_deterministic_and_stale_page_cleanup(self):
        self.write_record(self.record("published"))
        generate(self.root)
        page = (self.root / "media/example-video/index.qmd")
        first = page.read_bytes()
        generate(self.root)
        self.assertEqual(first, page.read_bytes())
        self.write_record(self.record("draft"))
        generate(self.root)
        self.assertFalse(page.exists())

    def test_rejects_duplicate_slug(self):
        self.write_record(self.record("published"))
        second = self.record("published")
        second["media_id"] = "360PE-MED-2026-002"
        self.write_record(second, "second.yml")
        with self.assertRaisesRegex(ValueError, "duplicate public slug"):
            generate(self.root)

    def test_rejects_missing_canonical_or_summary(self):
        record = self.record("published")
        record["canonical_url"] = "https://example.org/media/example-video/"
        self.write_record(record)
        with self.assertRaisesRegex(ValueError, "canonical.*URL"):
            generate(self.root)

    def test_rejects_missing_transcript(self):
        record = self.record("published")
        record["transcript_path"] = "missing.md"
        self.write_record(record)
        with self.assertRaisesRegex(ValueError, "Existing media validation failed"):
            generate(self.root)

    def test_rejects_unverified_external_distribution(self):
        record = self.record("published")
        record["distribution"] = [{"platform": "youtube", "url": "https://youtube.com/watch?v=example", "published_at": "2026-10-18"}]
        self.write_record(record)
        with self.assertRaisesRegex(ValueError, "no verified official account"):
            generate(self.root)

    def test_rejects_unknown_article_id(self):
        record = self.record("published")
        record["source_content_ids"] = ["360PE-REV-2026-999"]
        self.write_record(record)
        with self.assertRaisesRegex(ValueError, "unknown source article"):
            generate(self.root)

    def test_rejects_unapproved_public_release(self):
        record = self.record("published")
        record["editorial"]["approved"] = False
        self.write_record(record)
        with self.assertRaisesRegex(ValueError, "editorial checks"):
            generate(self.root)


if __name__ == "__main__":
    unittest.main()
