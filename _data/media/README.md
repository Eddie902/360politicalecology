# 360PE Media Records (PR #6A)

This directory is intentionally empty of publication records until a real media item has been approved. One `.yml` file per media item is the canonical source. The repository's `_data/media-types.yml` defines controlled values.

A record represents one intellectual media asset. Platform releases are separate entries in `distribution`, so the same video can be released on different platforms without duplicating the source record.

Example **not to publish** (illustrative only):

```yaml
media_id: "360PE-MED-2026-001"
title: "Example only"
media_type: short_video
status: planned
source_content_ids: ["360PE-REV-2026-001"]
primary_topic: MIN
secondary_topics: [ENE, GOV, JUS]
editorial:
  factual_check: false
  rights_check: false
  accessibility_check: false
  approved: false
distribution: []
```

For `published` or `corrected` records, include a real ISO `published_at` date, a stable `canonical_url` on the 360PE website, a valid `source_notes_path` within the repository, and `editorial` flags all true. For video/audio, include a valid `transcript_path`. Any external release must include `platform`, `url`, and `published_at`; the corresponding official account must first be verified in `_data/social-platforms.yml`.

Only add actual records after editorial approval. Do not create placeholder public posts, fake handles, or fictitious publication dates. The media landing page is informational until PR #6B introduces approved listings.
