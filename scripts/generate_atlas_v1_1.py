from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATLAS_DIR = ROOT / "atlas"
BASE_MANIFEST = ATLAS_DIR / "atlas.manifest.v1.json"
OUT_MANIFEST = ATLAS_DIR / "atlas.manifest.v1.1.json"

SUPPLEMENT_REF = "trigger-complement-2026-03-30"

LEGACY_TRIGGER_CLUSTER_IDS = {
    "trigger_cluster_audit_suite_988_992",
    "trigger_cluster_codex_1_170",
    "trigger_cluster_core_session_516_544",
    "trigger_cluster_emergent_approx_500",
    "trigger_cluster_prism_551_600",
    "trigger_cluster_silvi_mode_174_210",
    "trigger_cluster_trigger_audit_675",
}


def append_unique(items: list[str], values: list[str]) -> None:
    for value in values:
        if value not in items:
            items.append(value)


def build_object(
    obj_id: str,
    kind: str,
    title: str,
    theme_ids: list[str],
    summary: str,
    *,
    status: str = "seeded",
    source_refs: list[str] | None = None,
    tags: list[str] | None = None,
    extras: dict | None = None,
) -> dict:
    obj = {
        "id": obj_id,
        "kind": kind,
        "title": title,
        "theme_ids": theme_ids,
        "summary": summary,
        "status": status,
        "source_refs": source_refs or [SUPPLEMENT_REF],
        "tags": tags or [],
    }
    if extras:
        obj.update(extras)
    return obj


