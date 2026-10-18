# 360PE V3 — PR #6A Media & Dialogues Foundation

## Scope and release boundaries

PR #6A adds a Media & Dialogues informational page, top-level navigation, scoped responsive styles, controlled delivery-format metadata, a verified-account registry, a canonical media-record directory, and automated validation with tests. It does **not** publish any media, invent official social handles, integrate social APIs, post to external platforms, modify existing article content, or change Cloudflare/DNS settings.

## Institutional architecture

- **360PE Review** remains the research-informed publication and authoritative source for long-form analysis.
- **Research & Data** holds methods, evidence documentation, and reproducibility resources.
- **Media & Dialogues** provides public explanation and dialogue, with source attribution and editorial accountability.
- The twelve-topic taxonomy remains the sole thematic classification.
- Existing six editorial content types remain unchanged; media types describe **delivery formats** only.

## Metadata design

- `_data/media-types.yml`: allowed media delivery formats, platforms, and lifecycle states.
- `_data/social-platforms.yml`: one account per platform; unverified entries have null URLs and verification dates.
- `_data/media/<media-id>.yml`: one canonical media asset per file, with `media_id`, `media_type`, `status`, `source_content_ids`, `primary_topic`, optional `secondary_topics`, `editorial`, and optional `distribution` events.
- Platform distribution events are distinct from the intellectual media record and require verified official account records and actual release URLs.
- Planned and draft records are internal; the public Media page is informational until a subsequent approved PR adds real records and listings.
- Publication dates and canonical URLs are not fabricated. Public video/audio records require transcripts and source notes checked into the repository.
- Validator prevents path traversal for source notes/transcripts and enforces official HTTPS platform hostnames.

## Editorial release gates

1. Source article ID and controlled topic codes exist.
2. Factual, rights, accessibility, and editorial approval flags are all true.
3. Published/corrected media has a real release date, 360PE canonical URL, source notes, and video/audio transcript.
4. Every platform distribution has a verified account, an actual HTTPS platform URL, and a publication date.
5. Corrections must be recorded and substantive changes disclosed in accordance with editorial standards.

## PR #6A review checklist

1. Python media validator and unit tests pass.
2. Quarto renders the Media page and the pre-existing article, topic, RSS, branding, and sitemap outputs.
3. Navigation and mobile presentation are visually checked in branch preview.
4. No unverified social links, invented releases, or placeholder published content appear.
5. No existing URL, article body, logo, original ten-area infographic, or Cloudflare production configuration changes.
6. Draft PR remains unmerged until founder approval. GitHub branch previews, if Cloudflare generates them automatically, are not production deployments.

## Deferred

PR #6B: real media records, approved listings, publication-to-media links, transcript pages, and media discovery.
PR #6C: the first editorially approved cross-platform research-to-media campaign. No social posting is performed by this repository.
