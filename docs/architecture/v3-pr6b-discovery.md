# 360PE V3 — PR #6B: Research-to-Media Discovery

## Scope
This draft PR adds deterministic build-time media discovery, source-to-media and topic-to-media links, canonical accessible detail-page templates, and synthetic-fixture tests. It adds **no actual media records** and verifies **no official social accounts**. PR #6C remains the first content-release stage.

## Architecture
- `_data/media/*.yml` is the sole canonical source of media records.
- `scripts/validate_media.py` enforces existing source IDs, topic IDs, editorial release checks, transcripts, and verified distribution accounts.
- `scripts/build_media.py` refuses invalid public records and generates untracked `_generated_media/archive.md`, article/topic related-media snippets, and `media/<slug>/index.qmd` detail pages.
- `media.qmd`, each topic page, and the existing article include the generated snippets. Empty snippets are inert; no fake media are listed.
- `_quarto.yml` renders nested media pages when published records exist.
- GitHub Actions and the Cloudflare build script run the generator **before** Quarto. The production branch is unaffected unless this PR is explicitly merged.
- The existing 360PE Review RSS feed is article-only. It is not changed to include media.

## Public visibility
- `planned`, `draft`, `in_review`, `approved`: never publicly listed or rendered.
- `published`, `corrected`: publicly rendered only after existing media validator and new canonical-slug, summary, thumbnail and correction checks.
- `withdrawn`, `archived`: not promoted or rendered by this version. A separate editorial decision is needed to retain withdrawal notices in future.
- Public media detail pages link to their original research, sources, research topics, and accessible transcript file; they do not auto-load third-party embeds.
- Research article `advance_online` and pending issue-check statuses are preserved in related media pages.

## Release metadata
A published record requires the PR #6A fields plus:
- `slug`: lowercase hyphenated path segment, unique across published media
- `summary`: non-empty editorial abstract
- `canonical_url`: exactly `https://360politicalecology.org/media/<slug>/`
- optional `thumbnail_path` plus `thumbnail_alt`
- `correction_notice` when status is `corrected`

Publication date, source notes, transcript (audio/video), editorial approval and verified external distribution rules remain as established in PR #6A.

## Safety and review
- The generator never modifies hand-authored media pages. It removes only generated pages carrying its own marker.
- Build artifacts are ignored by Git; running the generator twice with unchanged inputs yields identical output.
- Tests use **temporary directories only** for synthetic publications, and never add example content to the public registry.
- Verify mobile navigation, no false social links, the unchanged twelve-topic taxonomy and ten-area infographic, article PDFs, RSS, sitemap, and official branding before merge.
- No social posting, account verification, production deployment, or merge is authorized by this PR.

## Manual content release later
1. Prepare actual content and source documentation.
2. Approve editorial and accessibility checks.
3. Verify account ownership only if an external distribution URL is to be claimed.
4. Add a real YAML record with matching canonical slug.
5. Build, preview, review and separately approve production release.
