#!/usr/bin/env python3
"""Build MMD-006 CAP module registry package from MMD-005 drafts."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTROL_DIR = REPO_ROOT / "docs" / "atlas" / "control-tower"
SCHEMA_PATH = CONTROL_DIR / "object-registry.schema.json"

MODULE_DRAFTS = "mmd-005.cap-module-drafts.csv"
HASH_LEDGER = "mmd-005.hash-ledger.csv"
HASH_MATERIAL = "mmd-005.hash-material.json"

GO_PHRASE = "GO Notion MMD-006 anwenden"

FEEDBACK_MAP = {
    "registry": "Registry",
    "logbook": "Logbook",
    "trigger_map": "Trigger Map",
    "prism_zenodo": "Prism / Zenodo",
    "github_atlas": "GitHub Atlas",
}

PRISM_RELEVANCE_BY_REF = {
    "516": "Not relevant",
    "520": "Not relevant",
    "521": "Not relevant",
    "540": "Backpropagation",
    "544": "Backpropagation",
}


def read_csv(name: str) -> list[dict[str, str]]:
    with (CONTROL_DIR / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def github_anchor(module_id: str) -> str:
    return f"docs/atlas/control-tower/mmd-005.cap-module-drafts.md#{module_id}"


def feedback_target(ref: str, hash_material: dict[str, Any]) -> str:
    raw = (
        hash_material.get("modules", {})
        .get(ref, {})
        .get("material", {})
        .get("feedback_target", "github_atlas")
    )
    return FEEDBACK_MAP.get(raw, "GitHub Atlas")


def build_registry_rows(
    module_rows: list[dict[str, str]], hash_material: dict[str, Any]
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for module in module_rows:
        ref = module["Visible Reference"]
        module_id = module["Draft Module ID"]
        name = f"{module_id} - {module['Working Name']}"
        rows.append(
            {
                "Name": name,
                "Object Type": "GitHub Artifact",
                "Object ID / URL": github_anchor(module_id),
                "Parent / Hub": "CAP 0.1.0 - Workspace Object Registry",
                "Source Layer": "GitHub Atlas",
                "Count Basis": "not counted",
                "Mode": "STUDIO",
                "Trigger Band": "401+",
                "Freedom Mode": "bounded manual",
                "Status": "Indexed",
                "Canon Status": "Candidate",
                "Sensitivity": "Internal",
                "Owner": "Silvan / Codex",
                "Last Edited": "",
                "Last Reviewed": "2026-05-17",
                "Related Canonical Object": "MMD-004 Candidate Review and Canon Gate; Atlas v1.1 Trigger Complement",
                "Causal Chain": "MMD-001 readpass -> MMD-002 extraction -> MMD-003 bridge -> MMD-004 gate -> MMD-005 draft -> MMD-006 registry package",
                "Emergent Coherence Evidence": (
                    f"{module['Evidence Count']} visual evidence row(s), "
                    f"{module['Guard Count']} guard row(s), hash {module['Hash Handle']}; "
                    f"{module['Trigger Cluster']}"
                ),
                "Probabilistic Hypothesis": (
                    f"{module['Working Name']} can function as a bounded CAP draft module for "
                    f"{module['Primary Runtime Role']} while source review remains open."
                ),
                "Deterministic Boundary": (
                    f"{module['Boundary']} No canonical TRG assignment; no external mutation from MMD-006 package alone."
                ),
                "Feedback / Backpropagation Target": feedback_target(ref, hash_material),
                "Prism / Zenodo Relevance": PRISM_RELEVANCE_BY_REF.get(ref, "Unknown"),
                "Understanding State": "grasped",
                "Duplicate Group": "",
                "GitHub Path": github_anchor(module_id),
                "Sync Status": "Needs sync",
                "Equilibrium Notes": "R4 trace, R13 GitHub sync and R16 boundary are explicit; draft hash is not canon.",
            }
        )
    return rows


def field_rule(field_name: str) -> tuple[str, str]:
    rules = {
        "Name": ("MMD-005 Draft Module ID plus working name", "Creates one stable registry title per CAP draft module."),
        "Object Type": ("Fixed value: GitHub Artifact", "The module draft exists locally in GitHub, not as a Notion source page yet."),
        "Object ID / URL": ("Local GitHub path anchor", "Uses repo path text and avoids raw private Notion IDs."),
        "Parent / Hub": ("Fixed value: CAP 0.1.0 - Workspace Object Registry", "Routes rows to the registry control surface."),
        "Source Layer": ("Fixed value: GitHub Atlas", "MMD-005 is a repo-local Atlas artifact."),
        "Count Basis": ("Fixed value: not counted", "Module drafts do not change 777/808/~880 workspace count layers."),
        "Mode": ("Fixed value: STUDIO", "This is system control work."),
        "Trigger Band": ("Fixed value: 401+", "Visible references are 516, 520, 521, 540 and 544."),
        "Freedom Mode": ("Fixed value: bounded manual", "MMD-006 prepares rows; it does not authorize autonomous mutation."),
        "Status": ("Fixed value: Indexed", "Rows are package-ready but not canonical."),
        "Canon Status": ("Fixed value: Candidate", "MMD-004 explicitly blocked canonical TRG assignment."),
        "Sensitivity": ("Fixed value: Internal", "No raw private IDs or restricted trigger expansion included."),
        "Owner": ("Fixed value: Silvan / Codex", "Silvan remains recovery anchor; Codex built the package."),
        "Last Edited": ("Blank", "No external edited date is claimed."),
        "Last Reviewed": ("Fixed date: 2026-05-17", "Matches MMD-006 package creation date."),
        "Related Canonical Object": ("MMD-004 and Atlas v1.1 references", "Links draft rows back to canon gate and source complement."),
        "Causal Chain": ("MMD-001 -> MMD-006 chain", "Makes emergent coherence auditable."),
        "Emergent Coherence Evidence": ("Evidence count, guard count, hash handle, cluster", "Summarizes why each row exists."),
        "Probabilistic Hypothesis": ("Module role hypothesis", "States draft usefulness without final truth claim."),
        "Deterministic Boundary": ("MMD-005 boundary plus no-mutation clause", "Prevents registry package from becoming silent action."),
        "Feedback / Backpropagation Target": ("Mapped from MMD-005 hash material", "Preserves module-specific feedback route."),
        "Prism / Zenodo Relevance": ("540/544 Backpropagation, others Not relevant", "Keeps Prism link focused."),
        "Understanding State": ("Fixed value: grasped", "Drafts are understood enough for registry sync, not final canon."),
        "Duplicate Group": ("Blank", "No duplicate row claim."),
        "GitHub Path": ("Local GitHub path anchor", "Keeps sync trace local and reviewable."),
        "Sync Status": ("Fixed value: Needs sync", "Rows are not live in Notion yet."),
        "Equilibrium Notes": ("Fixed R4/R13/R16 note", "Trace, GitHub sync and boundary are explicit."),
    }
    return rules.get(field_name, ("Package source rule", "Mapped from schema."))


def build_field_map(schema: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for field in schema["fields"]:
        rule, boundary = field_rule(field["name"])
        rows.append(
            {
                "Registry Field": field["name"],
                "Schema Type": field["type"],
                "Required": str(field.get("required", False)),
                "MMD-006 Source Rule": rule,
                "Boundary": boundary,
            }
        )
    return rows


def build_view_package() -> list[dict[str, str]]:
    return [
        {
            "View Name": "CAP Module Drafts",
            "Target": "CAP registry database",
            "View Type": "Table",
            "Filter": "Object Type = GitHub Artifact AND Canon Status = Candidate AND GitHub Path contains mmd-005.cap-module-drafts",
            "Sort": "Name ascending",
            "Requires GO": "Yes",
            "Boundary": "View only; no schema change and no row mutation beyond MMD-006 package.",
        },
        {
            "View Name": "CAP Module Sync Needed",
            "Target": "CAP registry database",
            "View Type": "Table",
            "Filter": "Sync Status = Needs sync AND GitHub Path contains mmd-005.cap-module-drafts",
            "Sort": "Feedback / Backpropagation Target ascending, Name ascending",
            "Requires GO": "Yes",
            "Boundary": "View only; supports manual follow-up after package application.",
        },
    ]


def build_mutation_package(registry_rows: list[dict[str, str]], view_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "Mutation ID": "MMD-006-A",
            "Target": "CAP registry data source",
            "Mutation Type": "Create rows",
            "Exact Intent": "Create five CAP module draft rows exactly from mmd-006.registry-package.csv.",
            "Source File": "mmd-006.registry-package.csv",
            "Row Count": str(len(registry_rows)),
            "Requires GO": f"Yes - exact phrase: {GO_PHRASE}",
            "External Mutation Risk": "Low",
            "Blocked Content": "deletion; schema change; canonical TRG assignment; raw private IDs; restricted trigger expansion",
            "Expected Result": "The five MMD-005 draft modules become visible as Candidate rows in the live CAP registry.",
        },
        {
            "Mutation ID": "MMD-006-B",
            "Target": "CAP registry database",
            "Mutation Type": "Create view",
            "Exact Intent": f"Create view {view_rows[0]['View Name']} using mmd-006.view-package.csv.",
            "Source File": "mmd-006.view-package.csv",
            "Row Count": "1",
            "Requires GO": f"Yes - exact phrase: {GO_PHRASE}",
            "External Mutation Risk": "Low",
            "Blocked Content": "schema change; deletion; broad workspace crawl",
            "Expected Result": "CAP module draft rows are easy to inspect in Notion.",
        },
        {
            "Mutation ID": "MMD-006-C",
            "Target": "CAP registry database",
            "Mutation Type": "Create view",
            "Exact Intent": f"Create view {view_rows[1]['View Name']} using mmd-006.view-package.csv.",
            "Source File": "mmd-006.view-package.csv",
            "Row Count": "1",
            "Requires GO": f"Yes - exact phrase: {GO_PHRASE}",
            "External Mutation Risk": "Low",
            "Blocked Content": "schema change; deletion; broad workspace crawl",
            "Expected Result": "Unsynced CAP module draft rows have a review surface.",
        },
        {
            "Mutation ID": "MMD-006-D",
            "Target": "CAP page",
            "Mutation Type": "Append content",
            "Exact Intent": "Append a short MMD-005/MMD-006 checkpoint and the no-canon/no-delete boundary.",
            "Source File": "mmd-006.apply-gate.md",
            "Row Count": "1",
            "Requires GO": f"Yes - exact phrase: {GO_PHRASE}",
            "External Mutation Risk": "Low",
            "Blocked Content": "raw private inventory; restricted trigger detail; publication claim",
            "Expected Result": "CAP page points to the new local module-draft registry package.",
        },
    ]


def build_markdown(summary: dict[str, Any], registry_rows: list[dict[str, str]]) -> str:
    lines = [
        "# MMD-006 - CAP Module Registry Package",
        "",
        "Status: prepared",
        "",
        "Date: 2026-05-17",
        "",
        "## Decision",
        "",
        "MMD-006 prepares a Notion-safe registry package for the five MMD-005 CAP module drafts.",
        "",
        "This is not a Notion mutation. It is an application package that can be applied later only with explicit authorization.",
        "",
        "## Registry Rows",
        "",
        "| Name | Trigger Ref | Feedback Target | Sync Status |",
        "| --- | ---: | --- | --- |",
    ]
    for row in registry_rows:
        ref = row["Name"].split("CAP-MOD-DRAFT-", 1)[1].split(" ", 1)[0]
        lines.append(
            f"| {row['Name']} | `{ref}` | {row['Feedback / Backpropagation Target']} | {row['Sync Status']} |"
        )

    lines.extend(
        [
            "",
            "## Package Outputs",
            "",
            "| File | Purpose |",
            "| --- | --- |",
            "| `mmd-006.registry-package.csv` | Five import/update-ready registry rows. |",
            "| `mmd-006.registry-field-map.csv` | Schema field mapping and value rules. |",
            "| `mmd-006.view-package.csv` | Two proposed registry views. |",
            "| `mmd-006.notion-mutation-package.csv` | Exact external mutations requiring explicit GO. |",
            "| `mmd-006.apply-gate.md` | Human-readable application gate and stop rules. |",
            "| `mmd-006.review-summary.json` | Machine-readable package summary. |",
            "",
            "## Application Boundary",
            "",
            f"Apply only after exact command: `{GO_PHRASE}`",
            "",
            "MMD-006 blocks:",
            "",
            "- deletion",
            "- schema change",
            "- raw private Notion IDs",
            "- canonical `TRG-*` assignment",
            "- expansion of `517`, `777` or `988-992`",
            "- publication or Zenodo action",
            "",
            "## Next",
            "",
            "Best next action: run `AUTO-001` after package preparation, then apply later only through `GO Notion MMD-006 anwenden` if the live registry should be changed.",
            "",
        ]
    )
    return "\n".join(lines)


def build_apply_gate(summary: dict[str, Any], registry_rows: list[dict[str, str]]) -> str:
    names = "\n".join(f"- {row['Name']}" for row in registry_rows)
    return "\n".join(
        [
            "# MMD-006 Apply Gate",
            "",
            "Status: prepared, not applied",
            "",
            "## Exact Authorization Required",
            "",
            f"`{GO_PHRASE}`",
            "",
            "Without that exact command, this package remains repo-local.",
            "",
            "## Planned Live Changes",
            "",
            names,
            "",
            "Additional planned live changes:",
            "",
            "- create registry view `CAP Module Drafts`",
            "- create registry view `CAP Module Sync Needed`",
            "- append a short MMD-006 checkpoint to the CAP page",
            "",
            "## Stop Rules",
            "",
            "Stop before mutation if:",
            "",
            "- registry schema differs from `notion-registry-field-map.md`",
            "- a row with the same exact `Name` already exists",
            "- Notion connector cannot verify the target registry",
            "- any target would require raw private IDs in the output",
            "- the action would assign canonical `TRG-*` IDs",
            "- the action would expand `517`, `777` or `988-992`",
            "",
            "## Verification After Apply",
            "",
            "- fetch or search the registry rows by exact `Name`",
            "- confirm five created rows",
            "- confirm both views exist",
            "- write `mmd-006.registry-updates.csv` with applied targets",
            "- rerun `python scripts/cap_control_checks.py --live-zenodo`",
            "",
        ]
    )


def build_batch_markdown(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# MMD-006 - CAP Module Registry Package",
            "",
            "Date: 2026-05-17",
            "",
            "Activation: `MMD-006 - CAP Module Registry Package GO`",
            "",
            "Mode: repo-local registry package preparation",
            "",
            "External mutation: none",
            "",
            "Notion AI credits used: 0",
            "",
            "## Purpose",
            "",
            "MMD-006 prepares the mutation-safe registry package for the five MMD-005 CAP module drafts.",
            "",
            "## Result",
            "",
            f"- Registry rows: {summary['registry_rows']}",
            f"- Field map rows: {summary['field_map_rows']}",
            f"- View package rows: {summary['view_package_rows']}",
            f"- Mutation package rows: {summary['mutation_package_rows']}",
            f"- Required apply command: `{GO_PHRASE}`",
            "",
            "## Boundary",
            "",
            "No live Notion mutation was performed. The package does not assign canonical `TRG-*` IDs and does not expose raw private IDs.",
            "",
        ]
    )


def build_causal_log(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "log_id": "CAP-LOG-2026-05-17-MMD-006",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "operator": "Codex",
        "mode": "STUDIO",
        "activation": "manual",
        "source_trace": [
            "docs/atlas/control-tower/mmd-005.cap-module-drafts.csv",
            "docs/atlas/control-tower/mmd-005.hash-ledger.csv",
            "docs/atlas/control-tower/notion-registry-field-map.md",
            "docs/atlas/control-tower/object-registry.schema.json",
        ],
        "observation": "MMD-005 produced five CAP module drafts ready for registry packaging.",
        "trigger_band": "401+",
        "trigger_ids": summary["visible_references"],
        "probabilistic_hypothesis": "The five draft modules can be represented in the CAP registry as internal candidate GitHub artifacts without asserting canon.",
        "probability_note": "High confidence for package preparation; no claim about live Notion state until apply verification.",
        "deterministic_boundary": "No external mutation without exact GO phrase; no canonical TRG assignment; no raw private IDs.",
        "selected_action": "Prepared registry rows, field map, view package, mutation package and apply gate for MMD-006.",
        "feedback_target": "registry",
        "backpropagation_result": "CAP module drafts now have a controlled path into the live registry if explicitly authorized.",
        "verification_state": "repo_checked",
        "external_mutation": False,
        "mutation_authorization": "",
    }


def main() -> int:
    module_rows = read_csv(MODULE_DRAFTS)
    hash_rows = read_csv(HASH_LEDGER)
    hash_material = load_json(CONTROL_DIR / HASH_MATERIAL)
    schema = load_json(SCHEMA_PATH)

    if len(module_rows) != 5:
        raise RuntimeError(f"Expected five MMD-005 module drafts, got {len(module_rows)}")
    if len(hash_rows) != 5:
        raise RuntimeError(f"Expected five MMD-005 hash rows, got {len(hash_rows)}")

    registry_rows = build_registry_rows(module_rows, hash_material)
    field_map_rows = build_field_map(schema)
    view_rows = build_view_package()
    mutation_rows = build_mutation_package(registry_rows, view_rows)

    write_csv(
        CONTROL_DIR / "mmd-006.registry-package.csv",
        registry_rows,
        [field["name"] for field in schema["fields"]],
    )
    write_csv(
        CONTROL_DIR / "mmd-006.registry-field-map.csv",
        field_map_rows,
        ["Registry Field", "Schema Type", "Required", "MMD-006 Source Rule", "Boundary"],
    )
    write_csv(
        CONTROL_DIR / "mmd-006.view-package.csv",
        view_rows,
        ["View Name", "Target", "View Type", "Filter", "Sort", "Requires GO", "Boundary"],
    )
    write_csv(
        CONTROL_DIR / "mmd-006.notion-mutation-package.csv",
        mutation_rows,
        [
            "Mutation ID",
            "Target",
            "Mutation Type",
            "Exact Intent",
            "Source File",
            "Row Count",
            "Requires GO",
            "External Mutation Risk",
            "Blocked Content",
            "Expected Result",
        ],
    )

    summary = {
        "review_id": "MMD-006",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "external_mutation": False,
        "notion_ai_credits_used": 0,
        "registry_rows": len(registry_rows),
        "field_map_rows": len(field_map_rows),
        "view_package_rows": len(view_rows),
        "mutation_package_rows": len(mutation_rows),
        "visible_references": [row["Visible Reference"] for row in module_rows],
        "required_apply_phrase": GO_PHRASE,
        "boundary": "Registry package only; no live Notion mutation and no canonical TRG assignment.",
    }

    (CONTROL_DIR / "mmd-006.review-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (CONTROL_DIR / "mmd-006.registry-package.md").write_text(
        build_markdown(summary, registry_rows),
        encoding="utf-8",
    )
    (CONTROL_DIR / "mmd-006.apply-gate.md").write_text(
        build_apply_gate(summary, registry_rows),
        encoding="utf-8",
    )
    (CONTROL_DIR / "batch-mmd-006.md").write_text(
        build_batch_markdown(summary),
        encoding="utf-8",
    )
    (CONTROL_DIR / "causal-log.mmd-006-registry-package-2026-05-17.json").write_text(
        json.dumps(build_causal_log(summary), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
