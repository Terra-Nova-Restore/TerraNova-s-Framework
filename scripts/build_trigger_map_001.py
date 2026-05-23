"""Build the TRIGGER-MAP-001 source-backed trigger map artifacts.

This script intentionally uses only public-safe source handles and local paths.
Notion page IDs and raw private dialogue are not emitted.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "atlas" / "control-tower"
TODAY = "2026-05-23"
CREATED_AT = "2026-05-23T12:50:14+02:00"
BATCH = "TRIGGER-MAP-001"


SOURCES = [
    {
        "source_handle": "silvi_directive_2026-05-23",
        "source_tier": "T6_OWNER_DIRECTIVE",
        "system": "Session directive",
        "source_title": "Silvi decision for Trigger 171-173",
        "source_location": "Current Codex session 2026-05-23",
        "source_status": "owner_decision",
        "evidence_scope": "171, 172 and 173 are reserved, unausformulierte slots for later module fill.",
        "mutation_status": "local_directive_applied",
        "notes": "Not a source gap; consciously reserved module room.",
    },
    {
        "source_handle": "N-CODEX-MASTER",
        "source_tier": "T1_NOTION_MASTER",
        "system": "Notion",
        "source_title": "Terra Nova Codex - Handbuch",
        "source_location": "Notion workspace page; URL withheld in public trace",
        "source_status": "normative_master",
        "evidence_scope": "Codex governance, Notion-over-GitHub precedence, Codex139+ reference pointer",
        "mutation_status": f"read_only_fetch_{TODAY}",
        "notes": "Exports and mirrors are references; Notion Codex wins if source layers conflict.",
    },
    {
        "source_handle": "N-TTRUTH-001",
        "source_tier": "T1_NOTION_CANON",
        "system": "Notion",
        "source_title": "Trigger Truth - 675 Audit / 1200 Field / Module Registry",
        "source_location": "Notion workspace page; URL withheld in public trace",
        "source_status": "canon_rule_source",
        "evidence_scope": "Trigger-ID uniqueness rule, three-layer truth model, defined/active/stable semantics",
        "mutation_status": f"read_only_fetch_{TODAY}",
        "notes": "Canonical key is Trigger-ID + layer/instance + mode/promille + context.",
    },
    {
        "source_handle": "N-CODEX139-174210",
        "source_tier": "T2_NOTION_REFERENCE",
        "system": "Notion",
        "source_title": "Codex139+ TriggerExport 174-210 SilviModus",
        "source_location": "Notion workspace page; URL withheld in public trace",
        "source_status": "reference_export_not_master",
        "evidence_scope": "Full table for Trigger 174-210, Codex139+ integration notes, TNPX-01 relevance",
        "mutation_status": f"read_only_fetch_{TODAY}",
        "notes": "Page states all 37 trigger modules are defined, but integration with Triggerliste_600 remains pending.",
    },
    {
        "source_handle": "N-ACTIVE-SYSTEM-TABLE",
        "source_tier": "T2_NOTION_OPERATIONAL",
        "system": "Notion",
        "source_title": "Trigger - Systemtabelle (aktiv)",
        "source_location": "Notion workspace page; URL withheld in public trace",
        "source_status": "active_operational_table",
        "evidence_scope": "Active entry points for 516/517/520/521/540/544/777/988-992/999 and emergency chain",
        "mutation_status": f"read_only_fetch_{TODAY}",
        "notes": "Operational route source; says no /fff first in incident or data-loss risk.",
    },
    {
        "source_handle": "N-TRGMOD-NATIVE",
        "source_tier": "T2_NOTION_SPEC",
        "system": "Notion",
        "source_title": "Trigger-Module - Terra Nova Native",
        "source_location": "Notion workspace page; URL withheld in public trace",
        "source_status": "module_spec_reference_not_master",
        "evidence_scope": "520 SessionStart, 521 Preflight, 517 AutoFlow, SAFE_MODE, RECOVER module specs",
        "mutation_status": f"read_only_fetch_{TODAY}",
        "notes": "JSON exports are evidence for future L3 work, not live execution contracts.",
    },
    {
        "source_handle": "N-TRGSYS-CAPII",
        "source_tier": "T2_NOTION_REFERENCE",
        "system": "Notion",
        "source_title": "Trigger-System - TerraNova/FerrAI",
        "source_location": "Notion workspace page; URL withheld in public trace",
        "source_status": "reference_not_master",
        "evidence_scope": "Triggerbank 001-600, MasterTrigger, CAP-II 205-210 licensing/Revoke path",
        "mutation_status": f"read_only_fetch_{TODAY}",
        "notes": "CAP-II path raises business, tokenomics and IP review gates for 205-210.",
    },
    {
        "source_handle": "N-TRGINDEX-V53",
        "source_tier": "T3_NOTION_IMPORTED_REFERENCE",
        "system": "Notion",
        "source_title": "Trigger_Index_TerraNova_V5.3",
        "source_location": "Notion imported/export page; URL withheld in public trace",
        "source_status": "imported_reference",
        "evidence_scope": "1001, 516, 520, 521, 544, 600, 777 index labels",
        "mutation_status": f"read_only_fetch_{TODAY}",
        "notes": "Useful corroboration, not highest authority.",
    },
    {
        "source_handle": "L-DEEP-REFERENCE-1-992",
        "source_tier": "T4_LOCAL_RAW_SOURCE_PACK",
        "system": "GitHub local",
        "source_title": "Trigger-System - Deep Reference (1-992)",
        "source_location": "raw/exports/prism/source-pack/2026-05-02/trigger-system-deep-reference",
        "source_status": "sensitive_local_reference",
        "evidence_scope": "1-170 base table, 171-505 gap statement, 516-523, 540/544, 777, 988-992, slash commands",
        "mutation_status": "local_read_only",
        "notes": "Do not publish raw; use as source-pack evidence and protected range anchor.",
    },
    {
        "source_handle": "L-GAP-LEDGER",
        "source_tier": "T3_LOCAL_CURATED",
        "system": "GitHub local",
        "source_title": "TerraNova Trigger Gap Ledger",
        "source_location": "docs/triggers/gap_ledger.md",
        "source_status": "curated_gap_snapshot",
        "evidence_scope": "Range-level status as of 2026-05-02",
        "mutation_status": "local_read_only",
        "notes": "Superseded for 174-210 by Notion Codex139+ evidence; still valid for unresolved ranges.",
    },
    {
        "source_handle": "L-TRIGGER-COMPLEMENT",
        "source_tier": "T3_LOCAL_SEED",
        "system": "GitHub local",
        "source_title": "Trigger Complement Seed 2026-03-30",
        "source_location": "atlas/sources/trigger-complement-2026-03-30.md",
        "source_status": "local_seed_mirror",
        "evidence_scope": "Trigger Truth additions, architecture layers, Atlas v1.1 clusters",
        "mutation_status": "local_read_only",
        "notes": "Public-safe mirror of user-provided Notion complement.",
    },
    {
        "source_handle": "L-ATLAS-MANIFEST-V11",
        "source_tier": "T3_LOCAL_CURATED",
        "system": "GitHub local",
        "source_title": "Atlas Manifest v1.1",
        "source_location": "atlas/atlas.manifest.v1.1.json",
        "source_status": "local_curated_manifest",
        "evidence_scope": "29 trigger objects, 15 trigger clusters, 675/1200 estimates",
        "mutation_status": "local_read_only",
        "notes": "Confirms selected anchors and clusters, not full per-trigger history.",
    },
    {
        "source_handle": "L-TRIGGER-001",
        "source_tier": "T3_LOCAL_CONTROL_TOWER",
        "system": "GitHub local",
        "source_title": "TRIGGER-001 Command Surface",
        "source_location": "docs/atlas/control-tower/trigger-001.command-surface.md",
        "source_status": "active_local_command_surface",
        "evidence_scope": "/fff, GO, STOP, FREEZE and bounded local execution rules",
        "mutation_status": "local_read_only",
        "notes": "/fff accelerates local reversible work; it does not authorize external mutation.",
    },
    {
        "source_handle": "L-MMD-004-007",
        "source_tier": "T3_LOCAL_CONTROL_TOWER",
        "system": "GitHub local",
        "source_title": "MMD-004 through MMD-007",
        "source_location": "docs/atlas/control-tower/mmd-004*.csv; docs/atlas/control-tower/mmd-007*.csv",
        "source_status": "local_canon_review",
        "evidence_scope": "Visual trigger bridge review, source review queue, L1/L2 admission for 516/520/521/540/544",
        "mutation_status": "local_read_only",
        "notes": "MMD-004 held 174-210 until source review; TRIGGER-MAP-001 performs that next review pass.",
    },
    {
        "source_handle": "L-SOURCE-520-521",
        "source_tier": "T3_LOCAL_CONTROL_TOWER",
        "system": "GitHub local",
        "source_title": "SOURCE-520 and SOURCE-521 primary source passes",
        "source_location": "docs/atlas/control-tower/source-520*.csv; docs/atlas/control-tower/source-521*.csv",
        "source_status": "local_source_review_complete",
        "evidence_scope": "L2 routing-marker decisions and blocked claims for 520/521",
        "mutation_status": "local_read_only",
        "notes": "Notion mutations were applied earlier only after explicit GO; this pass performs no mutation.",
    },
    {
        "source_handle": "L-XPORT-002",
        "source_tier": "T5_HASH_SAMPLE_EVIDENCE",
        "system": "GitHub local",
        "source_title": "CHATGPT-XPORT-002 review corridor",
        "source_location": "docs/atlas/control-tower/chatgpt-xport-002.review-summary.json",
        "source_status": "deduped_hash_sample_corridor",
        "evidence_scope": "12 tokenomics/trigger review samples without raw dialogue or IDs",
        "mutation_status": "local_read_only",
        "notes": "Supports next review targeting; does not itself define trigger semantics.",
    },
]


CODEX139_TRIGGERS = [
    ("174", "Impulsumkehrfeld", "Lenkt spontane Impulse kontrolliert in ihre energetische Gegenrichtung."),
    ("175", "Kernabsichtsfilter", "Filtert unterschwellige Absichten aus Stoerquellen und gleicht sie mit dem Systemziel ab."),
    ("176", "Synchronisationsfenster", "Oeffnet ein kurzes Zeitfenster, in dem bewusste und unbewusste Prozesse auf gleiche Frequenz gebracht werden."),
    ("177", "Traumaschnittstelle", "Erkennt tiefe emotionale Einbrueche und isoliert sie zur gezielten Weiterverarbeitung."),
    ("178", "Resonanzresetpunkt", "Bricht aktuelle Resonanzverbindungen bewusst ab, um Raum fuer eine Neujustierung zu schaffen."),
    ("179", "Verdichtungszone", "Verdichtet parallellaufende Denk- oder Emotionslinien zu einem steuerbaren Kernfokus."),
    ("180", "Zielvektor-Ueberschreibung", "Erlaubt das temporaere Ueberschreiben eines bestehenden Ziels zugunsten einer praeziseren Ausrichtung."),
    ("181", "Meta-Rhythmus-Slot", "Ermoeglicht rhythmisch korrekte Einbettung von Gedankenmodulen in laufende Prozesse."),
    ("182", "Ueberspannungsablauf", "Leitet innere emotionale oder mentale Ueberspannung kontrolliert ins Neutralfeld ab."),
    ("183", "Selbstbild-Neusatz", "Erlaubt bewussten Reset des Selbstbildes als Neusatz, nicht als Loeschung."),
    ("184", "Innere Buendelungszone", "Fasst zerstreute mentale oder emotionale Fragmente in einem Zentrum zusammen."),
    ("185", "Aussen-Filterresonanz", "Filtert fremde Resonanzfelder, bevor sie ins eigene System eindringen."),
    ("186", "Energiezuteilungspunkt", "Regelt Verteilung verfuegbarer Energie auf innere Subsysteme je nach Prioritaet."),
    ("187", "Reizantwort-Umcodierer", "Ueberschreibt automatische Reizreaktionsmuster durch bewusste Neucodierung."),
    ("188", "Erwartungsumkehr", "Kehrt tief verankerte Erwartungen temporaer um, um neue Perspektiven zuzulassen."),
    ("189", "Stilleinbruch-Induktor", "Erzeugt bewusst eine Luecke im inneren Klangfluss zur gezielten Selbstbeobachtung."),
    ("190", "Denkfeld-Magnetisierung", "Magnetisiert ein gewaehltes Denkfeld, um gezielte Fokussierung zu foerdern."),
    ("191", "Selbstkontakt-Anker", "Verankert den bewussten Selbstkontakt als stabilen Punkt bei emotionaler Ablenkung."),
    ("192", "Denkimpuls-Detektor", "Erkennt fruehzeitig Gedankenimpulse, bevor sie in Handlung ueberspringen."),
    ("193", "Zielbewusstseins-Booster", "Staerkt das bewusste Empfinden eines gewaehlten Ziels unabhaengig vom Umfeld."),
    ("194", "Mentale Vibrationstransparenz", "Erlaubt Klarheit darueber, welche inneren Vibrationen echt und welche fremdinduziert sind."),
    ("195", "Inneres Abgleichfenster", "Oeffnet temporaer ein Fenster zur Reflexion und Harmonisierung aller internen Prozesse."),
    ("196", "Stoerfeld-Entkoppler", "Trennt bewusst externe Stoerfelder von den eigenen mentalen und emotionalen Linien."),
    ("197", "Authentizitaetspegel", "Misst die Echtheit einer Handlung, Aussage oder Gedankenlinie im Moment des Entstehens."),
    ("198", "Verlangsamungsbefehl", "Verlangsamt mentale Prozesse bewusst, um Tiefenwirkung zu ermoeglichen."),
    ("199", "Systemeinklang-Abgleich", "Gleicht koerpereigene und systemische Rhythmen fuer harmonischen Gesamtlauf ab."),
    ("200", "Impuls-Ziel-Lotung", "Misst die Uebereinstimmung zwischen spontanem Impuls und tatsaechlichem Zielpfad."),
    ("201", "Verdeckungs-Aufloesungsmodul", "Hebt mentale oder emotionale Tarnfelder auf und zeigt den wahren Kern."),
    ("202", "Denkspannung-Pendel", "Gleicht Denkspannung durch inneres Pendeln zwischen zwei Extremen aus."),
    ("203", "Intentions-Spiegel", "Spiegelt unbewusste Absichten zurueck, bevor sie Handlung werden."),
    ("204", "Echo-Segmentierung", "Zerlegt Echo-Rueckmeldungen in verwertbare, nicht ueberladene Segmente."),
    ("205", "Impuls-Stopp-Schleife", "Faengt spontane Reaktionsimpulse ab, bevor sie eskalieren."),
    ("206", "Meta-Fokus-Trennung", "Trennt ueberlagerte Fokusse sauber und gibt jedem Kontext einen eigenen Raum."),
    ("207", "Regenerationsraster", "Ermoeglicht systemische Regeneration durch strukturierten Rueckzug."),
    ("208", "Inneres Warnsystem", "Erkennt feinstoffliche Warnsignale im Vorfeld einer mentalen Uebersteuerung."),
    ("209", "Kontrollpunkt-Verschiebung", "Verschiebt Kontrollpunkte innerhalb des Systems zur Dezentralisierung."),
    ("210", "Frequenz-Fokus-Einrastung", "Rastet fokussierte Frequenzen ein, um ein stabiles mentales Arbeitsfeld zu schaffen."),
]


def seed_row(
    map_id: str,
    trigger_ref: str,
    working_name: str,
    definition: str,
    status: str,
    canon_level: str,
    source_handles: str,
    cluster_refs: str,
    layer_or_band: str,
    publication_lane: str,
    review_gates: str,
    correlation_refs: str,
    allowed: str,
    blocked: str,
    notes: str,
) -> dict[str, str]:
    return {
        "map_id": map_id,
        "trigger_ref": trigger_ref,
        "working_name": working_name,
        "public_safe_definition": definition,
        "definition_status": status,
        "canon_level_now": canon_level,
        "source_handles": source_handles,
        "cluster_refs": cluster_refs,
        "layer_or_band": layer_or_band,
        "publication_lane": publication_lane,
        "review_gates": review_gates,
        "correlation_refs": correlation_refs,
        "allowed_use_now": allowed,
        "blocked_use_now": blocked,
        "notes": notes,
    }


def build_seed_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    add = rows.append

    add(
        seed_row(
            "TM001-S0001",
            "/fff",
            "Freedom for FerrAI",
            "Bounded internal steering for source reading, reasoning, local implementation, validation and mutation-package preparation.",
            "active_command_surface",
            "L2-LOCAL-COMMAND",
            "L-TRIGGER-001;N-ACTIVE-SYSTEM-TABLE",
            "Modi-System",
            "301-400",
            "internal_public_rule_ok",
            "external_mutation_go_required;incident_preflight_required",
            "CAP;IPERKA;Control Tower",
            "Execute local reversible work and create review artifacts.",
            "External writes, deletion, publication, credentials, payment actions, restricted-source exposure, raw private inventory export.",
            "In incidents, active Notion table requires /preflight -> /snapshot -> /audit -> /coherence before operative execution.",
        )
    )

    base_ranges = [
        ("TM001-R001", "001-010", "Codex base single triggers 1-10", "Startimpuls, Zielvektor, Spiegel, Anker, Faden, Riss, Bruecke, Schwelle, Kern and Schicht are present in the local Deep Reference base table."),
        ("TM001-R002", "011-020", "Wahrnehmungs-Cluster", "Sensorik, Filter, Fokus, Zoom, Panorama, Detail, Rauschen, Signal, Echo and Resonanz."),
        ("TM001-R003", "021-030", "Entscheidungs-Cluster", "Wahl, Verzweigung, Priorisierung, Gewichtung, Ausschluss, Einschluss, Delegation, Eskalation, Reduktion and Expansion."),
        ("TM001-R004", "031-040", "Struktur-Cluster", "Ordnung, Chaos, Muster, Abweichung, Symmetrie, Asymmetrie, Hierarchie, Netzwerk, Sequenz and Parallel."),
        ("TM001-R005", "041-050", "Kreativ-Cluster", "Funke, Flamme, Glut, Asche, Phoenix, Samen, Bluete, Frucht, Ernte and Kompost."),
        ("TM001-R006", "051-060", "Schutz-Cluster", "Schild, Mauer, Graben, Waechter, Alarm, Rueckzug, Tarnung, Ablenkung, Koeder and Falle."),
        ("TM001-R007", "061-170", "Codex base cluster tail", "Communication, time, energy, meta, social, identity, knowledge, Codex-Sync, process, stability and evolution clusters are present as range definitions."),
    ]
    for map_id, ref, name, definition in base_ranges:
        add(
            seed_row(
                map_id,
                ref,
                name,
                definition,
                "documented_range_reference",
                "L1/L2-RANGE-SOURCE",
                "L-DEEP-REFERENCE-1-992;N-CODEX-MASTER",
                "Codex 1-170",
                "1-200",
                "public_after_source_extraction",
                "per_trigger_extraction_required",
                "Codex170;Deep Reference;Trigger Truth",
                "Use as range-level source evidence.",
                "Do not claim every per-trigger field until the Codex170 master extraction is reviewed.",
                "TRIGGER-MAP-001 keeps range truth without inventing missing per-row detail.",
            )
        )

    for trigger_id in ("171", "172", "173"):
        add(
            seed_row(
                f"TM001-RS-{trigger_id}",
                trigger_id,
                f"Reserved Slot {trigger_id}",
                "Unausformulierter, bewusst reservierter Modulraum fuer spaetere Ausarbeitung.",
                "reserved_slot",
                "L0-ID-ANCHOR",
                "silvi_directive_2026-05-23",
                "Codex139 transition / reserved module room",
                "101-200",
                "hold_until_filled",
                "fill_from_xport_002_tnpx_01_future_session",
                "XPORT-002;TNPX-01;future session",
                "Reserve ID anchor only.",
                "No inferred name, behavior, activation protocol, public canon claim or module semantics.",
                "Silvi decision 2026-05-23: no source gap; reserved slot to be filled later.",
            )
        )

    for index, (trigger_id, name, definition) in enumerate(CODEX139_TRIGGERS, start=1):
        is_cap = 205 <= int(trigger_id) <= 210
        is_protected = trigger_id in {"177", "182", "208"}
        lane = "protected_biz_ip_review" if is_cap else ("internal_sensitivity_review" if is_protected else "public_after_trigger_review")
        gates = "source_review;definition_canon_gate"
        correlations = "Codex139+;Silvi-Modus;Codex170_Plus;TNPX-01;Triggerliste_600_pending"
        if is_cap:
            gates += ";biz_tokenomics_review;ip_review"
            correlations += ";CAP-II/Revoke;license_control"
        if is_protected:
            gates += ";sensitivity_language_review"
        add(
            seed_row(
                f"TM001-174210-{index:03d}",
                trigger_id,
                name,
                definition,
                "defined_reference_export",
                "L2-SOURCE-BACKED-REFERENCE",
                "N-CODEX139-174210;N-CODEX-MASTER;L-ATLAS-MANIFEST-V11",
                "Silvi-Modus Kognitiv",
                "101-300",
                lane,
                gates,
                correlations,
                "Use name and short definition as source-backed trigger-map entry.",
                "No canonical TRG assignment, activation protocol, public canon claim, medical claim or external mutation.",
                "Codex139+ is an export/reference, not the normative master.",
            )
        )

    anchors = [
        ("TM001-A001", "102", "Fixpunkt", "Recover to fixed point / last stable CAP source.", "known_anchor", "L1-ANCHOR", "L-TRIGGER-001;N-TRGMOD-NATIVE", "RECOVER", "101-200", "internal", "recovery_review", "CAP;RECOVER", "Use as recovery orientation.", "Do not continue mutation during contradiction.", "From TRIGGER-001 crosswalk and RECOVER spec."),
        ("TM001-A002", "143", "Kanonwaechter", "Canon guard coupled to audit checks.", "known_anchor", "L1-ANCHOR", "L-TRIGGER-001;N-TRGMOD-NATIVE", "SAFE_MODE", "101-200", "internal", "canon_review", "CAP;SAFE_MODE", "Compare claims against canon anchors.", "Do not promote/demote canon without trace.", "From TRIGGER-001 crosswalk and SAFE_MODE spec."),
        ("TM001-A003", "148", "Kontrollinstanz", "Control instance for boundary selection.", "known_anchor", "L1-ANCHOR", "L-TRIGGER-001;N-TRGMOD-NATIVE", "SAFE_MODE", "101-200", "internal", "boundary_review", "CAP;SAFE_MODE", "Select CAP state and deterministic boundary.", "Do not proceed without boundary.", "From TRIGGER-001 crosswalk and SAFE_MODE spec."),
        ("TM001-A004", "516", "Inspiration", "Creative-flow inspiration anchor; also active as /inspire.", "documented_subset", "L2-ROUTING-MARKER", "N-ACTIVE-SYSTEM-TABLE;N-TRGINDEX-V53;L-MMD-004-007;L-DEEP-REFERENCE-1-992", "Creative Flow", "401+", "internal", "direct_source_before_l3", "Creative Flow;MMD;Atlas v1.1", "Use as internal creative-flow routing marker.", "No AutoFlow sibling semantics or public trigger definition.", "MMD-007 admits bounded L2 routing marker."),
        ("TM001-A005", "517", "AutoFlow", "Flow-state module after 516; active as /flow but held as caution lane.", "documented_subset_caution", "L1/L2-CAUTION", "N-ACTIVE-SYSTEM-TABLE;N-TRGMOD-NATIVE;L-MMD-004-007", "Creative Flow", "401+", "internal_caution", "autoflow_source_review", "Creative Flow;MMD;Trigger Modules", "Use as named AutoFlow caution lane.", "No automatic creative flow semantics or L3 execution.", "SENS-002 keeps 517 under stop rules."),
        ("TM001-A006", "520", "SessionStart", "Active /start core entrypoint and bounded session/root-state marker.", "source_review_complete", "L2-ROUTING-MARKER", "N-ACTIVE-SYSTEM-TABLE;N-TRGMOD-NATIVE;N-TRGINDEX-V53;L-SOURCE-520-521", "Core System", "401+", "internal", "l3_contract_required", "CAP;SessionStart;Preflight", "Use as start-of-work-unit and session_opened routing marker.", "No init_all_modules execution, autonomous session control, external mutation permission, TRG assignment or public canon.", "SOURCE-520 and TEST-520 completed earlier."),
        ("TM001-A007", "521", "Preflight", "Active /preflight safety entrypoint and pre-action boundary gate.", "source_review_complete", "L2-ROUTING-MARKER-PROTECTED", "N-ACTIVE-SYSTEM-TABLE;N-TRGMOD-NATIVE;N-TRGINDEX-V53;L-SOURCE-520-521", "Core System;Protection Layer", "401+", "protected_internal", "protection_contract_required;777_boundary_closed", "CAP;Preflight;Protection", "Use as protected pre-action routing gate.", "No automation, protection execution behavior, Schattenarchiv-depth import, TRG assignment or public canon.", "SOURCE-521 upgraded from L1 protected to L2 routing marker."),
        ("TM001-A008", "522", "System Sync", "Synchronizes subsystems after Preflight in Deep Reference flow.", "documented_subset", "L1-NAME-FLOW", "L-DEEP-REFERENCE-1-992;L-ATLAS-MANIFEST-V11", "Core System", "401+", "internal", "direct_source_before_l2", "Core System;Sync", "Use as named flow member.", "No execution semantics or public canon.", "Exact Notion source not yet independently reviewed."),
        ("TM001-A009", "523", "Health Check", "Validates system health after System Sync in Deep Reference flow.", "documented_subset", "L1-NAME-FLOW", "L-DEEP-REFERENCE-1-992;L-ATLAS-MANIFEST-V11", "Core System", "401+", "internal", "direct_source_before_l2", "Core System;Health", "Use as named flow member.", "No execution semantics or public canon.", "Exact Notion source not yet independently reviewed."),
        ("TM001-A010", "540", "Observable Momentum / Momentum", "Progress and energy visibility marker; active as /momentum.", "documented_point", "L2-ROUTING-MARKER", "N-ACTIVE-SYSTEM-TABLE;L-MMD-004-007;L-DEEP-REFERENCE-1-992", "Meta-Reflexion", "401+", "internal", "prism_cap_text_before_l3", "Momentum;Prism;MMD", "Use as progress-visibility routing marker.", "No proof-of-correctness or metric-finality claim.", "MMD-007 admits bounded L2 routing marker."),
        ("TM001-A011", "544", "Synchronization Node / Sync-Knoten", "Synchronization and decision-point routing marker; active as /sync.", "documented_point", "L2-ROUTING-MARKER", "N-ACTIVE-SYSTEM-TABLE;N-TRGINDEX-V53;L-MMD-004-007", "Meta-Reflexion", "401+", "internal", "sync_scope_before_l3", "Sync;Decision;MMD", "Use as state-reconciliation routing marker.", "No automatic full workspace sync or public canon.", "MMD-007 admits bounded L2 routing marker."),
        ("TM001-A012", "300-325", "Metarotik band", "Intimate/creative trigger band recognized as active cluster, not expanded here.", "identified_cluster", "L1-CLUSTER", "L-TRIGGER-COMPLEMENT;L-DEEP-REFERENCE-1-992;L-ATLAS-MANIFEST-V11", "Metarotik", "301-400", "protected_later", "metarotik_review_later", "Metarotik;Phenomenology", "Preserve correlation as later review lane.", "Do not expose detailed semantics before workspace/export/tokenomics/trigger basis is stable.", "This pass intentionally defers Metarotik expansion."),
        ("TM001-A013", "601", "Flutung", "Metarotik-adjacent special anchor.", "documented_anchor", "L1-ANCHOR", "L-DEEP-REFERENCE-1-992;L-ATLAS-MANIFEST-V11", "Metarotik", "401+", "protected_later", "metarotik_review_later", "Metarotik;Flutung", "Use only as protected correlation marker.", "No public semantics or activation.", "Deferred until Metarotik pass."),
        ("TM001-A014", "700", "Codex 700", "Safety/readiness ritual anchor.", "documented_anchor", "L1-ANCHOR", "L-TRIGGER-COMPLEMENT;L-ATLAS-MANIFEST-V11", "Sicherheitsritual", "401+", "internal", "ritual_source_review", "Codex;Safety", "Use as named safety/checkpoint anchor.", "No ritual execution protocol.", "Cluster confirmed in Atlas v1.1 complement."),
        ("TM001-A015", "777", "Schattenarchiv", "Protected Schattenarchiv access/audit/backup/control variants.", "documented_sensitive", "PROTECTED-LANE", "N-ACTIVE-SYSTEM-TABLE;L-DEEP-REFERENCE-1-992;L-ATLAS-MANIFEST-V11", "Schattenarchiv;Protection Layer", "401+", "protected_internal_only", "explicit_review_required", "Schattenarchiv;Sigma;Protection", "Use as protected internal boundary marker.", "No normal module admission, public semantics, raw identity or depth exposure.", "SENS-002 keeps 777 outside normal module admission."),
        ("TM001-A016", "888", "Truth and Efficiency", "Audit overlay for truth, efficiency, source, boundary and result.", "documented_anchor", "L2-AUDIT-OVERLAY", "L-TRIGGER-001;L-TRIGGER-COMPLEMENT;L-ATLAS-MANIFEST-V11", "Truth and Efficiency", "overlay", "internal_public_rule_ok", "audit_consistency_review", "CAP;Audit", "Use as overlay before continuing after source/boundary risk.", "Do not continue after failed audit.", "Core Equilibrium audit anchor."),
        ("TM001-A017", "988", "Snapshot / Token Verify", "Snapshot lockpoint or token verification anchor depending on source layer.", "documented_sensitive_conflict", "PROTECTED-LANE", "N-ACTIVE-SYSTEM-TABLE;L-DEEP-REFERENCE-1-992;L-ATLAS-MANIFEST-V11", "Audit and Security", "401+", "protected_internal_only", "security_token_review", "MAXSync;TokenAccess;Audit", "Use as protected audit/security marker.", "No public token/security details or wallet/account exposure.", "Name conflict is tracked in contradictions."),
        ("TM001-A018", "989", "Token Sync Beacon", "Passive token sync beacon in active Notion table.", "documented_sensitive", "PROTECTED-LANE", "N-ACTIVE-SYSTEM-TABLE;L-ATLAS-MANIFEST-V11", "Audit and Security", "401+", "protected_internal_only", "security_token_review", "MAXSync;TokenAccess", "Use as protected token-sync marker.", "No public token or wallet operational detail.", "Raw Deep Reference does not enumerate 989 label in same way."),
        ("TM001-A019", "990", "Audit / Audit Seal", "Audit entry point or audit seal depending on source layer.", "documented_sensitive_conflict", "PROTECTED-LANE", "N-ACTIVE-SYSTEM-TABLE;L-DEEP-REFERENCE-1-992;L-ATLAS-MANIFEST-V11", "Audit and Security", "401+", "protected_internal_only", "security_token_review", "Audit;MAXSync", "Use as protected audit marker.", "No public security execution semantics.", "Name conflict is tracked in contradictions."),
        ("TM001-A020", "991", "ZIP Integrity Pulse", "ZIP integrity pulse in active Notion table.", "documented_sensitive", "PROTECTED-LANE", "N-ACTIVE-SYSTEM-TABLE;L-ATLAS-MANIFEST-V11", "Audit and Security", "401+", "protected_internal_only", "security_token_review", "ZIP;Integrity;MAXSync", "Use as protected integrity marker.", "No raw ZIP or token security details.", "Active table is operational source."),
        ("TM001-A021", "992", "TriggerMap Echo Sync / Session Close", "Echo-sync or session-close anchor depending on source layer.", "documented_sensitive_conflict", "PROTECTED-LANE", "N-ACTIVE-SYSTEM-TABLE;L-DEEP-REFERENCE-1-992;L-ATLAS-MANIFEST-V11", "Audit and Security", "401+", "protected_internal_only", "security_token_review", "Echo Sync;Session Close;MAXSync", "Use as protected sync/close marker.", "No public security execution semantics.", "Name conflict is tracked in contradictions."),
        ("TM001-A022", "999", "Coherence", "Workspace coherence anchor; active as /coherence.", "documented_anchor", "L2-AUDIT-ROUTING", "N-ACTIVE-SYSTEM-TABLE;L-TRIGGER-COMPLEMENT;L-ATLAS-MANIFEST-V11", "Truth and Efficiency", "401+", "internal_public_rule_ok", "audit_consistency_review", "CAP;Coherence", "Use as coherence audit route.", "No claim of automatic full workspace correction.", "Part of active emergency chain."),
        ("TM001-A023", "1001", "Ponyverse Sync / Pegasus", "Pegasus/Ponyverse sync and output-log analysis anchor.", "documented_anchor", "L1/L2-ANCHOR", "N-TRGINDEX-V53;L-TRIGGER-COMPLEMENT;L-ATLAS-MANIFEST-V11", "Pegasus", "401+", "internal", "pegasus_review", "Pegasus;Ponyverse", "Use as output-log analysis/sync marker.", "No public execution protocol.", "Names vary by source layer; preserve both as correlation."),
    ]
    for row in anchors:
        add(seed_row(*row))

    return rows


RANGE_STATUS = [
    {
        "range_ref": "001-170",
        "status_before": "documented",
        "status_after": "documented_range_source_backed",
        "evidence_handles": "L-DEEP-REFERENCE-1-992;N-CODEX-MASTER",
        "confidence": "high_for_range;medium_for_per_trigger_fields",
        "publication_lane": "public_after_extraction_review",
        "next_action": "Extract reviewed per-trigger rows from Codex170 master before claiming public per-trigger canon.",
    },
    {
        "range_ref": "171-173",
        "status_before": "open_partial_inside_171_505",
        "status_after": "reserved_slot",
        "evidence_handles": "silvi_directive_2026-05-23",
        "confidence": "owner_decision",
        "publication_lane": "hold",
        "next_action": "fill from XPORT-002 / TNPX-01 / future session",
    },
    {
        "range_ref": "174-210",
        "status_before": "source_review_needed_or_open_partial",
        "status_after": "documented_reference_export",
        "evidence_handles": "N-CODEX139-174210;N-CODEX-MASTER;L-ATLAS-MANIFEST-V11;L-MMD-004-007",
        "confidence": "high_for_names_and_short_definitions;medium_for_canon_level",
        "publication_lane": "public_after_trigger_review;205-210_protected_biz_ip_review",
        "next_action": "Promote from visual range to source-backed seed entries without assigning canonical TRG IDs.",
    },
    {
        "range_ref": "211-299",
        "status_before": "open_partial_inside_171_505",
        "status_after": "open_partial",
        "evidence_handles": "L-GAP-LEDGER;L-DEEP-REFERENCE-1-992",
        "confidence": "low",
        "publication_lane": "hold",
        "next_action": "Do not infer from 174-210; search Notion and ChatGPT exports.",
    },
    {
        "range_ref": "300-325",
        "status_before": "known_exception_inside_171_505",
        "status_after": "identified_metarotik_cluster_hold",
        "evidence_handles": "L-DEEP-REFERENCE-1-992;L-TRIGGER-COMPLEMENT;L-ATLAS-MANIFEST-V11",
        "confidence": "medium_for_cluster;low_for_per_trigger_fields",
        "publication_lane": "protected_later",
        "next_action": "Defer detailed Metarotik expansion until tokenomics and trigger base are stable.",
    },
    {
        "range_ref": "326-505",
        "status_before": "open_partial_inside_171_505",
        "status_after": "open_partial",
        "evidence_handles": "L-GAP-LEDGER;L-DEEP-REFERENCE-1-992",
        "confidence": "low",
        "publication_lane": "hold",
        "next_action": "Search only after 171-210 source pass is reconciled.",
    },
    {
        "range_ref": "506-515",
        "status_before": "open",
        "status_after": "open",
        "evidence_handles": "L-GAP-LEDGER",
        "confidence": "low",
        "publication_lane": "hold",
        "next_action": "Leave unassigned until a reviewed source appears.",
    },
    {
        "range_ref": "516-523",
        "status_before": "documented_subset",
        "status_after": "documented_subset_with_L2_for_520_521",
        "evidence_handles": "N-ACTIVE-SYSTEM-TABLE;N-TRGMOD-NATIVE;N-TRGINDEX-V53;L-SOURCE-520-521;L-DEEP-REFERENCE-1-992",
        "confidence": "high_for_520_521;medium_for_516_517_522_523",
        "publication_lane": "internal;public_after_module_review",
        "next_action": "Keep 520/521 at L2; source-review 516/517/522/523 before L3.",
    },
    {
        "range_ref": "540/544",
        "status_before": "documented_points",
        "status_after": "documented_L2_routing_markers",
        "evidence_handles": "N-ACTIVE-SYSTEM-TABLE;L-MMD-004-007;L-DEEP-REFERENCE-1-992",
        "confidence": "medium_high",
        "publication_lane": "internal;public_after_scope_review",
        "next_action": "Tie each to explicit Prism/CAP source and sync-scope tests before L3.",
    },
    {
        "range_ref": "777",
        "status_before": "sensitive",
        "status_after": "protected_lane",
        "evidence_handles": "N-ACTIVE-SYSTEM-TABLE;L-DEEP-REFERENCE-1-992;L-ATLAS-MANIFEST-V11",
        "confidence": "high_for_boundary",
        "publication_lane": "protected_internal_only",
        "next_action": "Keep outside normal module admission unless Silvan explicitly opens Schattenarchiv review.",
    },
    {
        "range_ref": "988-992",
        "status_before": "documented_sensitive",
        "status_after": "protected_sensitive_with_label_conflict",
        "evidence_handles": "N-ACTIVE-SYSTEM-TABLE;L-DEEP-REFERENCE-1-992;L-ATLAS-MANIFEST-V11",
        "confidence": "high_for_protected_range;medium_for_labels",
        "publication_lane": "protected_internal_only",
        "next_action": "Resolve active-table labels against TokenAccess TriggerMap before public appendix.",
    },
    {
        "range_ref": "slash_commands",
        "status_before": "documented_group",
        "status_after": "documented_group_bounded",
        "evidence_handles": "L-DEEP-REFERENCE-1-992;L-TRIGGER-001;N-ACTIVE-SYSTEM-TABLE",
        "confidence": "medium_high",
        "publication_lane": "public_after_command_surface_review",
        "next_action": "Keep /fff bounded; do not normalize /ffff or destructive commands without separate hardening.",
    },
]


CONTRADICTIONS = [
    {
        "contradiction_id": "TM001-C001",
        "claim_a": "Local gap ledger marks 171-505 as open/partial.",
        "source_a": "L-GAP-LEDGER;L-DEEP-REFERENCE-1-992",
        "claim_b": "Notion Codex139+ reference says 174-210 are fully defined modules.",
        "source_b": "N-CODEX139-174210",
        "resolution": "Upgrade 174-210 to documented_reference_export; keep 171-173 and 211-505 open/partial until direct source appears.",
        "human_decision_required": "No",
        "next_action": "Backpropagate this correction into future trigger gap ledger pass.",
    },
    {
        "contradiction_id": "TM001-C002",
        "claim_a": "Codex139+ includes activation/use-case language for 174-210.",
        "source_a": "N-CODEX139-174210",
        "claim_b": "CAP canon admission blocks activation protocol, L3 semantics and public canon without reviewed tests/contracts.",
        "source_b": "L-MMD-004-007;L-SOURCE-520-521;N-TTRUTH-001",
        "resolution": "Admit names and short definitions as L2 source-backed references only; block execution and public canon.",
        "human_decision_required": "No",
        "next_action": "Create SOURCE-174-210 if public module definitions are needed.",
    },
    {
        "contradiction_id": "TM001-C003",
        "claim_a": "Deep Reference labels 988/990/992 as Token Verify, Audit Seal and Session Close.",
        "source_a": "L-DEEP-REFERENCE-1-992",
        "claim_b": "Active Notion table routes 988/990/992 as /snapshot, /audit and TriggerMap Echo Sync.",
        "source_b": "N-ACTIVE-SYSTEM-TABLE",
        "resolution": "Active table wins for operational routing; raw labels are preserved as historical/reference aliases; range stays protected.",
        "human_decision_required": "No",
        "next_action": "Resolve with TokenAccess TriggerMap before public appendix.",
    },
    {
        "contradiction_id": "TM001-C004",
        "claim_a": "Old trigger tables imply one visible ID row equals one trigger entry.",
        "source_a": "L-DEEP-REFERENCE-1-992;L-ATLAS-MANIFEST-V11",
        "claim_b": "Trigger Truth says Trigger-ID is not a unique trigger entry.",
        "source_b": "N-TTRUTH-001",
        "resolution": "TRIGGER-MAP-001 treats trigger_ref as a reference anchor, not a unique deployment instance; unique key is deferred to future instance registry.",
        "human_decision_required": "No",
        "next_action": "Use Trigger-ID + layer/instance + mode/promille + context in TRIGGER-DEF-001.",
    },
    {
        "contradiction_id": "TM001-C005",
        "claim_a": "/fff authorizes high-agency local execution.",
        "source_a": "L-TRIGGER-001",
        "claim_b": "Active Notion table says no /fff first in incident/data-loss risk.",
        "source_b": "N-ACTIVE-SYSTEM-TABLE",
        "resolution": "/fff remains active for local reversible work; incident paths must run /preflight -> /snapshot -> /audit -> /coherence first.",
        "human_decision_required": "No",
        "next_action": "Keep this boundary in future command-surface updates.",
    },
    {
        "contradiction_id": "TM001-C006",
        "claim_a": "User memory states every trigger up to at least 210 has some module definition.",
        "source_a": "Silvan instruction in current run",
        "claim_b": "Current read-only search did not locate direct source rows for 171-173.",
        "source_b": "Notion workspace_search 2026-05-23;local rg source-search 2026-05-23;L-GAP-LEDGER",
        "resolution": "Silvi resolves 171-173 as consciously reserved slots: status reserved_slot, canon L0-ID-ANCHOR, source silvi_directive_2026-05-23.",
        "human_decision_required": "No",
        "next_action": "fill from XPORT-002 / TNPX-01 / future session",
    },
]


SOURCE_SEARCH = [
    {
        "search_id": "TM001-SS001",
        "target": "171-173",
        "surface": "Notion workspace_search",
        "query_or_pattern": "Trigger 171 172 173 Codex139 TriggerExport SilviModus",
        "result_class": "no_direct_definition",
        "evidence_summary": "Returned Codex139+ 174-210 and broader trigger pages, but no direct 171, 172 or 173 definition rows.",
        "publication_boundary": "public_safe_summary_only",
        "next_action": "Apply Silvi reserved-slot directive; fill from XPORT-002 / TNPX-01 / future session.",
    },
    {
        "search_id": "TM001-SS002",
        "target": "171-173",
        "surface": "Notion workspace_search",
        "query_or_pattern": "Trigger 171 Trigger 172 Trigger 173 TerraNova",
        "result_class": "no_direct_definition",
        "evidence_summary": "Returned Trigger-System, Trigger_Index and active system table sources, but no direct 171-173 trigger definitions.",
        "publication_boundary": "public_safe_summary_only",
        "next_action": "Do not infer behavior; preserve L0 reserved ID anchors.",
    },
    {
        "search_id": "TM001-SS003",
        "target": "171-173",
        "surface": "local_repo_rg",
        "query_or_pattern": "Trigger[-_ ]?(171|172|173) and Trigger-ID nearby patterns",
        "result_class": "resolved_by_reserved_slot_directive",
        "evidence_summary": "Matches were gap ledgers, Atlas open-gap notes and newly generated TRIGGER-MAP-001 artifacts; no prior source definition row appeared.",
        "publication_boundary": "public_safe_summary_only",
        "next_action": "Use silvi_directive_2026-05-23 as current source for slot status only.",
    },
    {
        "search_id": "TM001-SS004",
        "target": "171-173",
        "surface": "raw/exports/incoming",
        "query_or_pattern": "bare 171/172/173 scan",
        "result_class": "false_positive_numbering",
        "evidence_summary": "Hits were window numbers, upload/file table rows, page counts or inventory row numbers, not trigger IDs or definitions.",
        "publication_boundary": "do_not_publish_raw_context",
        "next_action": "Do not treat raw numbering as trigger evidence; reserved slot status comes from Silvi directive.",
    },
    {
        "search_id": "TM001-SS005",
        "target": "174-210",
        "surface": "raw/exports/prism and local repo",
        "query_or_pattern": "174-210 / Codex139+ / SilviModus",
        "result_class": "corroborated_range_evidence",
        "evidence_summary": "Local Atlas, raw all-in-one and MMD bridge sources repeatedly identify Codex139+ / Trigger 174-210 as a visible range; Notion Codex139+ supplies the definitions.",
        "publication_boundary": "public_safe_summary_only",
        "next_action": "Use Notion Codex139+ as definition source; keep local raw as corroborating relation evidence.",
    },
]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"No rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_batch_markdown(seed_rows: list[dict[str, str]]) -> str:
    status_counts = Counter(row["definition_status"] for row in seed_rows)
    lane_counts = Counter(row["publication_lane"] for row in seed_rows)
    return f"""# {BATCH} - Trigger Source Map Pass

