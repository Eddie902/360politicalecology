#!/usr/bin/env python3
"""Validate 360PE PR #6A media and official-account registries.

Runs without changing any website content. The media archive may be empty.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from urllib.parse import urlparse
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
HOSTS = {
    "youtube": {"youtube.com", "youtu.be"},
    "linkedin": {"linkedin.com"},
    "instagram": {"instagram.com"},
    "facebook": {"facebook.com", "fb.com", "fb.watch"},
    "tiktok": {"tiktok.com"},
}
STATUSES = {"planned", "draft", "in_review", "approved", "published", "corrected", "withdrawn", "archived"}
PUBLIC = {"published", "corrected"}
ID_PATTERN = re.compile(r"360PE-MED-\d{4}-\d{3,}")
ARTICLE_ID = re.compile(r"360PE-[A-Z]+-\d{4}-\d{3,}")


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
    return yaml.load(path.read_text(encoding="utf-8-sig"), Loader=UniqueLoader)


def valid_url(value, allowed_hosts):
    if not isinstance(value, str):
        return False
    try:
        parsed = urlparse(value)
        host = (parsed.hostname or "").lower()
        return (parsed.scheme == "https" and parsed.username is None
                and parsed.password is None and parsed.port in (None, 443)
                and any(host == domain or host.endswith("." + domain) for domain in allowed_hosts))
    except ValueError:
        return False


def valid_date(value):
    if isinstance(value, date):
        return True
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def valid_local_file(root, value):
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return False
    return candidate.is_file()


def article_ids(root):
    ids = set()
    for path in (root / "articles").rglob("*.qmd"):
        raw = path.read_text(encoding="utf-8-sig")
        match = re.match(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", raw, flags=re.S)
        if not match:
            continue
        data = yaml.load(match.group(1), Loader=UniqueLoader) or {}
        if data.get("content_id"):
            ids.add(str(data["content_id"]))
    return ids


def validate_accounts(accounts, platforms):
    errors, verified = [], set()
    if not isinstance(accounts, list):
        return ["accounts must be a list"], verified
    seen = set()
    for item in accounts:
        if not isinstance(item, dict):
            errors.append("account entry must be a mapping")
            continue
        platform = item.get("platform")
        if platform not in platforms or platform not in HOSTS:
            errors.append(f"unknown account platform: {platform}")
            continue
        if platform in seen:
            errors.append(f"duplicate account platform: {platform}")
        seen.add(platform)
        flag = item.get("verified")
        if not isinstance(flag, bool):
            errors.append(f"{platform}: verified must be boolean")
            continue
        url, verified_on = item.get("url"), item.get("verified_on")
        if flag:
            if not valid_url(url, HOSTS[platform]):
                errors.append(f"{platform}: verified account needs a valid official HTTPS URL")
            if not valid_date(verified_on):
                errors.append(f"{platform}: verified account needs verified_on date")
            if valid_url(url, HOSTS[platform]) and valid_date(verified_on):
                verified.add(platform)
        elif url is not None or verified_on is not None:
            errors.append(f"{platform}: unverified account must not assert URL/date")
    if seen != set(platforms):
        errors.append("account registry must enumerate all controlled platforms exactly once")
    return errors, verified


def validate_record(record, root, media_types, platforms, topics, sources, verified):
    errors = []
    if not isinstance(record, dict):
        return ["media record must be a mapping"]
    media_id = record.get("media_id")
    prefix = str(media_id or "<missing>")
    if not isinstance(media_id, str) or not ID_PATTERN.fullmatch(media_id):
        errors.append(f"{prefix}: invalid media_id")
    if not isinstance(record.get("title"), str) or not record["title"].strip():
        errors.append(f"{prefix}: missing title")
    if record.get("media_type") not in media_types:
        errors.append(f"{prefix}: invalid media_type")
    status = record.get("status")
    if status not in STATUSES:
        errors.append(f"{prefix}: invalid status")
    source_ids = record.get("source_content_ids")
    if not isinstance(source_ids, list) or not source_ids:
        errors.append(f"{prefix}: source_content_ids must be nonempty list")
    else:
        if len(source_ids) != len(set(map(str, source_ids))):
            errors.append(f"{prefix}: duplicate source_content_ids")
        for source in source_ids:
            if not isinstance(source, str) or not ARTICLE_ID.fullmatch(source) or source not in sources:
                errors.append(f"{prefix}: unknown source article {source}")
    primary = record.get("primary_topic")
    secondary = record.get("secondary_topics", [])
    if primary not in topics:
        errors.append(f"{prefix}: invalid primary_topic")
    if not isinstance(secondary, list):
        errors.append(f"{prefix}: secondary_topics must be a list")
        secondary = []
    if any(s not in topics for s in secondary) or primary in secondary or len(set(map(str, secondary))) != len(secondary) or len(secondary) > 3:
        errors.append(f"{prefix}: invalid secondary_topics")
    editorial = record.get("editorial", {})
    if not isinstance(editorial, dict) or any(not isinstance(editorial.get(k), bool) for k in ("factual_check", "rights_check", "accessibility_check", "approved")):
        errors.append(f"{prefix}: editorial requires four boolean checks")
        editorial = {}
    if status in PUBLIC:
        if not valid_date(record.get("published_at")):
            errors.append(f"{prefix}: public record requires published_at")
        if not valid_url(record.get("canonical_url"), {"360politicalecology.org"}):
            errors.append(f"{prefix}: public record requires canonical 360PE HTTPS URL")
        if not valid_local_file(root, record.get("source_notes_path")):
            errors.append(f"{prefix}: public record requires existing source_notes_path")
        if record.get("media_type") in {"long_video", "short_video", "interview", "audio"} and not valid_local_file(root, record.get("transcript_path")):
            errors.append(f"{prefix}: public audio/video requires existing transcript_path")
        if not all(editorial.get(k) is True for k in ("factual_check", "rights_check", "accessibility_check", "approved")):
            errors.append(f"{prefix}: public record requires all editorial checks approved")
    distribution = record.get("distribution", [])
    if not isinstance(distribution, list):
        errors.append(f"{prefix}: distribution must be a list")
        distribution = []
    seen_platforms = set()
    for item in distribution:
        if not isinstance(item, dict):
            errors.append(f"{prefix}: distribution entry must be mapping")
            continue
        platform = item.get("platform")
        if platform not in platforms or platform not in HOSTS:
            errors.append(f"{prefix}: unknown distribution platform {platform}")
            continue
        if platform in seen_platforms:
            errors.append(f"{prefix}: duplicate distribution platform {platform}")
        seen_platforms.add(platform)
        if status not in PUBLIC:
            errors.append(f"{prefix}: unreleased media cannot assert external distribution")
        if platform not in verified:
            errors.append(f"{prefix}: distribution platform {platform} has no verified official account")
        if not valid_url(item.get("url"), HOSTS[platform]):
            errors.append(f"{prefix}: invalid {platform} distribution URL")
        if not valid_date(item.get("published_at")):
            errors.append(f"{prefix}: {platform} distribution requires published_at")
    return errors


def validate(root=ROOT):
    errors = []
    try:
        types_doc = read_yaml(root / "_data/media-types.yml")
        accounts_doc = read_yaml(root / "_data/social-platforms.yml")
        topic_doc = read_yaml(root / "_data/topics.yml")
        media_types = [x["id"] for x in types_doc["media_types"]]
        platforms = types_doc["platforms"]
        topics = {x["id"] for x in topic_doc["topics"]}
        if len(media_types) != len(set(media_types)) or not media_types:
            errors.append("duplicate/empty media types")
        if len(platforms) != len(set(platforms)) or set(platforms) != set(HOSTS):
            errors.append("platform registry differs from approved platforms")
        if set(types_doc.get("statuses", [])) != STATUSES:
            errors.append("status registry differs from validator")
        account_errors, verified = validate_accounts(accounts_doc["accounts"], platforms)
        errors.extend(account_errors)
        sources = article_ids(root)
        seen_ids = set()
        files = sorted((root / "_data/media").glob("*.yml"))
        for path in files:
            try:
                record = read_yaml(path)
                errors.extend(validate_record(record, root, set(media_types), set(platforms), topics, sources, verified))
                media_id = record.get("media_id") if isinstance(record, dict) else None
                if media_id in seen_ids:
                    errors.append(f"duplicate media ID: {media_id}")
                seen_ids.add(media_id)
            except (OSError, yaml.YAMLError, ValueError, TypeError) as exc:
                errors.append(f"{path.name}: {exc}")
    except (OSError, yaml.YAMLError, ValueError, TypeError, KeyError) as exc:
        errors.append(f"registry: {exc}")
        files = []
    return errors, len(files)


def main():
    errors, count = validate()
    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        return 1
    print(f"PASS: media registry valid; {count} approved-or-draft records; no account URLs asserted unless verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
