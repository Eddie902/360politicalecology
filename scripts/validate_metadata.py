#!/usr/bin/env python3
"""Validate 360PE V3 taxonomy, crosswalk, formats, and article front matter.

Usage: python scripts/validate_metadata.py
Requires: PyYAML (pip install PyYAML).
No website content is modified.
"""
from __future__ import annotations
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []

class UniqueLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in result:
            raise ValueError(f"Duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node)
    return result

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)

def read_yaml(path):
    try:
        return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        ERRORS.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}

def check_unique(values, label):
    if len(values) != len(set(values)):
        ERRORS.append(f"Duplicate {label}: {values}")

def main():
    taxonomy = read_yaml(ROOT / "_data/topics.yml")
    crosswalk = read_yaml(ROOT / "_data/taxonomy-crosswalk.yml")
    formats = read_yaml(ROOT / "_data/content-types.yml")
    topics = taxonomy.get("topics", [])
    ids = [item.get("id") for item in topics]
    slugs = [item.get("slug") for item in topics]
    domain_ids = {item.get("id") for item in taxonomy.get("domains", [])}
    if len(topics) != 12:
        ERRORS.append(f"Expected 12 V3 topics, got {len(topics)}")
    check_unique(ids, "topic ID")
    check_unique(slugs, "topic slug")
    for item in topics:
        if not all(item.get(k) for k in ("id", "label", "slug", "domain", "description")):
            ERRORS.append(f"Incomplete topic: {item}")
        if item.get("domain") not in domain_ids:
            ERRORS.append(f"Unknown domain: {item}")
        if item.get("slug") and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", item["slug"]):
            ERRORS.append(f"Invalid slug: {item['slug']}")
    mappings = crosswalk.get("mappings", [])
    if len(mappings) != 10:
        ERRORS.append(f"Expected 10 historical mappings, got {len(mappings)}")
    check_unique([str(m.get("legacy_id")) for m in mappings], "historical area ID")
    for m in mappings:
        if not m.get("legacy_label"):
            ERRORS.append(f"Missing legacy label: {m}")
        for topic in [m.get("primary_topic"), *(m.get("secondary_topics") or [])]:
            if topic not in ids:
                ERRORS.append(f"Crosswalk unknown topic {topic}")
    format_ids = [f.get("id") for f in formats.get("content_types", [])]
    check_unique(format_ids, "content type")
    if len(format_ids) != 6:
        ERRORS.append(f"Expected 6 content types, got {len(format_ids)}")
    content_ids = []
    article_paths = sorted((ROOT / "articles").rglob("*.qmd"))
    if not article_paths:
        ERRORS.append("No article source files found")
    for path in article_paths:
        raw = path.read_text(encoding="utf-8-sig")
        match = re.match(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", raw, flags=re.S)
        if not match:
            ERRORS.append(f"{path.relative_to(ROOT)}: missing YAML front matter")
            continue
        try:
            data = yaml.load(match.group(1), Loader=UniqueLoader) or {}
        except (yaml.YAMLError, ValueError) as exc:
            ERRORS.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        for field in ("content_id", "title", "date", "author", "description", "content_type", "primary_topic", "status"):
            if not data.get(field):
                ERRORS.append(f"{path.relative_to(ROOT)}: missing {field}")
        if data.get("content_id"):
            content_ids.append(str(data["content_id"]))
        if data.get("content_type") not in format_ids:
            ERRORS.append(f"{path.relative_to(ROOT)}: invalid content_type")
        primary = data.get("primary_topic")
        secondary = data.get("secondary_topics") or []
        if not isinstance(secondary, list):
            ERRORS.append(f"{path.relative_to(ROOT)}: secondary_topics must be a list")
            secondary = []
        if primary not in ids or any(s not in ids for s in secondary):
            ERRORS.append(f"{path.relative_to(ROOT)}: unknown topic ID")
        if primary in secondary or len(set(secondary)) != len(secondary) or len(secondary) > 3:
            ERRORS.append(f"{path.relative_to(ROOT)}: secondary topics duplicate/over limit")
        if data.get("status") not in ("draft", "under_review", "advance_online", "published", "updated", "archived"):
            ERRORS.append(f"{path.relative_to(ROOT)}: invalid status")
        if not isinstance(data.get("categories"), list) or not data["categories"]:
            ERRORS.append(f"{path.relative_to(ROOT)}: keep Quarto categories")
    check_unique(content_ids, "content ID")
    if ERRORS:
        for error in ERRORS:
            print("ERROR:", error, file=sys.stderr)
        return 1
    print(f"PASS: {len(topics)} topics, {len(mappings)} legacy mappings, {len(format_ids)} formats, {len(article_paths)} articles")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