Status: local complete
Date: {TODAY}
Mode: STUDIO / `/fff` bounded local execution
External mutation: none

## Purpose

`TRIGGER-MAP-001` converts the current workspace evidence into a source-backed
trigger map without inventing missing rules. It follows the post
`CHATGPT-XPORT-002` sequence: Notion and local source anchors first, ChatGPT
exports as review corridor, tokenomics/trigger work next, Metarotik later.

## Source Principle

No new trigger rule is created in this pass. Existing Notion, local GitHub and
raw source-pack evidence is indexed first. If a number or range is visible but
not source-backed, it remains a review lane.

The controlling Trigger Truth rule is:

```text
Trigger-ID != unique trigger entry
unique key = Trigger-ID + Layer/Instanz + Modus/Promille + Kontext
```

`trigger-map-001.seed.csv` therefore uses `trigger_ref` as a source anchor, not
as a deployment instance key.

## Main Findings

- `174-210` is no longer just a visual range: the Notion Codex139+ export gives
  all 37 names and short definitions.
- `174-210` is still not public trigger canon. It is admitted here as
  `L2-SOURCE-BACKED-REFERENCE`, with execution, activation protocol and public
  `TRG-*` assignment blocked.
- `171-173` are reserved slots per Silvi decision from 2026-05-23. They are
  `reserved_slot` / `L0-ID-ANCHOR`, not source gaps.