def build_v1_1_manifest() -> dict:
    data = json.loads(BASE_MANIFEST.read_text(encoding="utf-8"))

    themes = data["themes"]
    objects = [obj for obj in data["objects"] if obj["id"] not in LEGACY_TRIGGER_CLUSTER_IDS]
    relations = [
        rel
        for rel in data["relations"]
        if rel["from"] not in LEGACY_TRIGGER_CLUSTER_IDS and rel["to"] not in LEGACY_TRIGGER_CLUSTER_IDS
    ]
    open_gaps = data["open_gaps"]

    if not any(theme["id"] == "theme_trigger_depth" for theme in themes):
        themes.append(
            {
                "id": "theme_trigger_depth",
                "title": "Trigger-Depth",
                "summary": "Mid-level trigger anchors, layer mappings and cluster-to-trigger membership added in Atlas v1.1.",
                "priority": "critical",
                "status": "seeded",
                "object_ids": [],
            }
        )

    object_by_id = {obj["id"]: obj for obj in objects}

    def touch_object(
        obj_id: str,
        *,
        theme_ids: list[str] | None = None,
        source_refs: list[str] | None = None,
        tags: list[str] | None = None,
        summary: str | None = None,
    ) -> None:
        obj = object_by_id[obj_id]
        if theme_ids:
            append_unique(obj["theme_ids"], theme_ids)
        if source_refs:
            append_unique(obj["source_refs"], source_refs)
        if tags:
            append_unique(obj["tags"], tags)
        if summary:
            obj["summary"] = summary

    trigger_depth_refs = [
        f"{SUPPLEMENT_REF}#trigger-truth-additions",
        f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11",
    ]
    touch_object(
        "page_trigger_architektur_520",
        theme_ids=["theme_trigger_depth"],
        source_refs=trigger_depth_refs,
        tags=["trigger-depth"],
        summary="Central steering logic for the trigger system. Atlas v1.1 expands it into core, flow, protection, audit and monitoring clusters.",
    )
    touch_object(
        "page_trigger_audit_675",
        theme_ids=["theme_trigger_depth"],
        source_refs=trigger_depth_refs,
        tags=["trigger-depth"],
        summary="Large trigger audit page. In Atlas v1.1 it anchors the IST layer inside the Trigger Truth Model and the documented 675-trigger audit space.",
    )
    touch_object(
        "page_trigger_zeichen_referenz",
        theme_ids=["theme_trigger_depth"],
        source_refs=[f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11"],
        tags=["trigger-depth"],
    )
    touch_object(
        "page_workspace_kohaerenz_protokoll",
        theme_ids=["theme_trigger_depth"],
        source_refs=[f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11"],
        tags=["trigger-depth"],
        summary="Trigger 999 coherence view with workspace sync protocol, dashboard state and truth-efficiency anchors.",
    )
    touch_object(
        "db_trigger_mapping",
        theme_ids=["theme_trigger_depth"],
        source_refs=[f"{SUPPLEMENT_REF}#trigger-truth-additions"],
        tags=["trigger-depth"],
        summary="Database linking trigger IDs, mapping surfaces, audit suites and the deployment-facing trigger registry.",
    )
    touch_object(
        "page_codex139_trigger_export_174_210",
        theme_ids=["theme_trigger_depth"],
        source_refs=[f"{SUPPLEMENT_REF}#known-single-triggers-for-mid-level-mapping"],
        tags=["trigger-depth"],
        summary="Trigger export focused on the Silvi-Modus Kognitiv anchor set used for Atlas v1.1 mid-level mapping.",
    )
    touch_object(
        "page_session_root",
        theme_ids=["theme_trigger_depth"],
        source_refs=[f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11"],
        tags=["trigger-depth"],
    )
    touch_object(
        "framework_prism",
        source_refs=[f"{SUPPLEMENT_REF}#atlas-v11-delta-notes"],
        tags=["formalization"],
        summary="Scientific-formal corpus spanning the PRISM parent, chapters, appendix and evidence matrix. Atlas v1.1 treats PRISM as a formalization layer over Codex and trigger logic.",
    )
    touch_object(
        "page_prism_parent",
        source_refs=[f"{SUPPLEMENT_REF}#atlas-v11-delta-notes"],
        summary="Parent page for the PRISM corpus spanning chapters, appendix and evidence matrix. Atlas v1.1 keeps it as the main entrypoint for formal trigger references.",
    )

    new_frameworks = [
        build_object(
            "framework_trigger_truth_model",
            "framework",
            "Trigger Truth Model",
            ["theme_trigger_system", "theme_trigger_depth", "theme_architecture_specs"],
            "Three-level trigger model joining the 1-1200 field, Trigger-Audit 675 as IST space and the deployment-facing trigger registry.",
            status="documented",
            source_refs=[f"{SUPPLEMENT_REF}#canonical-three-level-model"],
            tags=["framework", "trigger", "truth-model"],
            extras={"levels": ["field", "audit", "registry"]},
        ),
        build_object(
            "framework_trigger_architecture",
            "framework",
            "Trigger Architecture (5-Layer)",
            ["theme_trigger_system", "theme_trigger_depth", "theme_architecture_specs"],
            "Five-layer architecture spanning core, Schattenarchiv, Codex, meta-emergent and active-live trigger operation.",
            status="documented",
            source_refs=[f"{SUPPLEMENT_REF}#five-architecture-layers"],
            tags=["framework", "trigger", "architecture"],
            extras={"layer_count": 5},
        ),
        build_object(
            "framework_trigger_layer_1_system_core",
            "framework",
            "Trigger Layer 1: System-Core",
            ["theme_trigger_system", "theme_trigger_depth", "theme_architecture_specs"],
            "Core system triggers for session boot, preflight, sync and health logic.",
            status="documented",
            source_refs=[f"{SUPPLEMENT_REF}#five-architecture-layers"],
            tags=["framework", "trigger-layer", "core"],
            extras={"layer_index": 1},
        ),
        build_object(
            "framework_trigger_layer_2_schattenarchiv",
            "framework",
            "Trigger Layer 2: Schattenarchiv",
            ["theme_trigger_system", "theme_trigger_depth", "theme_shadow_archive_creative"],
            "Consent-sensitive and protective trigger layer for Schattenarchiv-linked operation.",
            status="documented",
            source_refs=[f"{SUPPLEMENT_REF}#five-architecture-layers"],
            tags=["framework", "trigger-layer", "schattenarchiv"],
            extras={"layer_index": 2},
        ),
        build_object(
            "framework_trigger_layer_3_codex",
            "framework",
            "Trigger Layer 3: Codex",
            ["theme_trigger_system", "theme_trigger_depth", "theme_code_ethics"],
            "Codex-facing trigger layer for modes, rituals and explicit instruction anchors.",
            status="documented",
            source_refs=[f"{SUPPLEMENT_REF}#five-architecture-layers"],
            tags=["framework", "trigger-layer", "codex"],
            extras={"layer_index": 3},
        ),
        build_object(
            "framework_trigger_layer_4_meta_emergent",
            "framework",
            "Trigger Layer 4: Meta-Emergent",
            ["theme_trigger_system", "theme_trigger_depth"],
            "Meta, creative and emergent trigger layer for reflective and not-yet-fully-canonical anchors.",
            status="documented",
            source_refs=[f"{SUPPLEMENT_REF}#five-architecture-layers"],
            tags=["framework", "trigger-layer", "emergent"],
            extras={"layer_index": 4},
        ),
        build_object(
            "framework_trigger_layer_5_active_live",
            "framework",
            "Trigger Layer 5: Active-Live",
            ["theme_trigger_system", "theme_trigger_depth", "theme_hubs_navigation"],
            "Live operational layer for dashboards, audits, Pegasus and active monitoring commands.",
            status="documented",
            source_refs=[f"{SUPPLEMENT_REF}#five-architecture-layers"],
            tags=["framework", "trigger-layer", "live"],
            extras={"layer_index": 5},
        ),
    ]

    new_clusters = [
        build_object(
            "trigger_cluster_core_system_520_530",
            "trigger_cluster",
            "Core System Trigger Cluster 520-530",
            ["theme_trigger_system", "theme_trigger_depth", "theme_architecture_specs"],
            "SessionStart, preflight, sync and health-oriented core system band.",
            status="active",
            source_refs=[f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11"],
            tags=["trigger-cluster", "core-system"],
            extras={"members": ["520-530"]},
        ),
        build_object(
            "trigger_cluster_silvi_modus_kognitiv",
            "trigger_cluster",
            "Silvi-Modus Kognitiv Trigger Cluster",
            ["theme_trigger_system", "theme_trigger_depth", "theme_code_ethics"],
            "Cognitive focus, impulse-stop, meta-focus and regeneration anchors centered on 174 and 205-210.",
            status="active",
            source_refs=[f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11"],
            tags=["trigger-cluster", "silvi-mode"],
            extras={"members": ["174", "205-210"]},
        ),
        build_object(
            "trigger_cluster_metarotik_300_325_601",
            "trigger_cluster",
            "Metarotik Trigger Cluster 300-325 / 601",
            ["theme_trigger_system", "theme_trigger_depth", "theme_shadow_archive_creative"],
            "Intimate or flutung-related trigger band across 300-325 plus 601.",
            status="active",
            source_refs=[f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11"],
            tags=["trigger-cluster", "metarotik"],
            extras={"members": ["300-325", "601"]},
        ),
        build_object(
            "trigger_cluster_creative_flow_516_517",
            "trigger_cluster",
            "Creative Flow Trigger Cluster 516-517",
            ["theme_trigger_system", "theme_trigger_depth", "theme_shadow_archive_creative"],
            "Inspiration and AutoFlow anchor pair.",
            status="active",
            source_refs=[f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11"],
            tags=["trigger-cluster", "creative-flow"],
            extras={"members": ["516", "517"]},
        ),
        build_object(
            "trigger_cluster_meta_reflexion_540_544",
            "trigger_cluster",
            "Meta-Reflexion Trigger Cluster 540 / 544",
            ["theme_trigger_system", "theme_trigger_depth", "theme_cic_theory"],
            "Validation, decision-point and momentum anchors for reflective execution.",
            status="active",
            source_refs=[f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11"],
            tags=["trigger-cluster", "meta-reflexion"],
            extras={"members": ["540", "544"]},
        ),
        build_object(
            "trigger_cluster_protection_layer_182_521_777",
            "trigger_cluster",
            "Protection Layer Trigger Cluster 182 / 521 / 777",
            ["theme_trigger_system", "theme_trigger_depth", "theme_security_blockchain_infra"],
            "Airbag, preflight-protective and Schattenarchiv-linked protection anchors.",
            status="active",
            source_refs=[f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11"],
            tags=["trigger-cluster", "protection"],
            extras={"members": ["182", "521", "777"]},
        ),
        build_object(
            "trigger_cluster_sicherheitsritual_700",
            "trigger_cluster",
            "Sicherheitsritual Trigger Cluster 700",
            ["theme_trigger_system", "theme_trigger_depth", "theme_code_ethics"],
            "Codex 700 ritual anchor used as an explicit safety or readiness checkpoint.",
            status="active",
            source_refs=[f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11"],
            tags=["trigger-cluster", "ritual"],
            extras={"members": ["700"]},
        ),
        build_object(
            "trigger_cluster_schattenarchiv_777",
            "trigger_cluster",
            "Schattenarchiv Trigger Cluster 777",
            ["theme_trigger_system", "theme_trigger_depth", "theme_shadow_archive_creative"],
            "Consent-gated sensitive-memory cluster for Schattenarchiv operation.",
            status="active",
            source_refs=[f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11"],
            tags=["trigger-cluster", "schattenarchiv"],
            extras={"members": ["777"]},
        ),
        build_object(
            "trigger_cluster_truth_efficiency_888_999",
            "trigger_cluster",
            "Truth and Efficiency Trigger Cluster 888 / 999",
            ["theme_trigger_system", "theme_trigger_depth", "theme_workspace_infrastructure"],
            "Control-comparison and workspace-coherence anchors for truth-efficiency checks.",
            status="active",
            source_refs=[f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11"],
            tags=["trigger-cluster", "truth-efficiency"],
            extras={"members": ["888", "999"]},
        ),
        build_object(
            "trigger_cluster_audit_security_988_992",
            "trigger_cluster",
            "Audit and Security Trigger Cluster 988-992",
            ["theme_trigger_system", "theme_trigger_depth", "theme_security_blockchain_infra"],
            "Snapshot lockpoint, token sync, integrity and echo-sync audit suite.",
            status="active",
            source_refs=[f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11"],
            tags=["trigger-cluster", "audit-security"],
            extras={"members": ["988-992"]},
        ),
        build_object(
            "trigger_cluster_pegasus_1001",
            "trigger_cluster",
            "Pegasus Trigger Cluster 1001",
            ["theme_trigger_system", "theme_trigger_depth", "theme_hubs_navigation"],
            "Pegasus-mode cluster for output-log analysis and vision-oriented monitoring.",
            status="active",
            source_refs=[f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11"],
            tags=["trigger-cluster", "pegasus"],
            extras={"members": ["1001"]},
        ),
        build_object(
            "trigger_cluster_dashboard_monitoring",
            "trigger_cluster",
            "Dashboard and Monitoring Trigger Cluster",
            ["theme_trigger_system", "theme_trigger_depth", "theme_hubs_navigation"],
            "Slash-command cluster for dashboard, health, metrics and snapshot surfaces.",
            status="active",
            source_refs=[f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11"],
            tags=["trigger-cluster", "monitoring"],
            extras={"members": ["/dashboard", "/health", "/metrics", "/snapshot"]},
        ),
        build_object(
            "trigger_cluster_maxsync_token",
            "trigger_cluster",
            "MAXSync and Token Trigger Cluster",
            ["theme_trigger_system", "theme_trigger_depth", "theme_token_blockchain"],
            "Partial token-integration cluster for sync-start and trigger-zip matching commands.",
            status="partial",
            source_refs=[f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11"],
            tags=["trigger-cluster", "token-sync"],
            extras={"members": ["/start_sync_max", "/sync_trigger_zip_match"]},
        ),
        build_object(
            "trigger_cluster_modi_system",
            "trigger_cluster",
            "Modi-System Trigger Cluster",
            ["theme_trigger_system", "theme_trigger_depth", "theme_code_ethics"],
            "Behavioral mode cluster for /fff, /seepferdli, /fix, /gaertner and /deep.",
            status="active",
            source_refs=[f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11"],
            tags=["trigger-cluster", "modes"],
            extras={"members": ["/fff", "/seepferdli", "/fix", "/gaertner", "/deep"]},
        ),
        build_object(
            "trigger_cluster_error_handling_900_950",
            "trigger_cluster",
            "Error-Handling Trigger Cluster 900-950",
            ["theme_trigger_system", "theme_trigger_depth", "theme_workspace_infrastructure"],
            "Planned fallback and error-handling band proposed for Atlas v1.1 without full single-trigger expansion yet.",
            status="planned",
            source_refs=[f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11"],
            tags=["trigger-cluster", "error-handling"],
            extras={"members": ["900-950"]},
        ),
    ]

    trigger_specs = [
        ("trigger_174", 174, "Trigger 174", ["theme_trigger_system", "theme_trigger_depth", "theme_code_ethics"], "Cognitive-focus anchor in the Silvi-Modus Kognitiv band.", "documented", ["trigger", "silvi-mode"], ["trigger_cluster_silvi_modus_kognitiv"], "framework_trigger_layer_3_codex"),
        ("trigger_182", 182, "Trigger 182", ["theme_trigger_system", "theme_trigger_depth", "theme_security_blockchain_infra"], "Airbag or emergency-stop anchor in the protection layer.", "documented", ["trigger", "protection"], ["trigger_cluster_protection_layer_182_521_777"], "framework_trigger_layer_2_schattenarchiv"),
        ("trigger_205", 205, "Trigger 205", ["theme_trigger_system", "theme_trigger_depth", "theme_code_ethics"], "Named trigger anchor in the Silvi-Modus Kognitiv band; the current seed does not pin a stable local label beyond the cluster role.", "identified", ["trigger", "silvi-mode"], ["trigger_cluster_silvi_modus_kognitiv"], "framework_trigger_layer_3_codex"),
        ("trigger_206", 206, "Trigger 206", ["theme_trigger_system", "theme_trigger_depth", "theme_code_ethics"], "Named trigger anchor in the Silvi-Modus Kognitiv band; the current seed does not pin a stable local label beyond the cluster role.", "identified", ["trigger", "silvi-mode"], ["trigger_cluster_silvi_modus_kognitiv"], "framework_trigger_layer_3_codex"),
        ("trigger_207", 207, "Trigger 207", ["theme_trigger_system", "theme_trigger_depth", "theme_code_ethics"], "Named trigger anchor in the Silvi-Modus Kognitiv band; the current seed does not pin a stable local label beyond the cluster role.", "identified", ["trigger", "silvi-mode"], ["trigger_cluster_silvi_modus_kognitiv"], "framework_trigger_layer_3_codex"),
        ("trigger_208", 208, "Trigger 208", ["theme_trigger_system", "theme_trigger_depth", "theme_code_ethics"], "Named trigger anchor in the Silvi-Modus Kognitiv band; the current seed does not pin a stable local label beyond the cluster role.", "identified", ["trigger", "silvi-mode"], ["trigger_cluster_silvi_modus_kognitiv"], "framework_trigger_layer_3_codex"),
        ("trigger_209", 209, "Trigger 209", ["theme_trigger_system", "theme_trigger_depth", "theme_code_ethics"], "Named trigger anchor in the Silvi-Modus Kognitiv band; the current seed does not pin a stable local label beyond the cluster role.", "identified", ["trigger", "silvi-mode"], ["trigger_cluster_silvi_modus_kognitiv"], "framework_trigger_layer_3_codex"),
        ("trigger_210", 210, "Trigger 210", ["theme_trigger_system", "theme_trigger_depth", "theme_code_ethics"], "Named trigger anchor in the Silvi-Modus Kognitiv band; the current seed does not pin a stable local label beyond the cluster role.", "identified", ["trigger", "silvi-mode"], ["trigger_cluster_silvi_modus_kognitiv"], "framework_trigger_layer_3_codex"),
        ("trigger_300", 300, "Trigger 300", ["theme_trigger_system", "theme_trigger_depth", "theme_shadow_archive_creative"], "Edge anchor for the Metarotik trigger band; the exact local label remains unresolved in the current seed.", "identified", ["trigger", "metarotik"], ["trigger_cluster_metarotik_300_325_601"], "framework_trigger_layer_4_meta_emergent"),
        ("trigger_325", 325, "Trigger 325", ["theme_trigger_system", "theme_trigger_depth", "theme_shadow_archive_creative"], "Edge anchor for the Metarotik trigger band; the exact local label remains unresolved in the current seed.", "identified", ["trigger", "metarotik"], ["trigger_cluster_metarotik_300_325_601"], "framework_trigger_layer_4_meta_emergent"),
        ("trigger_516", 516, "Trigger 516", ["theme_trigger_system", "theme_trigger_depth", "theme_shadow_archive_creative"], "Inspiration anchor in the Creative Flow band.", "documented", ["trigger", "creative-flow"], ["trigger_cluster_creative_flow_516_517"], "framework_trigger_layer_4_meta_emergent"),
        ("trigger_517", 517, "Trigger 517", ["theme_trigger_system", "theme_trigger_depth", "theme_shadow_archive_creative"], "AutoFlow anchor in the Creative Flow band.", "documented", ["trigger", "creative-flow"], ["trigger_cluster_creative_flow_516_517"], "framework_trigger_layer_4_meta_emergent"),
        ("trigger_520", 520, "Trigger 520", ["theme_trigger_system", "theme_trigger_depth", "theme_architecture_specs"], "SessionStart anchor in the core system band.", "documented", ["trigger", "core-system"], ["trigger_cluster_core_system_520_530"], "framework_trigger_layer_1_system_core"),
        ("trigger_521", 521, "Trigger 521", ["theme_trigger_system", "theme_trigger_depth", "theme_security_blockchain_infra"], "Preflight anchor that appears in both the core system and the protection layer.", "documented", ["trigger", "preflight"], ["trigger_cluster_core_system_520_530", "trigger_cluster_protection_layer_182_521_777"], "framework_trigger_layer_2_schattenarchiv"),
        ("trigger_522", 522, "Trigger 522", ["theme_trigger_system", "theme_trigger_depth", "theme_architecture_specs"], "Named anchor inside the 520-530 core system band; the exact local label is not fixed in the current seed.", "identified", ["trigger", "core-system"], ["trigger_cluster_core_system_520_530"], "framework_trigger_layer_1_system_core"),
        ("trigger_523", 523, "Trigger 523", ["theme_trigger_system", "theme_trigger_depth", "theme_architecture_specs"], "Named anchor inside the 520-530 core system band; the exact local label is not fixed in the current seed.", "identified", ["trigger", "core-system"], ["trigger_cluster_core_system_520_530"], "framework_trigger_layer_1_system_core"),
        ("trigger_540", 540, "Trigger 540", ["theme_trigger_system", "theme_trigger_depth", "theme_cic_theory"], "Validation and momentum anchor in the Meta-Reflexion band.", "documented", ["trigger", "meta-reflexion"], ["trigger_cluster_meta_reflexion_540_544"], "framework_trigger_layer_4_meta_emergent"),
        ("trigger_544", 544, "Trigger 544", ["theme_trigger_system", "theme_trigger_depth", "theme_cic_theory"], "Synchronization and decision-point anchor in the Meta-Reflexion band.", "documented", ["trigger", "meta-reflexion"], ["trigger_cluster_meta_reflexion_540_544"], "framework_trigger_layer_4_meta_emergent"),
        ("trigger_601", 601, "Trigger 601", ["theme_trigger_system", "theme_trigger_depth", "theme_shadow_archive_creative"], "Somatic or flutung-adjacent anchor grouped with the Metarotik band.", "documented", ["trigger", "metarotik"], ["trigger_cluster_metarotik_300_325_601"], "framework_trigger_layer_4_meta_emergent"),
        ("trigger_700", 700, "Trigger 700", ["theme_trigger_system", "theme_trigger_depth", "theme_code_ethics"], "Codex 700 ritual anchor.", "documented", ["trigger", "ritual"], ["trigger_cluster_sicherheitsritual_700"], "framework_trigger_layer_3_codex"),
        ("trigger_777", 777, "Trigger 777", ["theme_trigger_system", "theme_trigger_depth", "theme_shadow_archive_creative"], "Schattenarchiv anchor that also functions as a protection-layer trigger.", "documented", ["trigger", "schattenarchiv"], ["trigger_cluster_protection_layer_182_521_777", "trigger_cluster_schattenarchiv_777"], "framework_trigger_layer_2_schattenarchiv"),
        ("trigger_888", 888, "Trigger 888", ["theme_trigger_system", "theme_trigger_depth", "theme_workspace_infrastructure"], "Truth-and-efficiency audit anchor.", "documented", ["trigger", "truth-efficiency"], ["trigger_cluster_truth_efficiency_888_999"], "framework_trigger_layer_5_active_live"),
        ("trigger_988", 988, "Trigger 988", ["theme_trigger_system", "theme_trigger_depth", "theme_security_blockchain_infra"], "Snapshot lockpoint anchor in the audit-security suite.", "documented", ["trigger", "audit-security"], ["trigger_cluster_audit_security_988_992"], "framework_trigger_layer_5_active_live"),
        ("trigger_989", 989, "Trigger 989", ["theme_trigger_system", "theme_trigger_depth", "theme_security_blockchain_infra"], "Token-sync anchor in the audit-security suite.", "documented", ["trigger", "audit-security"], ["trigger_cluster_audit_security_988_992"], "framework_trigger_layer_5_active_live"),
        ("trigger_990", 990, "Trigger 990", ["theme_trigger_system", "theme_trigger_depth", "theme_security_blockchain_infra"], "Integrity anchor in the audit-security suite.", "documented", ["trigger", "audit-security"], ["trigger_cluster_audit_security_988_992"], "framework_trigger_layer_5_active_live"),
        ("trigger_991", 991, "Trigger 991", ["theme_trigger_system", "theme_trigger_depth", "theme_security_blockchain_infra"], "Echo-sync anchor in the audit-security suite.", "documented", ["trigger", "audit-security"], ["trigger_cluster_audit_security_988_992"], "framework_trigger_layer_5_active_live"),
        ("trigger_992", 992, "Trigger 992", ["theme_trigger_system", "theme_trigger_depth", "theme_security_blockchain_infra"], "Named anchor in the audit-security suite; the current seed confirms the suite membership but not a stable local label.", "identified", ["trigger", "audit-security"], ["trigger_cluster_audit_security_988_992"], "framework_trigger_layer_5_active_live"),
        ("trigger_999", 999, "Trigger 999", ["theme_trigger_system", "theme_trigger_depth", "theme_workspace_infrastructure"], "Workspace-coherence anchor in the truth-efficiency band.", "documented", ["trigger", "truth-efficiency"], ["trigger_cluster_truth_efficiency_888_999"], "framework_trigger_layer_5_active_live"),
        ("trigger_1001", 1001, "Trigger 1001", ["theme_trigger_system", "theme_trigger_depth", "theme_hubs_navigation"], "Pegasus-mode anchor for output-log analysis.", "documented", ["trigger", "pegasus"], ["trigger_cluster_pegasus_1001"], "framework_trigger_layer_5_active_live"),
    ]

    new_triggers = []
    for obj_id, trigger_id, title, theme_ids, summary, status, tags, cluster_ids, layer_id in trigger_specs:
        new_triggers.append(
            build_object(
                obj_id,
                "trigger",
                title,
                theme_ids,
                summary,
                status=status,
                source_refs=[f"{SUPPLEMENT_REF}#known-single-triggers-for-mid-level-mapping"],
                tags=tags,
                extras={"trigger_id": trigger_id, "cluster_ids": cluster_ids, "layer_id": layer_id},
            )
        )

    objects.extend(new_frameworks)
    objects.extend(new_clusters)
    objects.extend(new_triggers)

    new_relations = [
        {"from": "framework_trigger_architecture", "to": "framework_trigger_layer_1_system_core", "type": "contains", "note": "The five-layer trigger architecture contains the system-core layer."},
        {"from": "framework_trigger_architecture", "to": "framework_trigger_layer_2_schattenarchiv", "type": "contains", "note": "The five-layer trigger architecture contains the Schattenarchiv layer."},
        {"from": "framework_trigger_architecture", "to": "framework_trigger_layer_3_codex", "type": "contains", "note": "The five-layer trigger architecture contains the Codex layer."},
        {"from": "framework_trigger_architecture", "to": "framework_trigger_layer_4_meta_emergent", "type": "contains", "note": "The five-layer trigger architecture contains the meta-emergent layer."},
        {"from": "framework_trigger_architecture", "to": "framework_trigger_layer_5_active_live", "type": "contains", "note": "The five-layer trigger architecture contains the active-live layer."},
        {"from": "framework_trigger_truth_model", "to": "page_trigger_audit_675", "type": "formalizes", "note": "Trigger-Audit 675 acts as the IST space inside the Trigger Truth Model."},
        {"from": "framework_trigger_truth_model", "to": "db_trigger_mapping", "type": "depends_on", "note": "The deployment-facing registry layer is represented by trigger mapping data."},
        {"from": "framework_trigger_truth_model", "to": "page_trigger_architektur_520", "type": "references", "note": "The Trigger Truth Model reads the architecture page as a control surface for documented trigger logic."},
        {"from": "page_trigger_audit_675", "to": "framework_trigger_truth_model", "type": "contains", "note": "Trigger-Audit 675 is the clearest page-level source for the three-level trigger model."},
        {"from": "page_trigger_architektur_520", "to": "framework_trigger_architecture", "type": "contains", "note": "Trigger-Architektur 520 is the main page-level anchor for the five-layer trigger architecture."},
        {"from": "page_trigger_architektur_520", "to": "trigger_cluster_core_system_520_530", "type": "contains", "note": "The architecture page anchors the core-system cluster."},
        {"from": "page_trigger_architektur_520", "to": "trigger_cluster_creative_flow_516_517", "type": "references", "note": "The architecture page references the creative-flow band around 516 and 517."},
        {"from": "page_trigger_architektur_520", "to": "trigger_cluster_meta_reflexion_540_544", "type": "references", "note": "The architecture page references validation, momentum and sync anchors."},
        {"from": "page_trigger_architektur_520", "to": "trigger_cluster_protection_layer_182_521_777", "type": "references", "note": "The architecture page names protection and Schattenarchiv hooks."},
        {"from": "page_trigger_architektur_520", "to": "trigger_cluster_audit_security_988_992", "type": "references", "note": "The architecture page references the audit-security suite."},
        {"from": "page_trigger_architektur_520", "to": "trigger_cluster_truth_efficiency_888_999", "type": "references", "note": "The architecture page connects core session logic to truth-efficiency checks."},
        {"from": "page_workspace_kohaerenz_protokoll", "to": "trigger_cluster_truth_efficiency_888_999", "type": "contains", "note": "Workspace coherence protocol is the clearest page anchor for triggers 888 and 999."},
        {"from": "page_workspace_kohaerenz_protokoll", "to": "trigger_cluster_dashboard_monitoring", "type": "references", "note": "The workspace protocol names dashboard and monitoring surfaces."},
        {"from": "page_system_status_dashboard", "to": "trigger_cluster_dashboard_monitoring", "type": "references", "note": "System Status Dashboard is a live surface for the monitoring command cluster."},
        {"from": "page_master_dashboard", "to": "trigger_cluster_dashboard_monitoring", "type": "references", "note": "Master Dashboard backs the dashboard and monitoring cluster."},
        {"from": "page_session_root", "to": "trigger_cluster_core_system_520_530", "type": "references", "note": "SESSION_ROOT aligns with core system boot and preflight logic."},
        {"from": "page_session_root", "to": "trigger_cluster_creative_flow_516_517", "type": "references", "note": "SESSION_ROOT names inspiration and AutoFlow as active session mechanics."},
        {"from": "page_session_root", "to": "trigger_cluster_meta_reflexion_540_544", "type": "references", "note": "SESSION_ROOT touches momentum and synchronization anchors."},
        {"from": "page_session_root", "to": "trigger_cluster_protection_layer_182_521_777", "type": "references", "note": "SESSION_ROOT links to protective and Schattenarchiv-aware operation."},
        {"from": "page_codex139_trigger_export_174_210", "to": "trigger_cluster_silvi_modus_kognitiv", "type": "contains", "note": "Codex139+ is the page-level seed for the 174 and 205-210 cognitive trigger band."},
        {"from": "page_schattenarchiv_hub", "to": "trigger_cluster_schattenarchiv_777", "type": "contains", "note": "Schattenarchiv Hub is the clearest page-level source for the 777 cluster."},
        {"from": "page_token_blockchain_system_index", "to": "trigger_cluster_maxsync_token", "type": "references", "note": "Token index names the MAXSync and trigger-zip match integration surface."},
        {"from": "page_prism_parent", "to": "framework_prism", "type": "contains", "note": "PRISM parent remains the top-level page for the PRISM framework."},
        {"from": "framework_prism", "to": "page_codex170_plus_final", "type": "formalizes", "note": "The trigger complement positions PRISM as a formalization layer over Codex logic."},
        {"from": "framework_prism", "to": "trigger_540", "type": "references", "note": "PRISM is treated as part of the formalization path for reflective trigger logic."},
        {"from": "framework_prism", "to": "trigger_544", "type": "references", "note": "PRISM is treated as part of the formalization path for synchronization-oriented trigger logic."},
        {"from": "framework_prism", "to": "trigger_888", "type": "references", "note": "PRISM is treated as part of the formalization path for truth-efficiency logic."},
        {"from": "framework_prism", "to": "trigger_700", "type": "references", "note": "PRISM is aligned with codified safety-ritual logic in the Atlas v1.1 complement."},
        {"from": "page_codex170_plus_final", "to": "framework_trigger_layer_3_codex", "type": "references", "note": "Codex170 is best modeled as a Codex-layer anchor inside the trigger architecture."},
        {"from": "page_mermaid_manifesto_public", "to": "framework_trigger_architecture", "type": "references", "note": "The manifesto frames trigger entities as graph nodes within a living architecture."},
        {"from": "trigger_cluster_audit_security_988_992", "to": "db_zip_index_master", "type": "depends_on", "note": "Lockpoint and integrity concepts rely on bundle index data."},
        {"from": "trigger_cluster_audit_security_988_992", "to": "db_trigger_mapping", "type": "depends_on", "note": "Audit-security triggers depend on trigger mapping data."},
    ]

    layer_map = {
        "trigger_cluster_core_system_520_530": "framework_trigger_layer_1_system_core",
        "trigger_cluster_silvi_modus_kognitiv": "framework_trigger_layer_3_codex",
        "trigger_cluster_metarotik_300_325_601": "framework_trigger_layer_4_meta_emergent",
        "trigger_cluster_creative_flow_516_517": "framework_trigger_layer_4_meta_emergent",
        "trigger_cluster_meta_reflexion_540_544": "framework_trigger_layer_4_meta_emergent",
        "trigger_cluster_protection_layer_182_521_777": "framework_trigger_layer_2_schattenarchiv",
        "trigger_cluster_sicherheitsritual_700": "framework_trigger_layer_3_codex",
        "trigger_cluster_schattenarchiv_777": "framework_trigger_layer_2_schattenarchiv",
        "trigger_cluster_truth_efficiency_888_999": "framework_trigger_layer_5_active_live",
        "trigger_cluster_audit_security_988_992": "framework_trigger_layer_5_active_live",
        "trigger_cluster_pegasus_1001": "framework_trigger_layer_5_active_live",
        "trigger_cluster_dashboard_monitoring": "framework_trigger_layer_5_active_live",
        "trigger_cluster_maxsync_token": "framework_trigger_layer_5_active_live",
        "trigger_cluster_modi_system": "framework_trigger_layer_3_codex",
        "trigger_cluster_error_handling_900_950": "framework_trigger_layer_4_meta_emergent",
    }
    for cluster_id, layer_id in layer_map.items():
        new_relations.append(
            {
                "from": cluster_id,
                "to": layer_id,
                "type": "belongs_to_layer",
                "note": "Atlas v1.1 maps this trigger cluster into the five-layer trigger architecture.",
            }
        )

    for obj_id, _, _, _, _, _, _, cluster_ids, layer_id in trigger_specs:
        new_relations.append(
            {
                "from": obj_id,
                "to": layer_id,
                "type": "belongs_to_layer",
                "note": "Atlas v1.1 maps this trigger anchor to its primary architecture layer.",
            }
        )
        for cluster_id in cluster_ids:
            new_relations.append(
                {
                    "from": cluster_id,
                    "to": obj_id,
                    "type": "has_members",
                    "note": "Atlas v1.1 expands trigger-depth by linking canonical clusters to named trigger anchors.",
                }
            )

    relations.extend(new_relations)

    for gap in open_gaps:
        if gap["id"] == "gap_trigger_range_171_505":
            gap["description"] = (
                "Atlas v1.1 now maps selected anchors such as 174, 182, 205-210 and 300/325, "
                "but the interior of the 171-505 range still is not fully enumerated from source material."
            )
            append_unique(gap["source_refs"], [f"{SUPPLEMENT_REF}#known-single-triggers-for-mid-level-mapping"])

    open_gaps.append(
        {
            "id": "gap_trigger_depth_partial_ranges_v1_1",
            "title": "Trigger-depth still partial for interior ranges",
            "description": (
                "Atlas v1.1 adds named trigger anchors and 15 canonical clusters, but ranges such as 300-325, "
                "520-530 and the proposed 900-950 band are still only partially expanded at single-trigger level."
            ),
            "status": "open",
            "source_refs": [
                f"{SUPPLEMENT_REF}#trigger-clusters-for-atlas-v11",
                f"{SUPPLEMENT_REF}#known-single-triggers-for-mid-level-mapping",
            ],
        }
    )

    theme_by_id = {theme["id"]: theme for theme in themes}
    for theme in themes:
        theme["object_ids"] = []
    for obj in objects:
        for theme_id in obj["theme_ids"]:
            theme_by_id[theme_id]["object_ids"].append(obj["id"])
    for theme in themes:
        theme["object_ids"] = sorted(set(theme["object_ids"]))

    themes.sort(key=lambda item: item["id"])
    objects.sort(key=lambda item: (item["kind"], item["title"].lower(), item["id"]))
    relations.sort(key=lambda item: (item["from"], item["type"], item["to"]))
    open_gaps.sort(key=lambda item: item["id"])
    kind_counts = dict(sorted(Counter(obj["kind"] for obj in objects).items()))

    data["workspace"]["atlas_id"] = "terranova-atlas-v1.1"
    data["source"] = {
        "id": "atlas-seed-2026-03-27-plus-trigger-complement-2026-03-30",
        "type": "manual atlas seed plus Notion trigger complement",
        "captured_at": "2026-03-30",
        "ingested_at": "2026-03-30",
        "supplements": ["workspace-export-2026-03-27", SUPPLEMENT_REF],
        "notes": [
            "Atlas v1.1 keeps the original workspace export seed and adds the user-provided Trigger Truth complement from 2026-03-30.",
            "The trigger model now includes canonical 15-cluster coverage, trigger-layer mapping and selected single-trigger anchors.",
            "The repo still does not perform a live Notion crawl; this remains a curated manual seed.",
        ],
    }
    data["stats"] = {
        "theme_count": len(themes),
        "object_count": len(objects),
        "relation_count": len(relations),
        "open_gap_count": len(open_gaps),
        "objects_by_kind": kind_counts,
        "estimates": {
            "workspace_main_pages": 85,
            "workspace_pages_via_api": 323,
            "workspace_total_page_range": "400-600",
            "workspace_subpages_and_crossrefs": "500+",
            "active_databases_estimate": "15+",
            "files_estimate": "1750+",
            "ipfs_cids": 39,
            "documented_triggers": 675,
            "defined_triggers_estimate": "1200+",
            "canonical_trigger_clusters_v1_1": 15,
            "single_trigger_anchors_v1_1": len(new_triggers),
        },
        "coverage": {
            "atlas_scope": "themes-plus-main-objects-plus-trigger-depth",
            "source_mode": "manual-seed-from-workspace-export-plus-trigger-complement",
            "live_notion_scan_attached": False,
            "full_subpage_expansion": False,
            "production_sync_unchanged": True,
        },
    }
    data["themes"] = themes
    data["objects"] = objects
    data["relations"] = relations
    data["open_gaps"] = open_gaps
    return data


def write_manifest() -> None:
    manifest = build_v1_1_manifest()
    OUT_MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    write_manifest()
