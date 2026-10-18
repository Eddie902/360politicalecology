"""Focused regression tests for 360PE media publication safeguards."""
import tempfile
import unittest
from pathlib import Path

from scripts.validate_media import (
    validate_accounts, validate_record, valid_url, valid_local_file,
)

PLATFORMS = {"youtube", "linkedin", "instagram", "facebook", "tiktok"}
MEDIA_TYPES = {"short_video", "long_video", "interview", "audio", "carousel", "infographic"}
TOPICS = {"MIN", "ENE", "GOV", "JUS"}
SOURCES = {"360PE-REV-2026-001"}


def draft_record():
    return {
        "media_id": "360PE-MED-2026-001",
        "title": "Illustrative draft",
        "media_type": "short_video",
        "status": "planned",
        "source_content_ids": ["360PE-REV-2026-001"],
        "primary_topic": "MIN",
        "secondary_topics": ["ENE"],
        "editorial": {
            "factual_check": False,
            "rights_check": False,
            "accessibility_check": False,
            "approved": False,
        },
        "distribution": [],
    }


class MediaValidationTests(unittest.TestCase):
    def test_valid_planned_record_is_not_published(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual([], validate_record(draft_record(), Path(temp), MEDIA_TYPES, PLATFORMS, TOPICS, SOURCES, set()))

    def test_unknown_source_is_rejected(self):
        record = draft_record()
        record["source_content_ids"] = ["360PE-REV-2026-999"]
        with tempfile.TemporaryDirectory() as temp:
            self.assertTrue(any("unknown source" in e for e in validate_record(record, Path(temp), MEDIA_TYPES, PLATFORMS, TOPICS, SOURCES, set())))

    def test_unapproved_published_record_is_rejected(self):
        record = draft_record()
        record["status"] = "published"
        with tempfile.TemporaryDirectory() as temp:
            errors = validate_record(record, Path(temp), MEDIA_TYPES, PLATFORMS, TOPICS, SOURCES, set())
        self.assertTrue(any("editorial checks" in e for e in errors))
        self.assertTrue(any("transcript_path" in e for e in errors))
        self.assertTrue(any("canonical" in e for e in errors))

    def test_unverified_account_cannot_assert_url(self):
        accounts = [{"platform": p, "verified": False, "url": None, "verified_on": None} for p in sorted(PLATFORMS)]
        errors, verified = validate_accounts(accounts, PLATFORMS)
        self.assertEqual([], errors)
        self.assertEqual(set(), verified)
        accounts[0]["url"] = "https://www.facebook.com/example"
        errors, _ = validate_accounts(accounts, PLATFORMS)
        self.assertTrue(any("unverified account" in e for e in errors))

    def test_distribution_requires_verified_account(self):
        record = draft_record()
        record["distribution"] = [{"platform": "youtube", "url": "https://youtube.com/watch?v=example", "published_at": "2026-10-18"}]
        with tempfile.TemporaryDirectory() as temp:
            errors = validate_record(record, Path(temp), MEDIA_TYPES, PLATFORMS, TOPICS, SOURCES, set())
        self.assertTrue(any("unreleased" in e for e in errors))
        self.assertTrue(any("no verified official account" in e for e in errors))

    def test_https_domain_validation_blocks_impostor(self):
        self.assertTrue(valid_url("https://www.youtube.com/watch?v=test", {"youtube.com"}))
        self.assertFalse(valid_url("https://youtube.com.evil.example/watch", {"youtube.com"}))
        self.assertFalse(valid_url("http://youtube.com/watch", {"youtube.com"}))

    def test_local_paths_must_stay_within_repository(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "notes.txt").write_text("Source notes", encoding="utf-8")
            self.assertTrue(valid_local_file(root, "notes.txt"))
            self.assertFalse(valid_local_file(root, "../notes.txt"))


if __name__ == "__main__":
    unittest.main()