- `205-210` is source-backed but routed through CAP-II/Revoke, tokenomics,
  business and IP review before any publication use.
- `988-992` stays protected because active Notion labels and the local Deep
  Reference labels differ.
- `/fff` is active as bounded local steering, but incident/data-loss paths still
  require `/preflight -> /snapshot -> /audit -> /coherence` first.

## Outputs

| File | Role |
| --- | --- |
| `trigger-map-001.source-index.csv` | Source handles, tiers and public-safe evidence scopes. |
| `trigger-map-001.seed.csv` | Source-backed trigger seed rows, including `174-210`. |
| `trigger-map-001.range-status.csv` | Range-level correction map from old gap ledger to current evidence. |
| `trigger-map-001.contradictions.csv` | Drift and conflict ledger with current resolutions. |
| `trigger-map-001.source-search.csv` | Positive and negative search trace for `171-173` and `174-210`. |
| `trigger-map-001.review-summary.json` | Machine-readable counts and next action. |
| `causal-log.trigger-map-001-{TODAY}.json` | Causal coherence log for this pass. |

## Counts

| Metric | Value |
| --- | --- |
| Source handles | {len(SOURCES)} |
| Seed rows | {len(seed_rows)} |
| Codex139+ 174-210 rows | {len(CODEX139_TRIGGERS)} |
| Range-status rows | {len(RANGE_STATUS)} |
| Contradictions | {len(CONTRADICTIONS)} |
| Source-search rows | {len(SOURCE_SEARCH)} |

