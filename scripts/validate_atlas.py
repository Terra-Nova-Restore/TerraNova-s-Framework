import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


REQUIRED_TOP_LEVEL_KEYS = {
    "workspace",
    "source",
    "stats",
    "themes",
    "objects",
    "relations",
    "open_gaps",
}

REQUIRED_THEME_KEYS = {"id", "title", "summary", "priority", "status", "object_ids"}
REQUIRED_OBJECT_KEYS = {"id", "kind", "title", "theme_ids", "summary", "status", "source_refs", "tags"}
REQUIRED_RELATION_KEYS = {"from", "to", "type", "note"}
REQUIRED_GAP_KEYS = {"id", "title", "description", "status", "source_refs"}

ALLOWED_KINDS = {
    "page",
    "database",
    "trigger",
    "trigger_cluster",
    "framework",
    "formula",
    "contract",
    "product",
    "patent",
    "public_domain",
    "agent",
}


def fail(errors: list[str]) -> None:
    for error in errors:
        print(f"ERROR: {error}")
    raise SystemExit(1)


def main() -> None:
    manifest_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("atlas/atlas.manifest.v1.json")
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors: list[str] = []

    missing_top_level = REQUIRED_TOP_LEVEL_KEYS - set(data.keys())
    if missing_top_level:
        errors.append(f"Manifest is missing top-level keys: {sorted(missing_top_level)}")

    themes = data.get("themes", [])
    objects = data.get("objects", [])
    relations = data.get("relations", [])
    open_gaps = data.get("open_gaps", [])
    stats = data.get("stats", {})

    if not isinstance(themes, list) or not themes:
        errors.append("`themes` must be a non-empty list.")
    if not isinstance(objects, list) or not objects:
        errors.append("`objects` must be a non-empty list.")
    if not isinstance(relations, list):
        errors.append("`relations` must be a list.")
    if not isinstance(open_gaps, list):
        errors.append("`open_gaps` must be a list.")

    theme_ids = set()
    object_ids = set()
    theme_membership_from_theme = defaultdict(set)
    theme_membership_from_object = defaultdict(set)

    for theme in themes:
        missing = REQUIRED_THEME_KEYS - set(theme.keys())
        if missing:
            errors.append(f"Theme `{theme.get('id', '<missing>')}` is missing keys: {sorted(missing)}")
            continue
        theme_id = theme["id"]
        if theme_id in theme_ids:
            errors.append(f"Duplicate theme id: {theme_id}")
        theme_ids.add(theme_id)
        if not isinstance(theme["object_ids"], list):
            errors.append(f"Theme `{theme_id}` has non-list `object_ids`.")
            continue
        for obj_id in theme["object_ids"]:
            theme_membership_from_theme[theme_id].add(obj_id)

    for obj in objects:
        missing = REQUIRED_OBJECT_KEYS - set(obj.keys())
        if missing:
            errors.append(f"Object `{obj.get('id', '<missing>')}` is missing keys: {sorted(missing)}")
            continue
        obj_id = obj["id"]
        if obj_id in object_ids:
            errors.append(f"Duplicate object id: {obj_id}")
        object_ids.add(obj_id)
        if obj["kind"] not in ALLOWED_KINDS:
            errors.append(f"Object `{obj_id}` has invalid kind `{obj['kind']}`.")
        if not isinstance(obj["theme_ids"], list) or not obj["theme_ids"]:
            errors.append(f"Object `{obj_id}` must have at least one theme id.")
            continue
        for theme_id in obj["theme_ids"]:
            theme_membership_from_object[theme_id].add(obj_id)
            if theme_id not in theme_ids:
                errors.append(f"Object `{obj_id}` references unknown theme `{theme_id}`.")

    for theme in themes:
        theme_id = theme["id"]
        for obj_id in theme_membership_from_theme[theme_id]:
            if obj_id not in object_ids:
                errors.append(f"Theme `{theme_id}` references unknown object `{obj_id}`.")
        if theme_membership_from_theme[theme_id] != theme_membership_from_object[theme_id]:
            missing_from_theme = sorted(theme_membership_from_object[theme_id] - theme_membership_from_theme[theme_id])
            missing_from_object = sorted(theme_membership_from_theme[theme_id] - theme_membership_from_object[theme_id])
            if missing_from_theme:
                errors.append(f"Theme `{theme_id}` is missing objects declared by those objects: {missing_from_theme}")
            if missing_from_object:
                errors.append(f"Theme `{theme_id}` contains objects that do not point back to it: {missing_from_object}")

    for relation in relations:
        missing = REQUIRED_RELATION_KEYS - set(relation.keys())
        if missing:
            errors.append(f"Relation `{relation}` is missing keys: {sorted(missing)}")
            continue
        if relation["from"] not in object_ids:
            errors.append(f"Relation source `{relation['from']}` does not exist.")
        if relation["to"] not in object_ids:
            errors.append(f"Relation target `{relation['to']}` does not exist.")

    gap_ids = set()
    for gap in open_gaps:
        missing = REQUIRED_GAP_KEYS - set(gap.keys())
        if missing:
            errors.append(f"Open gap `{gap.get('id', '<missing>')}` is missing keys: {sorted(missing)}")
            continue
        if gap["id"] in gap_ids:
            errors.append(f"Duplicate open gap id: {gap['id']}")
        gap_ids.add(gap["id"])

    expected_kind_counts = dict(sorted(Counter(obj["kind"] for obj in objects).items()))
    if stats.get("theme_count") != len(themes):
        errors.append(f"stats.theme_count={stats.get('theme_count')} does not match {len(themes)} themes.")
    if stats.get("object_count") != len(objects):
        errors.append(f"stats.object_count={stats.get('object_count')} does not match {len(objects)} objects.")
    if stats.get("relation_count") != len(relations):
        errors.append(f"stats.relation_count={stats.get('relation_count')} does not match {len(relations)} relations.")
    if stats.get("open_gap_count") != len(open_gaps):
        errors.append(f"stats.open_gap_count={stats.get('open_gap_count')} does not match {len(open_gaps)} open gaps.")
    if stats.get("objects_by_kind") != expected_kind_counts:
        errors.append("stats.objects_by_kind does not match actual object-kind counts.")

    if errors:
        fail(errors)

    print(f"OK: validated {manifest_path}")
    print(f"OK: themes={len(themes)} objects={len(objects)} relations={len(relations)} open_gaps={len(open_gaps)}")
    print(f"OK: object kinds={expected_kind_counts}")


if __name__ == "__main__":
    main()
