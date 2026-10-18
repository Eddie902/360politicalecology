# 360PE Knowledge Architecture V3 — PR 1

This change is a **metadata-only foundation**. It does not change navigation, article claims, logos, PDF assets, publication URLs, or the ten-area historical infographic.

## Registries
- `_data/topics.yml`: four domains and 12 controlled V3 topics.
- `_data/taxonomy-crosswalk.yml`: explicit mapping of all 10 historical thematic areas.
- `_data/content-types.yml`: six editorial formats.

## Publication metadata
Existing article front matter gains `content_id`, `content_type`, `primary_topic`, `secondary_topics`, `geographies`, `analytical_lenses`, `evidence_types`, `content_language`, `status`, and `issue_status`. Quarto-native categories, titles, authors, dates, article bodies and PDF links are unchanged. `advance_online` denotes the actual status of Issue 01; `issue_status: pending_final_checks` explicitly preserves the caveat.

## Validation
Run `python -m pip install PyYAML` then `python scripts/validate_metadata.py`. GitHub Actions runs this check before the existing Quarto render. The workflow retains all existing website regression checks.

## Release boundary
Do not merge this PR until the founder approves. Cloudflare production builds may be triggered by merging into `main`; no deploy step is added here.

## Future PRs
PR 2 will connect V3 topics to navigable pages; PR 3 will introduce social distribution records; PR 4 will strengthen quality and discovery. No future functionality is claimed as already present.

## Compatibility note
Use `content_language` rather than Quarto-reserved `language`; the latter is interpreted as a localization-file reference by Quarto 1.10 and caused the first PR check to fail.