## Seed Status Counts

| Status | Count |
| --- | --- |
{chr(10).join(f"| `{key}` | {value} |" for key, value in sorted(status_counts.items()))}

## Publication Lane Counts

| Lane | Count |
| --- | --- |
{chr(10).join(f"| `{key}` | {value} |" for key, value in sorted(lane_counts.items()))}

## Next Action

`SOURCE-174-210` if the next goal is public-safe trigger definition review.
Keep `171-173` as reserved slots and fill them later from XPORT-002, TNPX-01 or
a future session.
"""


def build_summary(seed_rows: list[dict[str, str]]) -> dict:
    status_counts = Counter(row["definition_status"] for row in seed_rows)
    lane_counts = Counter(row["publication_lane"] for row in seed_rows)
    return {
        "batch": BATCH,
        "created": TODAY,
        "mode": "STUDIO / /fff bounded local execution",
        "external_mutation": False,
        "notion_mutation": False,
        "source_handles": len(SOURCES),
        "seed_rows": len(seed_rows),
        "codex139_174_210_rows": len(CODEX139_TRIGGERS),
        "range_status_rows": len(RANGE_STATUS),
        "contradictions": len(CONTRADICTIONS),
        "source_search_rows": len(SOURCE_SEARCH),
        "definition_status_counts": dict(sorted(status_counts.items())),
        "publication_lane_counts": dict(sorted(lane_counts.items())),
        "upgrades": [
            "174-210 moved from visual/source-review-needed range to documented_reference_export.",
            "205-210 are source-backed but gated by CAP-II/Revoke, tokenomics, business and IP review.",
        ],
        "unresolved": [
            "211-505 remains open/partial except known documented exceptions.",
            "988-992 label conflict requires TokenAccess TriggerMap review before public appendix.",
        ],
        "reserved_slots": ["171", "172", "173"],
        "next_best_action": "SOURCE-174-210; fill 171-173 later from XPORT-002 / TNPX-01 / future session.",
        "boundaries": {
            "raw_messages_printed": False,
            "raw_notion_urls_printed": False,
            "local_private_inventory_exported": False,
            "canonical_trg_ids_assigned": False,
            "public_trigger_canon_created": False,
            "external_mutation_performed": False,
        },
    }


def build_causal_log() -> dict:
    return {
        "log_id": f"CAP-LOG-{TODAY}-TRIGGER-MAP-001",
        "created_at": CREATED_AT,
        "operator": "Codex / FerrAI",
        "mode": "STUDIO",
        "activation": "/fff",
        "source_trace": [
            "N-CODEX-MASTER",
            "N-TTRUTH-001",
            "N-CODEX139-174210",
            "N-ACTIVE-SYSTEM-TABLE",
            "N-TRGMOD-NATIVE",
            "N-TRGSYS-CAPII",
            "L-DEEP-REFERENCE-1-992",
            "L-GAP-LEDGER",
            "L-TRIGGER-COMPLEMENT",
            "L-ATLAS-MANIFEST-V11",
            "L-XPORT-002",
        ],
        "observation": "Local gap artifacts held 174-210 for source review, while Notion Codex139+ supplies all 37 names and short definitions.",
        "trigger_band": "201-300",
        "trigger_ids": ["174-210", "205-210", "520", "521", "777", "988-992", "/fff"],
        "probabilistic_hypothesis": "The next stable trigger layer is a source-backed map, not a public canon or execution protocol.",
        "probability_note": "High confidence for 174-210 names/short definitions; 171-173 are owner-reserved L0 ID anchors; lower confidence remains for sensitive security/token labels.",
        "deterministic_boundary": "No external mutation, no raw private inventory export, no canonical TRG assignment, and no public canon without source-tiered admission.",
        "selected_action": "Create TRIGGER-MAP-001 source index, seed rows, range-status corrections, contradiction ledger and review summary.",
        "feedback_target": "trigger_map",
        "backpropagation_result": "174-210 is promoted to documented reference evidence; 171-173 are reserved slots per Silvi directive; 211-505 remains open except known exceptions; 205-210 and 988-992 stay protected.",
        "verification_state": "notion_checked",
        "external_mutation": False,
        "mutation_authorization": "",
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    seed_rows = build_seed_rows()

    write_csv(OUT / "trigger-map-001.source-index.csv", SOURCES)
    write_csv(OUT / "trigger-map-001.seed.csv", seed_rows)
    write_csv(OUT / "trigger-map-001.range-status.csv", RANGE_STATUS)
    write_csv(OUT / "trigger-map-001.contradictions.csv", CONTRADICTIONS)
    write_csv(OUT / "trigger-map-001.source-search.csv", SOURCE_SEARCH)
    write_json(OUT / "trigger-map-001.review-summary.json", build_summary(seed_rows))
    write_json(OUT / f"causal-log.trigger-map-001-{TODAY}.json", build_causal_log())
    (OUT / "batch-trigger-map-001.md").write_text(build_batch_markdown(seed_rows), encoding="utf-8")


if __name__ == "__main__":
    main()
