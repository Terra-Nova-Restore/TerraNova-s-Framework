#!/usr/bin/env python3
"""Build public-safe workspace correlation metrics from a local Notion export.

The script preserves relation structure without printing raw Notion URLs, page
IDs or titles. It is intentionally conservative: it emits aggregate axis counts,
axis co-occurrences and publication-lane counts. A private row map can be added
later, but it must stay outside public GitHub unless explicitly reviewed.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import urllib.parse
from collections import Counter
from itertools import combinations
from pathlib import Path


URL_RE = re.compile(r"(?:https?://)?(?:www\.)?notion\.so/[^\s)\]>\"']+", re.IGNORECASE)
UUID32_RE = re.compile(r"([0-9a-f]{32})$", re.IGNORECASE)
DASHED_UUID_RE = re.compile(
    r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
    re.IGNORECASE,
)

AXIS_RULES: dict[str, tuple[str, ...]] = {
    "notion_workspace": ("notion",),
    "control_tower": (
        "cap",
        "control",
        "tower",
        "cognitive",
        "terranova",
        "terra-nova",
        "ferrai",
        "equilibrium",
        "ora",
        "triquetra",
        "cic",
    ),
    "trigger": ("trigger", "trg", "sessionstart", "preflight", "fff"),
    "tokenomics": (
        "token",
        "dao",
        "wallet",
        "nft",
        "staking",
        "ferr",
        "ferrcoin",
        "license",
        "lizenz",
    ),
    "mermaid": ("mermaid", "mmd", "diagram", "graph", "flowchart"),
    "patent_ip": ("patent", "tnpx", "ige", "ip-", "intellectual", "schutz", "rechte"),
    "metarotik": ("metarotik", "metaerotik", "erotik", "intim", "flutung", "koerper", "körper"),
    "prism_zenodo": ("prism", "zenodo", "latex", "monographie", "doi", "rc01"),
    "github_sync": ("github", "sync", "delta", "repository", "repo", "pull-request", "pr-"),
    "chatgpt_export": ("chatgpt", "gpt", "codex", "prompt", "export"),
}

AXIS_ORDER = [
    "notion_workspace",
    "control_tower",
    "trigger",
    "tokenomics",
    "mermaid",
    "patent_ip",
    "metarotik",
    "prism_zenodo",
    "github_sync",
    "chatgpt_export",
]


def normalize_url(raw: str) -> str:
    if raw.startswith("http://") or raw.startswith("https://"):
        return raw
    return f"https://{raw}"


def page_id_from_path(path: str) -> tuple[str | None, str]:
    last = path.rstrip("/").split("/")[-1]
    match = UUID32_RE.search(last) or DASHED_UUID_RE.search(last)
    if not match:
        return None, urllib.parse.unquote(last).strip() or "(no-slug)"

    page_id = match.group(1).replace("-", "").lower()
    slug = urllib.parse.unquote(last[: match.start(1)].rstrip("-")).strip() or "(no-slug)"
    return page_id, slug


def classify_axes(slug: str) -> set[str]:
    normalized = slug.lower()
    axes = {"notion_workspace"}
    for axis, needles in AXIS_RULES.items():
        if axis == "notion_workspace":
            continue
        if any(needle in normalized for needle in needles):
            axes.add(axis)
    return axes


def publication_lane(axes: set[str]) -> str:
    if "patent_ip" in axes:
        return "public_after_ip_review"
    if "tokenomics" in axes:
        return "public_after_biz_review"
    if "metarotik" in axes:
        return "public_after_phenomenology_review"
    if "trigger" in axes:
        return "trigger_module_candidate"
    if "mermaid" in axes:
        return "diagram_bridge_candidate"
    if "chatgpt_export" in axes:
        return "chat_export_correlation_candidate"
    if "prism_zenodo" in axes:
        return "evidence_apparatus_candidate"
    if "github_sync" in axes:
        return "sync_trace_candidate"
    if "control_tower" in axes:
        return "control_tower_candidate"
    return "workspace_index_candidate"


def analyze(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    text = data.decode("utf-8-sig", errors="replace")
    urls = [normalize_url(match) for match in URL_RE.findall(text)]

    page_axes: dict[str, set[str]] = {}
    page_lanes: dict[str, str] = {}
    view_urls = 0
    anchor_urls = 0

    for url in urls:
        parsed = urllib.parse.urlparse(url)
        if "v=" in parsed.query:
            view_urls += 1
        if parsed.fragment:
            anchor_urls += 1

        page_id, slug = page_id_from_path(parsed.path)
        if page_id is None:
            continue

        axes = classify_axes(slug)
        page_axes.setdefault(page_id, set()).update(axes)

    for page_id, axes in page_axes.items():
        page_lanes[page_id] = publication_lane(axes)

    axis_counts: Counter[str] = Counter()
    cooccurrence_counts: Counter[tuple[str, str]] = Counter()
    lane_counts: Counter[str] = Counter(page_lanes.values())

    for axes in page_axes.values():
        for axis in axes:
            axis_counts[axis] += 1
        for left, right in combinations(sorted(axes), 2):
            cooccurrence_counts[(left, right)] += 1

    return {
        "source": {
            "label": path.name,
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
        },
        "metrics": {
            "urls_seen": len(urls),
            "unique_page_refs": len(page_axes),
            "database_view_urls_with_v": view_urls,
            "block_anchor_urls": anchor_urls,
            "axis_count": len(AXIS_ORDER),
            "publication_lane_count": len(lane_counts),
        },
        "axis_counts": dict(sorted(axis_counts.items())),
        "axis_cooccurrences": {
            f"{left}|{right}": count
            for (left, right), count in sorted(cooccurrence_counts.items())
        },
        "publication_lanes": dict(sorted(lane_counts.items())),
        "redaction": {
            "raw_urls_printed": False,
            "raw_page_ids_printed": False,
            "raw_titles_printed": False,
            "raw_content_printed": False,
        },
        "boundary": {
            "silvan_related_default": "public_after_professional_framing",
            "exceptions": [
                "private_third_parties",
                "accounts",
                "raw_identities",
                "intimate_real_names",
                "security_material",
                "unreviewed_ip_specifics",
            ],
            "correlation_rule": "Do not remove relation axes during redaction.",
        },
    }


def write_axis_counts(path: Path, axis_counts: dict[str, int]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Axis", "Page Count", "Publication Meaning"])
        meanings = {
            "notion_workspace": "Workspace membership baseline.",
            "control_tower": "CAP, Equilibrium, ORA, Triquetra or CIC control surface.",
            "trigger": "Trigger architecture, command surface or module candidate.",
            "tokenomics": "Tokenomics, DAO, wallet, license or commercial-governance surface.",
            "mermaid": "Mermaid/MMD graph, diagram or visual bridge surface.",
            "patent_ip": "Patent, IGE, TNPX, IP or rights-related surface.",
            "metarotik": "Metarotik, intimacy, somatic or phenomenological resonance surface.",
            "prism_zenodo": "Prism, Zenodo, DOI, LaTeX or monograph evidence surface.",
            "github_sync": "GitHub, sync, delta, repo or PR trace surface.",
            "chatgpt_export": "ChatGPT/Codex/export dialogue surface.",
        }
        for axis in AXIS_ORDER:
            writer.writerow([axis, axis_counts.get(axis, 0), meanings[axis]])


def write_cooccurrences(path: Path, cooccurrences: dict[str, int]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Axis A", "Axis B", "Shared Page Count"])
        for key, count in sorted(cooccurrences.items()):
            left, right = key.split("|", 1)
            writer.writerow([left, right, count])


def write_lanes(path: Path, lanes: dict[str, int]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Publication Lane", "Page Count", "Rule"])
        rules = {
            "public_after_ip_review": "Keep correlation; review IP/legal specifics before public text.",
            "public_after_biz_review": "Keep correlation; review tokenomics and commercial claims.",
            "public_after_phenomenology_review": "Keep correlation; frame Metarotik professionally before release.",
            "trigger_module_candidate": "Convert to trigger-module source review before canon claim.",
            "diagram_bridge_candidate": "Route through MMD bridge before trigger/canon use.",
            "chat_export_correlation_candidate": "Wait for ChatGPT export pass before final correlation.",
            "evidence_apparatus_candidate": "Route through Prism/Zenodo evidence apparatus.",
            "sync_trace_candidate": "Route through GitHub/Notion sync trace.",
            "control_tower_candidate": "Route through CAP/Equilibrium control tower.",
            "workspace_index_candidate": "Keep as indexed workspace object until classified.",
        }
        for lane, count in sorted(lanes.items()):
            writer.writerow([lane, count, rules[lane]])


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="Local Notion Home export text file.")
    parser.add_argument("--output-dir", required=True, help="Directory for public-safe outputs.")
    parser.add_argument("--expect-sha256", help="Expected SHA-256 for the source file.")
    args = parser.parse_args(argv[1:])

    source = Path(args.source)
    output_dir = Path(args.output_dir)
    if not source.is_file():
        print(f"not a file: {source}", file=sys.stderr)
        return 2

    result = analyze(source)
    if args.expect_sha256 and result["source"]["sha256"] != args.expect_sha256:
        print(
            "sha256 mismatch: "
            f"expected {args.expect_sha256}, got {result['source']['sha256']}",
            file=sys.stderr,
        )
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)
    write_axis_counts(output_dir / "workspace-corr-001.axis-counts.csv", result["axis_counts"])
    write_cooccurrences(
        output_dir / "workspace-corr-001.axis-cooccurrence.csv",
        result["axis_cooccurrences"],
    )
    write_lanes(
        output_dir / "workspace-corr-001.publication-lane-counts.csv",
        result["publication_lanes"],
    )
    summary_path = output_dir / "workspace-corr-001.review-summary.json"
    summary_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(result["metrics"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
