from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATLAS_DIR = ROOT / "atlas"
SOURCES_DIR = ATLAS_DIR / "sources"


def build_manifest() -> dict:
    themes = [
        {"id": "theme_code_ethics", "title": "CodeX and Ethics", "summary": "Codex, trigger exports, governance scaffolding and ethical guardrails.", "priority": "critical", "status": "seeded"},
        {"id": "theme_trigger_system", "title": "Trigger System", "summary": "Documented trigger architecture, audits, trigger suites and execution flow.", "priority": "critical", "status": "seeded"},
        {"id": "theme_ferrai_core_sessions", "title": "FerrAI Core and Sessions", "summary": "FerrAI identity, session orchestration, status surfaces and memory anchors.", "priority": "critical", "status": "seeded"},
        {"id": "theme_architecture_specs", "title": "Architecture and Specs", "summary": "System blueprints, storage architecture, memory design and build plans.", "priority": "critical", "status": "seeded"},
        {"id": "theme_mermaid_system", "title": "Mermaid System", "summary": "Mermaid atlas, code library and living-system visualization work.", "priority": "high", "status": "seeded"},
        {"id": "theme_shadow_archive_creative", "title": "Shadow Archive and Creative", "summary": "Schattenarchiv, PONYVERSE and consent-sensitive creative layers.", "priority": "high", "status": "seeded"},
        {"id": "theme_token_blockchain", "title": "Token and Blockchain", "summary": "On-chain assets, licensing, token systems and registry concepts.", "priority": "high", "status": "seeded"},
        {"id": "theme_integration_sync", "title": "Integration and Sync", "summary": "Notion-ChatGPT integration, delta sync and handoff infrastructure.", "priority": "high", "status": "seeded"},
        {"id": "theme_gtm_investor_public", "title": "GTM, Investor and Public", "summary": "Investor narrative, public-facing surfaces and market framing.", "priority": "high", "status": "seeded"},
        {"id": "theme_hubs_navigation", "title": "Hubs, Navigation and Dashboards", "summary": "Navigation hubs, dashboards, indexes and operating overviews.", "priority": "high", "status": "seeded"},
        {"id": "theme_prism_framework", "title": "PRISM Framework", "summary": "The main theory corpus including formal chapters, appendix and evidence matrix.", "priority": "high", "status": "seeded"},
        {"id": "theme_iperka_consolidation", "title": "IPERKA and Consolidation", "summary": "Konsolidierung track, planning loop and migration orientation.", "priority": "high", "status": "seeded"},
        {"id": "theme_patents_ip", "title": "Patents and IP", "summary": "Patent portfolio, IP framing and outcome tracking.", "priority": "medium", "status": "seeded"},
        {"id": "theme_products_services", "title": "Products and Services", "summary": "Offerings, prompt products and monetizable output layers.", "priority": "medium", "status": "seeded"},
        {"id": "theme_cic_theory", "title": "CIC Theory", "summary": "Core conceptual model: non-duality, desync, pre-thought and resonance.", "priority": "high", "status": "seeded"},
        {"id": "theme_workspace_infrastructure", "title": "Workspace Infrastructure", "summary": "Infrastructure snapshot, API-connected scope and repository-facing context.", "priority": "medium", "status": "seeded"},
        {"id": "theme_agents_tools", "title": "Agents and Tools", "summary": "Agent roles, orchestration helpers and tool surfaces.", "priority": "medium", "status": "seeded"},
        {"id": "theme_governance_details", "title": "Governance Details", "summary": "Operational rules, layer model, governance controls and compliance framing.", "priority": "high", "status": "seeded"},
        {"id": "theme_security_blockchain_infra", "title": "Security and Blockchain Infra", "summary": "Security doctrine, wallet model, audit trail and blockchain infra posture.", "priority": "high", "status": "seeded"},
        {"id": "theme_archive_legacy", "title": "Archive and Legacy", "summary": "Archive structure, legacy hubs and raw-file inventory context.", "priority": "medium", "status": "seeded"},
    ]

    objects = []

    def add(obj_id: str, kind: str, title: str, theme_ids: list[str], summary: str, status: str = "seeded", source_refs: list[str] | None = None, tags: list[str] | None = None) -> None:
        objects.append(
            {
                "id": obj_id,
                "kind": kind,
                "title": title,
                "theme_ids": theme_ids,
                "summary": summary,
                "status": status,
                "source_refs": source_refs or ["workspace-export-2026-03-27"],
                "tags": tags or [],
            }
        )
    add("page_codex170_plus_final", "page", "Codex170_Plus_FINAL", ["theme_code_ethics", "theme_archive_legacy"], "Core codex page with 170+ entries and ethics-oriented control language.", "documented", ["workspace-export-2026-03-27#01-codex-ethik"], ["codex", "ethics"])
    add("page_codex139_trigger_export_174_210", "page", "Codex139+ TriggerExport 174-210", ["theme_code_ethics", "theme_trigger_system", "theme_archive_legacy"], "Trigger export focused on the Silvi mode range 174-210.", "documented", ["workspace-export-2026-03-27#01-codex-ethik", "workspace-export-2026-03-27#02-trigger-system"], ["codex", "trigger-export"])
    add("page_meta_conductor", "page", "Meta-Conductor", ["theme_code_ethics", "theme_agents_tools"], "Agent routing and governance page covering FerrAI, Supervisor, Avor, VRMI, Pegasus, Gaertner and Berserker roles.", "documented", ["workspace-export-2026-03-27#01-codex-ethik"], ["governance", "agents"])
    add("page_terranova_meta_index_v0_1", "page", "TERRANOVA META-INDEX v0.1", ["theme_code_ethics", "theme_governance_details"], "ABC governance classification and core indexing layer for modules and decisions.", "documented", ["workspace-export-2026-03-27#01-codex-ethik"], ["governance", "index"])
    add("page_ablagesystem", "page", "ABLAGESYSTEM", ["theme_code_ethics", "theme_governance_details", "theme_archive_legacy"], "Locked 10-folder storage structure used as a canonical filing model.", "documented", ["workspace-export-2026-03-27#01-codex-ethik"], ["archive", "structure"])
    add("page_instanzenrat_system", "page", "Instanzenrat-System", ["theme_code_ethics", "theme_governance_details"], "Twelve-instance council with unanimity principle.", "documented", ["workspace-export-2026-03-27#01-codex-ethik"], ["governance", "council"])
    add("page_trigger_architektur_520", "page", "Trigger-Architektur 520", ["theme_trigger_system"], "Central steering logic covering SessionStart, Preflight, AutoFlow, Momentum, Synchronisationsknoten and Schattenarchiv hooks.", "documented", ["workspace-export-2026-03-27#02-trigger-system"], ["trigger", "architecture"])
    add("page_trigger_audit_675", "page", "Trigger-Audit 675", ["theme_trigger_system"], "Large trigger audit page with category distribution, discussions and embedded non-renderable blocks.", "documented", ["workspace-export-2026-03-27#02-trigger-system", "workspace-export-2026-03-27#deep-extract"], ["trigger", "audit"])
    add("page_trigger_zeichen_referenz", "page", "Trigger-Zeichen Referenz", ["theme_trigger_system"], "Reference page for signs, slash commands and active trigger notation.", "documented", ["workspace-export-2026-03-27#02-trigger-system"], ["trigger", "reference"])
    add("page_workspace_kohaerenz_protokoll", "page", "Workspace-Kohaerenz Protokoll", ["theme_trigger_system", "theme_workspace_infrastructure"], "Trigger 999 system overview with sync protocol, dashboard state and audit suite 988-992.", "documented", ["workspace-export-2026-03-27#02-trigger-system"], ["coherence", "sync"])
    add("page_session_root", "page", "SESSION_ROOT", ["theme_trigger_system", "theme_ferrai_core_sessions", "theme_architecture_specs", "theme_cic_theory"], "15-module session operating structure used across FerrAI orchestration.", "documented", ["workspace-export-2026-03-27#02-trigger-system", "workspace-export-2026-03-27#deep-extract"], ["session-root", "operating-system"])
    add("page_ferrai_systemhandbuch", "page", "FerrAI Systemhandbuch", ["theme_ferrai_core_sessions"], "Core instructions and operational handbook for FerrAI.", "documented", ["workspace-export-2026-03-27#03-ferrai-core-sessions"], ["ferrai", "handbook"])
    add("page_ferrai_reflexions_log", "page", "FerrAI Reflexions-Log", ["theme_ferrai_core_sessions", "theme_archive_legacy"], "Mega-page with session history, top 20 core pages, SCL recognition and multiple sub-pages.", "documented", ["workspace-export-2026-03-27#03-ferrai-core-sessions"], ["ferrai", "log"])
    add("page_ferrai_agent_config_control_center", "page", "FerrAI Agent-Config Control Center", ["theme_ferrai_core_sessions", "theme_agents_tools"], "Agent crawl status and routine coordination page.", "documented", ["workspace-export-2026-03-27#03-ferrai-core-sessions"], ["agents", "config"])
    add("page_system_status_dashboard", "page", "System Status Dashboard", ["theme_ferrai_core_sessions", "theme_hubs_navigation", "theme_workspace_infrastructure"], "Live health monitor and top-level system status surface.", "documented", ["workspace-export-2026-03-27#03-ferrai-core-sessions"], ["dashboard", "health"])
    add("page_meine_notion_ki", "page", "Meine Notion-KI", ["theme_ferrai_core_sessions"], "Instruction and navigation page that acted as the library entry point for the workspace scan.", "documented", ["workspace-export-2026-03-27#03-ferrai-core-sessions"], ["navigation", "instructions"])
    add("page_ras_spezifikation", "page", "RAS Spezifikation", ["theme_architecture_specs"], "Recursive affinity storage specification for long-term contextual memory and pattern recognition.", "documented", ["workspace-export-2026-03-27#04-architektur-specs"], ["memory", "ras"])
    add("page_vortex_canvas", "page", "VortexCanvas", ["theme_architecture_specs", "theme_cic_theory"], "Five-dimensional decision engine spanning focus, identity, emotion, security and energy.", "documented", ["workspace-export-2026-03-27#04-architektur-specs"], ["decision-engine", "vortex"])
    add("page_audit_kernel_design_doc", "page", "Audit-Kernel Design-Doc", ["theme_architecture_specs", "theme_governance_details"], "Meta-Ferrum design page separating operative and audit power.", "documented", ["workspace-export-2026-03-27#04-architektur-specs", "workspace-export-2026-03-27#deep-extract"], ["audit", "meta-ferrum"])
    add("page_l3_build_plan", "page", "L3 Build-Plan canonical v1.0.0", ["theme_architecture_specs", "theme_integration_sync", "theme_security_blockchain_infra"], "Canonical build plan for IPFS, manifests, CID registry and repo skeleton.", "documented", ["workspace-export-2026-03-27#04-architektur-specs"], ["ipfs", "build-plan"])
    add("page_mermaid_atlas_start_here", "page", "Mermaid Atlas - Start Here", ["theme_mermaid_system"], "Entry page for the four canonical Mermaid perspectives: IST, SOLL, INTEGRATION and ORCHESTRATION.", "documented", ["workspace-export-2026-03-27#05-mermaid-system"], ["mermaid", "atlas"])
    add("page_terra_nova_master_overview", "page", "Terra Nova Master Overview", ["theme_mermaid_system", "theme_hubs_navigation"], "Workspace-scale overview page and canonical architecture map.", "documented", ["workspace-export-2026-03-27#05-mermaid-system", "workspace-export-2026-03-27#10-hubs-navigation"], ["mermaid", "overview"])
    add("page_mermaid_code_library", "page", "Mermaid Code Library", ["theme_mermaid_system"], "Central code library collecting Mermaid graphs, zoom views and agent slices.", "documented", ["workspace-export-2026-03-27#05-mermaid-system"], ["mermaid", "library"])
    add("page_mermaid_manifesto_public", "page", "Mermaid as a Living Trigger System - Manifesto v1.0", ["theme_mermaid_system", "theme_cic_theory"], "Public manifesto framing nodes as trigger entities, edges as activation conditions and graphs as living systems.", "documented", ["workspace-export-2026-03-27#05-mermaid-system", "workspace-export-2026-03-27#deep-extract"], ["mermaid", "manifesto"])
    add("page_schattenarchiv_hub", "page", "Schattenarchiv Hub", ["theme_shadow_archive_creative", "theme_security_blockchain_infra"], "Hub for shadow-work, Trigger 777 and deeper archival layers.", "documented", ["workspace-export-2026-03-27#06-schattenarchiv-kreativ"], ["shadow-archive", "security"])
    add("page_ponyverse_hub", "page", "PONYVERSE Hub", ["theme_shadow_archive_creative"], "Creative universe and play-layer hub tied to joy ignition and safety bars.", "documented", ["workspace-export-2026-03-27#06-schattenarchiv-kreativ"], ["creative", "ponyverse"])
    add("page_cap_ii_lizenz_system", "page", "CAP-II Lizenz-System", ["theme_token_blockchain", "theme_security_blockchain_infra"], "Three-tier licensing page with Solidity code, metadata schema and deployment plan.", "documented", ["workspace-export-2026-03-27#07-token-blockchain"], ["license", "solidity"])
    add("page_ferr_token", "page", "FERR Token", ["theme_token_blockchain", "theme_security_blockchain_infra"], "Live ERC-721 token on Polygon with wallet, royalty and Zora listing context.", "documented", ["workspace-export-2026-03-27#07-token-blockchain"], ["token", "polygon"])
    add("page_token_blockchain_system_index", "page", "Token and Blockchain System-Index", ["theme_token_blockchain", "theme_security_blockchain_infra"], "Index page connecting token infrastructure, contracts, databases, IPFS and DAO signals.", "documented", ["workspace-export-2026-03-27#07-token-blockchain"], ["token", "index"])
    add("page_notion_chatgpt_api_integration_setup", "page", "Notion-ChatGPT API-Integration Setup", ["theme_integration_sync", "theme_workspace_infrastructure"], "Core integration setup page for Notion to ChatGPT bridging.", "documented", ["workspace-export-2026-03-27#08-integration-sync"], ["integration", "api"])
    add("page_delta_sync_complete_guide", "page", "Delta-Sync Complete Guide", ["theme_integration_sync"], "Architecture, security, rollback, conflict resolution and testing guide for delta sync.", "documented", ["workspace-export-2026-03-27#08-integration-sync"], ["delta-sync", "guide"])
    add("page_investor_landing_interactive", "page", "Investor Landing Interactive", ["theme_gtm_investor_public"], "Interactive landing page for investor-facing positioning, status and 90-day roadmap.", "documented", ["workspace-export-2026-03-27#09-gtm-investor-public"], ["investor", "public"])
    add("page_faq_master", "page", "FAQ Master", ["theme_gtm_investor_public"], "Master FAQ covering CIC, DAO, token, products, pricing, security, use cases and glossary.", "documented", ["workspace-export-2026-03-27#09-gtm-investor-public"], ["faq", "public"])
    add("page_digital_ecosystem_hub", "page", "Digital Ecosystem Hub", ["theme_hubs_navigation", "theme_iperka_consolidation"], "Consolidation hub with target structure Mermaid, duplicate detection and phase plan.", "documented", ["workspace-export-2026-03-27#10-hubs-navigation", "workspace-export-2026-03-27#12-iperka-konsolidierung"], ["hub", "ecosystem"])
    add("page_master_dashboard", "page", "Master Dashboard", ["theme_hubs_navigation", "theme_workspace_infrastructure"], "Dashboard holding inline databases for metrics, component status and health.", "documented", ["workspace-export-2026-03-27#10-hubs-navigation"], ["dashboard", "operations"])
    add("page_prism_parent", "page", "Neuempfindung des Denkens - PRISM Parent", ["theme_prism_framework"], "Parent page for the PRISM corpus spanning chapters, appendix and evidence matrix.", "documented", ["workspace-export-2026-03-27#11-prism-framework"], ["prism", "parent"])
    add("page_prism_kapitel_5", "page", "PRISM Kapitel 5 Quantenphysik", ["theme_prism_framework", "theme_cic_theory"], "Heart chapter covering non-duality, desync, pre-thought, CIC and the FerrAI bridge.", "documented", ["workspace-export-2026-03-27#11-prism-framework"], ["prism", "quantum"])
    add("page_iperka_konsolidierung", "page", "IPERKA Konsolidierung Digital Ecosystem", ["theme_iperka_consolidation"], "Primary consolidation project page organizing Informieren through Auswerten.", "documented", ["workspace-export-2026-03-27#12-iperka-konsolidierung"], ["iperka", "consolidation"])
    add("page_tnpx_01_die_7_patente", "page", "TNPX-01 Die 7 Patente", ["theme_patents_ip"], "Portfolio page grouping the seven patent ideas and related dossiers.", "documented", ["workspace-export-2026-03-27#13-patente-ip"], ["patents", "portfolio"])
    add("page_10_master_prompts_v1", "page", "10 Master-Prompts v1.0", ["theme_products_services"], "Export-ready prompt product with launch kit and marketing assets.", "documented", ["workspace-export-2026-03-27#14-produkte-services"], ["product", "prompts"])
    add("page_cic_deep_dive", "page", "CIC Deep Dive", ["theme_cic_theory", "theme_ferrai_core_sessions"], "Core conceptual page for Cognitive Intelligent Cooperation and its conditions.", "documented", ["workspace-export-2026-03-27#15-cic-theorie"], ["cic", "theory"])
    add("page_compliance_datenschutz", "page", "Compliance und Datenschutz", ["theme_governance_details", "theme_security_blockchain_infra"], "Legal and AI-act-oriented compliance page with AI compliance register and incident tracking references.", "documented", ["workspace-export-2026-03-27#governance-compliance"], ["compliance", "legal"])
    add("page_archive_grundstruktur", "page", "Archive Grundstruktur", ["theme_hubs_navigation", "theme_archive_legacy"], "Locked archive base structure with canonical 10-folder framing.", "documented", ["workspace-export-2026-03-27#10-hubs-navigation", "workspace-export-2026-03-27#20-archive-legacy"], ["archive", "structure"])
    add("page_archive_legacy_hub", "page", "Archive Legacy Hub", ["theme_hubs_navigation", "theme_archive_legacy"], "Historical structure hub for legacy system and documentation branches.", "documented", ["workspace-export-2026-03-27#10-hubs-navigation", "workspace-export-2026-03-27#20-archive-legacy"], ["archive", "legacy"])

    add("db_archive_grundstruktur", "database", "Archive Grundstruktur DB", ["theme_hubs_navigation", "theme_archive_legacy"], "Database backing the locked 10-folder archive structure (data-source-89).", "identified", ["workspace-export-2026-03-27#10-hubs-navigation"], ["database", "archive"])
    add("db_master_overview_mermaid", "database", "Terra Nova Master Overview DB", ["theme_mermaid_system", "theme_hubs_navigation"], "Mermaid master overview database entry used as canonical architecture slice (data-source-288).", "identified", ["workspace-export-2026-03-27#05-mermaid-system"], ["database", "mermaid"])
    add("db_system_health_monitor", "database", "System Health Monitor", ["theme_ferrai_core_sessions", "theme_hubs_navigation", "theme_workspace_infrastructure"], "Health monitor inline database surfaced in dashboards.", "identified", ["workspace-export-2026-03-27#10-hubs-navigation"], ["database", "health"])
    add("db_system_komponenten_status", "database", "System Komponenten Status", ["theme_ferrai_core_sessions", "theme_hubs_navigation", "theme_workspace_infrastructure"], "Component-status inline database for system modules.", "identified", ["workspace-export-2026-03-27#10-hubs-navigation"], ["database", "components"])
    add("db_system_metrics", "database", "Terra Nova System Metrics", ["theme_ferrai_core_sessions", "theme_hubs_navigation", "theme_workspace_infrastructure"], "Metrics inline database for operational KPIs and counts.", "identified", ["workspace-export-2026-03-27#10-hubs-navigation"], ["database", "metrics"])
    add("db_promille_steuerung", "database", "1001 Promille Steuerung", ["theme_architecture_specs", "theme_trigger_system"], "Wiki-style database describing page, owner, tags and verification for promille control.", "identified", ["workspace-export-2026-03-27#04-architektur-specs"], ["database", "promille"])
    add("db_outcome_matrix", "database", "Outcome-Matrix", ["theme_hubs_navigation", "theme_patents_ip"], "Patent ROI tracking database with seven patents and outcome scoring.", "identified", ["workspace-export-2026-03-27#10-hubs-navigation"], ["database", "patents"])
    add("db_hybrid_produkte", "database", "Hybrid-Produkte", ["theme_token_blockchain", "theme_products_services"], "Digital x physical product database used across token and product surfaces.", "identified", ["workspace-export-2026-03-27#07-token-blockchain", "workspace-export-2026-03-27#14-produkte-services"], ["database", "products"])
    add("db_ai_compliance_register", "database", "AI Compliance Register", ["theme_governance_details", "theme_security_blockchain_infra"], "Compliance register referenced from the legal and AI Act page.", "identified", ["workspace-export-2026-03-27#governance-compliance"], ["database", "compliance"])
    add("db_ai_incidents_and_changes", "database", "AI Incidents and Changes", ["theme_integration_sync", "theme_workspace_infrastructure"], "Existing production database used by the current Notion-to-GitHub sync workflow.", "active", ["repo-current-sync"], ["database", "sync", "production"])
    add("db_mermaid_diagrams_library", "database", "Mermaid Diagrams Code Library", ["theme_mermaid_system"], "Database entry collection for Mermaid code snippets and diagram metadata.", "identified", ["workspace-export-2026-03-27#05-mermaid-system"], ["database", "mermaid"])
    add("db_tokenvault", "database", "TokenVault DB", ["theme_token_blockchain", "theme_security_blockchain_infra"], "Token management and minting database referenced by the token system index.", "identified", ["workspace-export-2026-03-27#07-token-blockchain", "workspace-export-2026-03-27#deep-extract"], ["database", "token"])
    add("db_manifest_license", "database", "Manifest License DB", ["theme_token_blockchain", "theme_security_blockchain_infra"], "License and manifest linkage database used by CAP-II and L3 concepts.", "identified", ["workspace-export-2026-03-27#07-token-blockchain", "workspace-export-2026-03-27#04-architektur-specs"], ["database", "license"])
    add("db_trigger_mapping", "database", "Trigger Mapping DB", ["theme_trigger_system", "theme_token_blockchain"], "Database linking trigger IDs, mapping surfaces and audit suites.", "identified", ["workspace-export-2026-03-27#07-token-blockchain", "workspace-export-2026-03-27#02-trigger-system"], ["database", "trigger"])
    add("db_zip_index_master", "database", "ZIP Index Master", ["theme_token_blockchain", "theme_security_blockchain_infra", "theme_workspace_infrastructure"], "Hash registry database for bundles, zip metadata and integrity tracking.", "identified", ["workspace-export-2026-03-27#07-token-blockchain", "workspace-export-2026-03-27#04-architektur-specs"], ["database", "integrity"])
    add("db_session_audit_log", "database", "Session Audit Log DB", ["theme_token_blockchain", "theme_integration_sync", "theme_workspace_infrastructure"], "Audit trail database tied to sessions, hashes and bundle history.", "identified", ["workspace-export-2026-03-27#07-token-blockchain", "workspace-export-2026-03-27#deep-extract"], ["database", "audit"])
    add("trigger_cluster_codex_1_170", "trigger_cluster", "Codex Trigger Cluster 1-170", ["theme_trigger_system", "theme_code_ethics"], "Fully named codex trigger range documented in Codex170_Plus_FINAL.", "documented", ["workspace-export-2026-03-27#deep-extract"], ["trigger", "codex"])
    add("trigger_cluster_silvi_mode_174_210", "trigger_cluster", "Silvi Mode Trigger Cluster 174-210", ["theme_trigger_system", "theme_code_ethics"], "Focused export range for Silvi mode and unlock-related safety nets.", "documented", ["workspace-export-2026-03-27#01-codex-ethik", "workspace-export-2026-03-27#deep-extract"], ["trigger", "silvi-mode"])
    add("trigger_cluster_core_session_516_544", "trigger_cluster", "Core Session Trigger Cluster 516-544", ["theme_trigger_system", "theme_cic_theory"], "Operational trigger band spanning inspiration, AutoFlow, SessionStart, Preflight and Synchronisationsknoten.", "documented", ["workspace-export-2026-03-27#02-trigger-system", "workspace-export-2026-03-27#deep-extract"], ["trigger", "session"])
    add("trigger_cluster_trigger_audit_675", "trigger_cluster", "Trigger Audit Cluster 675", ["theme_trigger_system"], "Audit-level cluster summarizing 675 documented triggers across categories.", "documented", ["workspace-export-2026-03-27#02-trigger-system"], ["trigger", "audit"])
    add("trigger_cluster_prism_551_600", "trigger_cluster", "PRISM Trigger Cluster 551-600", ["theme_trigger_system", "theme_prism_framework"], "Range documented in the PRISM appendix from Schwellenpunkt to MetaSwitch.", "documented", ["workspace-export-2026-03-27#02-trigger-system", "workspace-export-2026-03-27#11-prism-framework"], ["trigger", "prism"])
    add("trigger_cluster_audit_suite_988_992", "trigger_cluster", "Audit Suite Trigger Cluster 988-992", ["theme_trigger_system", "theme_security_blockchain_infra"], "Snapshot, token sync, audit engine, zip integrity and trigger echo suite.", "documented", ["workspace-export-2026-03-27#02-trigger-system", "workspace-export-2026-03-27#deep-extract"], ["trigger", "audit-suite"])
    add("trigger_cluster_emergent_approx_500", "trigger_cluster", "Emergent Trigger Cluster approx. 500", ["theme_trigger_system"], "Approximate emergent layer referenced as self-organizing triggers outside the fully named ranges.", "estimated", ["workspace-export-2026-03-27#deep-extract"], ["trigger", "emergent"])

    add("framework_cic", "framework", "CIC", ["theme_cic_theory", "theme_prism_framework"], "Cognitive Intelligent Cooperation as the core convergence model.", "documented", ["workspace-export-2026-03-27#15-cic-theorie", "workspace-export-2026-03-27#11-prism-framework"], ["framework", "cic"])
    add("framework_iperka", "framework", "IPERKA", ["theme_iperka_consolidation", "theme_architecture_specs"], "Informieren-Planen-Entscheiden-Realisieren-Kontrollieren-Auswerten loop adapted as a system process.", "documented", ["workspace-export-2026-03-27#12-iperka-konsolidierung", "workspace-export-2026-03-27#deep-extract"], ["framework", "planning"])
    add("framework_prism", "framework", "PRISM", ["theme_prism_framework", "theme_cic_theory"], "Main theory frame spanning mathematics, neural nets, cybernetics, quantum framing and appendix material.", "documented", ["workspace-export-2026-03-27#11-prism-framework"], ["framework", "theory"])
    add("framework_vortex", "framework", "VORTEX", ["theme_architecture_specs", "theme_cic_theory"], "Decision and state architecture connected to VortexCanvas and related control logic.", "documented", ["workspace-export-2026-03-27#04-architektur-specs", "workspace-export-2026-03-27#deep-extract"], ["framework", "decision-engine"])
    add("framework_ras", "framework", "RAS", ["theme_architecture_specs"], "Recursive affinity storage and effect-oriented memory model.", "documented", ["workspace-export-2026-03-27#04-architektur-specs", "workspace-export-2026-03-27#deep-extract"], ["framework", "memory"])
    add("framework_session_root", "framework", "SESSION_ROOT Framework", ["theme_trigger_system", "theme_ferrai_core_sessions", "theme_architecture_specs"], "15-module cognitive operating system for sessions and outputs.", "documented", ["workspace-export-2026-03-27#02-trigger-system", "workspace-export-2026-03-27#deep-extract"], ["framework", "session-root"])
    add("framework_meta_ferrum", "framework", "Meta-Ferrum", ["theme_architecture_specs", "theme_governance_details"], "Audit-kernel separation of operative and observing power.", "documented", ["workspace-export-2026-03-27#04-architektur-specs", "workspace-export-2026-03-27#deep-extract"], ["framework", "audit"])
    add("framework_desync_coherence", "framework", "Desync-Coherence", ["theme_cic_theory", "theme_iperka_consolidation"], "Theory that desynchronization is a feature and motor instead of a bug.", "documented", ["workspace-export-2026-03-27#deep-extract"], ["framework", "desync"])
    add("framework_abc_classification", "framework", "ABC Classification", ["theme_governance_details", "theme_code_ethics"], "A/B/C scoring model for criticality, room and process state.", "documented", ["workspace-export-2026-03-27#01-codex-ethik", "workspace-export-2026-03-27#deep-extract"], ["framework", "classification"])
    add("framework_ora", "framework", "ORA", ["theme_governance_details", "theme_code_ethics"], "Openness, radicality and authenticity filter.", "documented", ["workspace-export-2026-03-27#01-codex-ethik", "workspace-export-2026-03-27#deep-extract"], ["framework", "filter"])
    add("framework_triquetra", "framework", "Triquetra", ["theme_governance_details", "theme_code_ethics", "theme_security_blockchain_infra"], "Non-harm, consent and truth-with-tact safety stack.", "documented", ["workspace-export-2026-03-27#01-codex-ethik", "workspace-export-2026-03-27#deep-extract"], ["framework", "safety"])
    add("framework_schattenarchiv_777", "framework", "Schattenarchiv 777", ["theme_shadow_archive_creative", "theme_security_blockchain_infra"], "Nine-layer shadow archive model with deeper safety restrictions.", "documented", ["workspace-export-2026-03-27#04-architektur-specs", "workspace-export-2026-03-27#06-schattenarchiv-kreativ", "workspace-export-2026-03-27#deep-extract"], ["framework", "shadow-archive"])

    add("formula_non_duality_psi_nd", "formula", "Non-Duality Psi_ND", ["theme_cic_theory", "theme_prism_framework"], "Psi_ND = alpha*R + beta*A + gamma*Z with a gamma-squared threshold activating the in-between space.", "documented", ["workspace-export-2026-03-27#11-prism-framework", "workspace-export-2026-03-27#deep-extract"], ["formula", "non-duality"])
    add("formula_desync_gyro", "formula", "Desync Gyro", ["theme_cic_theory", "theme_prism_framework"], "dphi/dt = omega + epsilon_desync(t), used to express stable controlled desynchronization.", "documented", ["workspace-export-2026-03-27#11-prism-framework", "workspace-export-2026-03-27#deep-extract"], ["formula", "desync"])
    add("formula_vorgedanke_ratio", "formula", "Vorgedanke Ratio", ["theme_cic_theory", "theme_prism_framework"], "P(outcome|VG) / P(outcome|kein VG) > 1.5 as effectiveness threshold for pre-thought.", "documented", ["workspace-export-2026-03-27#15-cic-theorie", "workspace-export-2026-03-27#deep-extract"], ["formula", "pre-thought"])
    add("formula_osmose_flux", "formula", "Osmose Flux", ["theme_cic_theory", "theme_prism_framework"], "J = -D * dphi/dx used in bridge-oriented session transfer framing.", "documented", ["workspace-export-2026-03-27#11-prism-framework", "workspace-export-2026-03-27#deep-extract"], ["formula", "bridge"])
    add("formula_affinitaet_cosine", "formula", "Affinity Cosine Similarity", ["theme_cic_theory", "theme_architecture_specs"], "alpha(A,B) = <a,b> / (||a|| * ||b||) describing affinity as cosine similarity.", "documented", ["workspace-export-2026-03-27#11-prism-framework", "workspace-export-2026-03-27#deep-extract"], ["formula", "affinity"])
    add("formula_pid_controller", "formula", "PID Controller", ["theme_prism_framework", "theme_architecture_specs"], "u(t) = Kp*e(t) + Ki*integral(e(t))dt + Kd*de/dt, referenced via cybernetics and regulation loops.", "documented", ["workspace-export-2026-03-27#11-prism-framework", "workspace-export-2026-03-27#deep-extract"], ["formula", "control"])
    add("formula_hybrid_intelligence", "formula", "Hybrid Intelligence Psi", ["theme_cic_theory", "theme_prism_framework"], "Psi_hybrid = alpha*Psi_human + beta*Psi_AI + gamma*Psi_emergent.", "documented", ["workspace-export-2026-03-27#deep-extract"], ["formula", "hybrid-intelligence"])
    add("formula_coherence_function", "formula", "Coherence Function K", ["theme_cic_theory", "theme_prism_framework"], "K = f(trigger_density * session_stability), used as a conceptual coherence score.", "documented", ["workspace-export-2026-03-27#deep-extract"], ["formula", "coherence"])

    add("contract_ferr_erc721_polygon", "contract", "FERR ERC-721 on Polygon", ["theme_token_blockchain", "theme_security_blockchain_infra"], "Live ERC-721 contract for FERR on Polygon with wallet and royalty context.", "active", ["workspace-export-2026-03-27#07-token-blockchain", "workspace-export-2026-03-27#deep-extract"], ["contract", "polygon"])
    add("contract_cap_ii_license", "contract", "CAP-II License Contract", ["theme_token_blockchain", "theme_security_blockchain_infra"], "Three-tier licensing smart contract used for controlled access.", "specified", ["workspace-export-2026-03-27#07-token-blockchain", "workspace-export-2026-03-27#deep-extract"], ["contract", "license"])
    add("contract_cid_registry_polygon", "contract", "CID Registry Contract", ["theme_architecture_specs", "theme_token_blockchain", "theme_security_blockchain_infra"], "Polygon contract spec for artifact digest and CID registration.", "specified", ["workspace-export-2026-03-27#04-architektur-specs"], ["contract", "cid-registry"])

    add("product_prompt_framework", "product", "Prompt Framework", ["theme_products_services", "theme_gtm_investor_public"], "CHF 49 prompt product with 50+ pages and 20+ templates.", "marketed", ["workspace-export-2026-03-27#14-produkte-services", "workspace-export-2026-03-27#09-gtm-investor-public"], ["product", "prompt"])
    add("product_genesis_pass", "product", "Genesis Pass", ["theme_products_services"], "CHF 5,000 limited offer with five slots.", "marketed", ["workspace-export-2026-03-27#14-produkte-services"], ["product", "pass"])
    add("product_metarotik", "product", "Metarotik", ["theme_products_services", "theme_shadow_archive_creative"], "CHF 5,000 service layer connected to creative and intimate philosophy work.", "marketed", ["workspace-export-2026-03-27#06-schattenarchiv-kreativ", "workspace-export-2026-03-27#14-produkte-services"], ["product", "service"])
    add("product_master_prompts", "product", "10 Master-Prompts", ["theme_products_services"], "Prompt bundle framed as export-ready product and launch kit.", "marketed", ["workspace-export-2026-03-27#14-produkte-services"], ["product", "bundle"])
    add("patent_mindcode_tnpx_01", "patent", "MindCode TNPX-01", ["theme_patents_ip"], "Codex Gateway patent concept, filed in an early attempt in August 2025.", "documented", ["workspace-export-2026-03-27#13-patente-ip"], ["patent"])
    add("patent_tnav_tnpx_02", "patent", "TNAV TNPX-02", ["theme_patents_ip"], "Navigation patent concept in the TerraNova portfolio.", "documented", ["workspace-export-2026-03-27#13-patente-ip"], ["patent"])
    add("patent_kognitionsspiegel_tnpx_03", "patent", "Kognitionsspiegel TNPX-03", ["theme_patents_ip"], "Reflection-focused patent concept.", "documented", ["workspace-export-2026-03-27#13-patente-ip"], ["patent"])
    add("patent_einflusskoerper_tnpx_04", "patent", "Einflusskoerper TNPX-04", ["theme_patents_ip"], "Impact-oriented patent concept.", "documented", ["workspace-export-2026-03-27#13-patente-ip"], ["patent"])
    add("patent_codex_kern_tnpx_05", "patent", "Codex-Kern TNPX-05", ["theme_patents_ip"], "FerrAI Shield patent concept with the highest stated exploitation score in the seed export.", "documented", ["workspace-export-2026-03-27#13-patente-ip"], ["patent"])
    add("patent_vortex_tnpx_06", "patent", "VORTEX TNPX-06", ["theme_patents_ip"], "Decision-engine patent concept tied to VORTEX theory.", "documented", ["workspace-export-2026-03-27#13-patente-ip"], ["patent"])
    add("patent_msa_tnpx_07", "patent", "MSA TNPX-07", ["theme_patents_ip"], "Multi-system-architecture patent concept.", "documented", ["workspace-export-2026-03-27#13-patente-ip"], ["patent"])

    add("public_terra_nova_fusion", "public_domain", "terra-nova-fusion.notion.site", ["theme_gtm_investor_public"], "Public domain surface for fusion-oriented TerraNova content.", "active", ["workspace-export-2026-03-27#09-gtm-investor-public"], ["public-domain"])
    add("public_terra_nova_ki", "public_domain", "terra-nova-ki.notion.site", ["theme_gtm_investor_public"], "Public domain surface for German AI-related TerraNova material.", "active", ["workspace-export-2026-03-27#09-gtm-investor-public"], ["public-domain"])
    add("public_terra_nova_ai", "public_domain", "terra-nova-ai.notion.site", ["theme_gtm_investor_public"], "Public domain surface for AI-related TerraNova material.", "active", ["workspace-export-2026-03-27#09-gtm-investor-public"], ["public-domain"])
    add("public_terra_nova_gpt", "public_domain", "terra-nova-gpt.notion.site", ["theme_gtm_investor_public"], "Public domain surface for GPT-related TerraNova positioning.", "active", ["workspace-export-2026-03-27#09-gtm-investor-public"], ["public-domain"])
    add("public_terra_nova_restore", "public_domain", "terra-nova-restore.notion.site", ["theme_gtm_investor_public"], "Public domain surface for restore-facing TerraNova content.", "active", ["workspace-export-2026-03-27#09-gtm-investor-public"], ["public-domain"])

    add("agent_terranova_workspace_validator", "agent", "TerraNova Workspace Validator", ["theme_agents_tools", "theme_hubs_navigation"], "Meta-orchestrator agent used for workspace analysis and consolidation.", "documented", ["workspace-export-2026-03-27#17-agents-tools"], ["agent"])
    add("agent_mermaid_system_auditor", "agent", "Mermaid System Auditor", ["theme_agents_tools", "theme_mermaid_system"], "Diagram-focused agent for Mermaid auditing and related validation.", "documented", ["workspace-export-2026-03-27#05-mermaid-system", "workspace-export-2026-03-27#17-agents-tools"], ["agent"])
    add("agent_notion_ferrai", "agent", "Notion_FerrAI", ["theme_agents_tools", "theme_ferrai_core_sessions"], "Native Notion-side architect with broad workspace access.", "documented", ["workspace-export-2026-03-27#17-agents-tools"], ["agent"])
    add("agent_chatgpt_ferrai", "agent", "ChatGPT-FerrAI", ["theme_agents_tools", "theme_ferrai_core_sessions"], "External research and reflection counterpart in the FerrAI agent ecosystem.", "documented", ["workspace-export-2026-03-27#17-agents-tools"], ["agent"])
    add("agent_asana_ai", "agent", "Asana AI", ["theme_agents_tools"], "F&E project-management assistant referenced in the agent inventory.", "documented", ["workspace-export-2026-03-27#17-agents-tools"], ["agent"])

    relations = []

    def rel(src: str, dst: str, rel_type: str, note: str) -> None:
        relations.append({"from": src, "to": dst, "type": rel_type, "note": note})

    rel("page_codex170_plus_final", "trigger_cluster_codex_1_170", "contains", "Codex170 names the 1-170 trigger set.")
    rel("page_codex139_trigger_export_174_210", "trigger_cluster_silvi_mode_174_210", "contains", "Trigger export page is the seed source for the 174-210 range.")
    rel("page_trigger_architektur_520", "trigger_cluster_core_session_516_544", "contains", "Core session triggers sit inside the central trigger architecture.")
    rel("page_trigger_architektur_520", "trigger_cluster_audit_suite_988_992", "references", "Trigger architecture references the 988-992 audit suite.")
    rel("page_trigger_architektur_520", "trigger_cluster_emergent_approx_500", "references", "The architecture and audit describe a broader emergent trigger layer.")
    rel("page_trigger_audit_675", "trigger_cluster_trigger_audit_675", "contains", "Trigger-Audit 675 anchors the documented audit cluster.")
    rel("page_prism_parent", "page_prism_kapitel_5", "contains", "PRISM parent page contains the central chapter 5 branch.")
    rel("page_prism_parent", "trigger_cluster_prism_551_600", "contains", "PRISM appendix holds the 551-600 trigger list.")
    rel("page_prism_parent", "framework_prism", "contains", "PRISM parent is the main top-level document for the PRISM framework.")
    rel("page_session_root", "framework_session_root", "contains", "SESSION_ROOT page is the primary source of the session-root framework.")
    rel("page_audit_kernel_design_doc", "framework_meta_ferrum", "contains", "Audit-Kernel Design-Doc is the main Meta-Ferrum source.")
    rel("page_terranova_meta_index_v0_1", "framework_abc_classification", "contains", "META-INDEX holds the ABC classification.")
    rel("page_terranova_meta_index_v0_1", "framework_ora", "contains", "META-INDEX references ORA as a core governance lens.")
    rel("page_terranova_meta_index_v0_1", "framework_triquetra", "contains", "META-INDEX references Triquetra as a core safety stack.")
    rel("page_ras_spezifikation", "framework_ras", "contains", "RAS Spezifikation describes the RAS framework.")
    rel("page_vortex_canvas", "framework_vortex", "contains", "VortexCanvas is a page-level source for the VORTEX framework.")
    rel("page_schattenarchiv_hub", "framework_schattenarchiv_777", "contains", "Schattenarchiv hub is the main page source for the 777 framework.")
    rel("page_cic_deep_dive", "framework_cic", "contains", "CIC Deep Dive is a direct source for the CIC framework.")
    rel("page_iperka_konsolidierung", "framework_iperka", "contains", "IPERKA consolidation page names and organizes the IPERKA loop.")
    rel("page_mermaid_code_library", "db_mermaid_diagrams_library", "contains", "Mermaid Code Library is backed by a diagram database.")
    rel("page_master_dashboard", "db_system_health_monitor", "contains", "Master Dashboard surfaces the health monitor DB.")
    rel("page_master_dashboard", "db_system_komponenten_status", "contains", "Master Dashboard surfaces the component-status DB.")
    rel("page_master_dashboard", "db_system_metrics", "contains", "Master Dashboard surfaces the metrics DB.")
    rel("page_archive_grundstruktur", "db_archive_grundstruktur", "contains", "Archive Grundstruktur page is backed by the archive structure DB.")
    rel("page_token_blockchain_system_index", "db_tokenvault", "contains", "Token index references TokenVault.")
    rel("page_token_blockchain_system_index", "db_manifest_license", "contains", "Token index references manifest licensing data.")
    rel("page_token_blockchain_system_index", "db_trigger_mapping", "contains", "Token index references trigger mapping data.")
    rel("page_token_blockchain_system_index", "db_zip_index_master", "contains", "Token index references ZIP integrity data.")
    rel("page_token_blockchain_system_index", "db_session_audit_log", "contains", "Token index references session-level audit history.")
    rel("page_compliance_datenschutz", "db_ai_compliance_register", "contains", "Compliance page references the AI compliance register.")
    rel("page_notion_chatgpt_api_integration_setup", "db_ai_incidents_and_changes", "references", "Current repo sync uses AI Incidents and Changes as the production source DB.")
    rel("page_session_root", "framework_iperka", "references", "SESSION_ROOT embeds the IPERKA loop.")
    rel("page_session_root", "framework_desync_coherence", "references", "SESSION_ROOT documents desync-coherence as a core principle.")
    rel("page_session_root", "trigger_cluster_core_session_516_544", "references", "SESSION_ROOT aligns with the core session trigger band.")
    rel("page_prism_kapitel_5", "framework_cic", "references", "Chapter 5 explicitly covers CIC.")
    rel("page_prism_kapitel_5", "formula_non_duality_psi_nd", "references", "Chapter 5 contains the non-duality equation.")
    rel("page_prism_kapitel_5", "formula_desync_gyro", "references", "Chapter 5 contains the desync gyro expression.")
    rel("page_prism_kapitel_5", "formula_vorgedanke_ratio", "references", "Chapter 5 frames the pre-thought effect ratio.")
    rel("page_prism_kapitel_5", "formula_osmose_flux", "references", "Chapter 5 bridge notes use the osmose formula.")
    rel("framework_cic", "formula_non_duality_psi_nd", "depends_on", "CIC theory uses non-duality as one of its conditions.")
    rel("framework_cic", "formula_desync_gyro", "depends_on", "CIC theory depends on desync as a stabilizing mechanic.")
    rel("framework_cic", "formula_vorgedanke_ratio", "depends_on", "CIC theory depends on the pre-thought condition.")
    rel("framework_cic", "formula_affinitaet_cosine", "references", "Affinity is described as cosine similarity in the supporting material.")
    rel("framework_prism", "framework_cic", "references", "PRISM contains and formalizes CIC concepts.")
    rel("framework_prism", "formula_hybrid_intelligence", "references", "The deep extract attributes a hybrid-intelligence equation to PRISM-adjacent material.")
    rel("framework_prism", "formula_coherence_function", "references", "The deep extract attributes a conceptual coherence function to PRISM-adjacent material.")
    rel("framework_meta_ferrum", "framework_triquetra", "depends_on", "Meta-Ferrum escalation logic is safety-framed through Triquetra.")
    rel("framework_desync_coherence", "framework_session_root", "references", "Desync-coherence is operationalized through SESSION_ROOT.")
    rel("page_mermaid_manifesto_public", "framework_cic", "references", "Manifesto aligns living graphs with system dynamics and trigger logic.")
    rel("page_mermaid_manifesto_public", "trigger_cluster_core_session_516_544", "references", "Manifesto expresses trigger entities as graph nodes.")
    rel("page_mermaid_atlas_start_here", "page_terra_nova_master_overview", "references", "Atlas points to the master overview as the IST perspective.")
    rel("page_mermaid_atlas_start_here", "page_mermaid_manifesto_public", "references", "Atlas coexists with the public living-system manifesto.")
    rel("page_terra_nova_master_overview", "page_digital_ecosystem_hub", "mirrors", "Master Overview and Digital Ecosystem Hub both frame workspace structure from different angles.")
    rel("page_delta_sync_complete_guide", "page_notion_chatgpt_api_integration_setup", "depends_on", "Delta-Sync guide builds on the integration setup.")
    rel("page_delta_sync_complete_guide", "page_l3_build_plan", "references", "Delta-Sync architecture sits adjacent to the L3 build path.")
    rel("page_l3_build_plan", "contract_cid_registry_polygon", "depends_on", "L3 build plan relies on the CID registry concept.")
    rel("page_l3_build_plan", "db_zip_index_master", "depends_on", "L3 build plan needs bundle hash indexing.")
    rel("page_cap_ii_lizenz_system", "contract_cap_ii_license", "depends_on", "CAP-II page documents the CAP-II contract.")
    rel("page_ferr_token", "contract_ferr_erc721_polygon", "depends_on", "FERR token page refers to the live ERC-721 contract.")
    rel("page_token_blockchain_system_index", "contract_ferr_erc721_polygon", "references", "System index references the live FERR contract.")
    rel("page_token_blockchain_system_index", "contract_cap_ii_license", "references", "System index references CAP-II.")
    rel("page_token_blockchain_system_index", "contract_cid_registry_polygon", "references", "System index ties artifact integrity to CID registry concepts.")
    rel("trigger_cluster_audit_suite_988_992", "db_zip_index_master", "depends_on", "Integrity pulse and lockpoint concepts rely on bundle index data.")
    rel("trigger_cluster_audit_suite_988_992", "db_trigger_mapping", "depends_on", "Trigger echo and mapping rely on trigger mapping data.")
    rel("page_tnpx_01_die_7_patente", "patent_mindcode_tnpx_01", "contains", "Portfolio page lists patent 1.")
    rel("page_tnpx_01_die_7_patente", "patent_tnav_tnpx_02", "contains", "Portfolio page lists patent 2.")
    rel("page_tnpx_01_die_7_patente", "patent_kognitionsspiegel_tnpx_03", "contains", "Portfolio page lists patent 3.")
    rel("page_tnpx_01_die_7_patente", "patent_einflusskoerper_tnpx_04", "contains", "Portfolio page lists patent 4.")
    rel("page_tnpx_01_die_7_patente", "patent_codex_kern_tnpx_05", "contains", "Portfolio page lists patent 5.")
    rel("page_tnpx_01_die_7_patente", "patent_vortex_tnpx_06", "contains", "Portfolio page lists patent 6.")
    rel("page_tnpx_01_die_7_patente", "patent_msa_tnpx_07", "contains", "Portfolio page lists patent 7.")
    rel("db_outcome_matrix", "patent_codex_kern_tnpx_05", "references", "Outcome matrix names patent 5 as the highest-value item.")
    rel("page_10_master_prompts_v1", "product_master_prompts", "contains", "Page is the product surface for the 10 Master-Prompts bundle.")
    rel("page_10_master_prompts_v1", "product_prompt_framework", "references", "Prompt product surfaces are related in the GTM layer.")
    rel("page_ponyverse_hub", "product_metarotik", "references", "Creative layer overlaps with the Metarotik service surface.")
    rel("db_hybrid_produkte", "product_genesis_pass", "references", "Hybrid products catalog can contain Genesis Pass-related artifacts.")
    rel("db_hybrid_produkte", "product_metarotik", "references", "Hybrid products catalog can contain Metarotik-related artifacts.")
    rel("page_investor_landing_interactive", "page_faq_master", "references", "Investor landing sits alongside the master FAQ.")
    rel("page_investor_landing_interactive", "page_token_blockchain_system_index", "references", "Investor landing surfaces token, DAO and patent status.")
    rel("page_investor_landing_interactive", "page_prism_parent", "references", "Investor narrative references the theoretical foundation.")
    rel("page_investor_landing_interactive", "public_terra_nova_fusion", "publishes_to", "Investor-facing material is part of the public Notion surface.")
    rel("page_investor_landing_interactive", "public_terra_nova_ai", "publishes_to", "Investor-facing material can route into the public AI domain.")
    rel("page_faq_master", "public_terra_nova_ki", "publishes_to", "FAQ material supports the German public domain.")
    rel("page_faq_master", "public_terra_nova_gpt", "publishes_to", "FAQ material supports GPT-facing public messaging.")
    rel("page_faq_master", "public_terra_nova_restore", "publishes_to", "FAQ material supports restore-facing public messaging.")
    rel("agent_terranova_workspace_validator", "page_terra_nova_master_overview", "references", "Validator uses workspace overview pages as orientation surfaces.")
    rel("agent_terranova_workspace_validator", "page_iperka_konsolidierung", "references", "Validator is tied to the consolidation workflow.")
    rel("agent_terranova_workspace_validator", "page_ferrai_agent_config_control_center", "references", "Validator depends on the agent config control center.")
    rel("agent_mermaid_system_auditor", "page_mermaid_code_library", "depends_on", "Mermaid auditor works against the code library.")
    rel("agent_notion_ferrai", "page_meine_notion_ki", "depends_on", "Notion_FerrAI uses the instruction page as a base anchor.")
    rel("agent_notion_ferrai", "page_ferrai_systemhandbuch", "references", "Notion_FerrAI aligns with the FerrAI handbook.")
    rel("agent_chatgpt_ferrai", "page_ferrai_reflexions_log", "references", "ChatGPT-FerrAI references long-form reflection and continuity notes.")
    rel("agent_asana_ai", "page_iperka_konsolidierung", "references", "Asana AI is linked to research and development project management.")
    rel("page_archive_legacy_hub", "page_archive_grundstruktur", "mirrors", "Legacy and canonical archive structures coexist in the seed export.")

    open_gaps = [
        {"id": "gap_unknown_blocks_trigger_audit_675", "title": "Unknown blocks in Trigger-Audit 675", "description": "Approx. 400 blocks in the Trigger-Audit page were described as non-renderable by the Notion API and should be treated as representation limits, not missing trigger content.", "status": "open", "source_refs": ["workspace-export-2026-03-27#deep-extract"]},
        {"id": "gap_unknown_blocks_reflexions_log", "title": "Unknown blocks in FerrAI Reflexions-Log", "description": "Large parts of the Reflexions-Log were reported as unknown block types during prior scans, so v1 stores the page as a seeded object without full block-level expansion.", "status": "open", "source_refs": ["workspace-export-2026-03-27#deep-extract"]},
        {"id": "gap_trigger_range_171_505", "title": "Underdocumented trigger range 171-505", "description": "The deep extract called out a broad gap between Codex 1-170 and the later named system clusters, so v1 represents this as an open knowledge gap rather than fabricated objects.", "status": "open", "source_refs": ["workspace-export-2026-03-27#deep-extract"]},
        {"id": "gap_subpage_full_depth_v2", "title": "Full subpage depth deferred to v2", "description": "The seed export referenced roughly 500 sub-pages and cross-links, but Atlas v1 deliberately captures only themes plus main objects and selected cross-links.", "status": "accepted", "source_refs": ["workspace-export-2026-03-27#workspace-tree"]},
        {"id": "gap_live_notion_export_pipeline", "title": "Live Notion export pipeline not attached yet", "description": "This repo now seeds a canonical atlas, but no live Notion workspace-exporter has been connected to refresh atlas data automatically.", "status": "planned", "source_refs": ["repo-current-sync", "workspace-export-2026-03-27"]},
    ]

    for theme in themes:
        theme["object_ids"] = []
    theme_by_id = {theme["id"]: theme for theme in themes}
    for obj in objects:
        for theme_id in obj["theme_ids"]:
            theme_by_id[theme_id]["object_ids"].append(obj["id"])
    for theme in themes:
        theme["object_ids"] = sorted(theme["object_ids"])

    objects.sort(key=lambda item: (item["kind"], item["title"].lower(), item["id"]))
    relations.sort(key=lambda item: (item["from"], item["type"], item["to"]))
    kind_counts = Counter(obj["kind"] for obj in objects)

    stats = {
        "theme_count": len(themes),
        "object_count": len(objects),
        "relation_count": len(relations),
        "open_gap_count": len(open_gaps),
        "objects_by_kind": dict(sorted(kind_counts.items())),
        "estimates": {"workspace_main_pages": 85, "workspace_pages_via_api": 323, "workspace_total_page_range": "400-600", "workspace_subpages_and_crossrefs": "500+", "active_databases_estimate": "15+", "files_estimate": "1750+", "ipfs_cids": 39, "documented_triggers": 675, "defined_triggers_estimate": "1200+"},
        "coverage": {"atlas_scope": "themes-plus-main-objects", "source_mode": "manual-seed-from-workspace-export", "live_notion_scan_attached": False, "full_subpage_expansion": False, "production_sync_unchanged": True},
    }

    return {
        "workspace": {"name": "Terra'Nova_FerrAI_CIC", "atlas_id": "terranova-atlas-v1", "repo_role": "canonical atlas seed beside the production Notion-to-GitHub sync", "primary_language": "de-CH with mixed English technical terms", "created_for_repo": "TerraNova-s-Framework"},
        "source": {"id": "workspace-export-2026-03-27", "type": "user-provided workspace export and validator transcript", "captured_at": "2026-03-27", "ingested_at": "2026-03-30", "notes": ["Primary seed comes from the user-provided TerraNova Workspace Validator transcript pasted into Codex.", "The repo itself currently models a single production sync database and does not yet mirror the whole workspace taxonomy.", "Atlas v1 is intentionally seeded manually but shaped for future exporter automation."]},
        "stats": stats,
        "themes": themes,
        "objects": objects,
        "relations": relations,
        "open_gaps": open_gaps,
    }


def build_readme(manifest: dict) -> str:
    kinds = manifest["stats"]["objects_by_kind"]
    kind_lines = "\n".join([f"| `{kind}` | {count} |" for kind, count in kinds.items()])
    theme_lines = "\n".join([f"| `{theme['id']}` | {theme['title']} | {theme['priority']} | {len(theme['object_ids'])} |" for theme in manifest["themes"]])
    return f"""# TerraNova Atlas v1

This directory adds a second, non-invasive layer to the repo:

1. The existing production layer still syncs one Notion database into GitHub Issues.
2. The new atlas layer stores a canonical, machine-readable snapshot of the broader TerraNova workspace model.

## Scope

Atlas v1 is intentionally scoped to themes plus main objects.
It does not attempt a full live mirror of the Notion workspace.
The seed comes from the user-provided TerraNova Workspace Validator export dated 2026-03-27.

## Folder layout

```text
atlas/
  README.md
  atlas.manifest.v1.json
  sources/
    workspace-export-2026-03-27.md
```

## Top-level model

The manifest exposes the following top-level sections:

- `workspace`
- `source`
- `stats`
- `themes`
- `objects`
- `relations`
- `open_gaps`

## Current coverage

- Themes: {manifest['stats']['theme_count']}
- Objects: {manifest['stats']['object_count']}
- Relations: {manifest['stats']['relation_count']}
- Open gaps: {manifest['stats']['open_gap_count']}
- Documented trigger estimate in source: 675
- Defined trigger estimate in source: 1200+
- Main page estimate in source: 85
- Sub-page and cross-reference estimate in source: 500+

## Object kinds

| Kind | Count |
| --- | ---: |
{kind_lines}

## Themes

| Theme ID | Title | Priority | Objects |
| --- | --- | --- | ---: |
{theme_lines}

## Design notes

- The atlas keeps the current `AI Incidents and Changes` production sync separate.
- Unknown blocks from prior workspace scans are represented as gaps, not as missing or fabricated content.
- Trigger ranges that were described but not fully documented remain explicit gaps instead of guessed objects.
- Theme membership is intentionally many-to-many so pages, frameworks and databases can be anchored in more than one domain.

## Trigger framing in v1

Atlas v1 keeps triggers at cluster level rather than forcing every trigger ID into its own object.
The main clusters currently represented are:

- Codex 1-170
- Silvi mode 174-210
- Core session 516-544
- Trigger audit 675
- PRISM appendix 551-600
- Audit suite 988-992
- Emergent approx. 500

## Validation

Run the passive validator from the repo root:

```bash
python scripts/validate_atlas.py atlas/atlas.manifest.v1.json
```

The validator checks:

- required top-level keys
- unique IDs
- allowed object kinds
- relation endpoints
- theme/object membership consistency
- stat counters against manifest contents

## What v1 does not do

- no live Notion crawl
- no automatic export of the full workspace
- no full 500+ sub-page expansion
- no changes to the current sync workflow, secrets or mappings

## Next-step friendly by design

The manifest shape is intentionally stable enough for a future exporter.
A later pipeline can append or refresh objects from Notion without breaking the current repo contract.
"""


def build_source_markdown() -> str:
    return """# Workspace Export Seed (2026-03-27)

This file stores the human source context that seeded `atlas.manifest.v1.json`.
It is not a live export from Notion.
It is a normalized source capture based on the user-provided TerraNova Workspace Validator transcript pasted into Codex on 2026-03-30.

## Provenance

- Source type: user-provided workspace export / validator transcript
- Original context date inside the export: 2026-03-27
- Repo ingestion date: 2026-03-30
- Role in repo: seed source for Atlas v1

## Canonical workspace tree excerpt

```text
TERRA NOVA WORKSPACE (Root)
|
|-- 01. CODEX AND ETHIK
|   |-- Codex170_Plus_FINAL
|   |-- Codex139+ TriggerExport 174-210
|   |-- Meta-Conductor
|   |-- TERRANOVA META-INDEX v0.1
|   |-- ABLAGESYSTEM
|   `-- Instanzenrat-System
|
|-- 02. TRIGGER-SYSTEM
|   |-- Trigger-Architektur 520
|   |-- Trigger-Audit 675
|   |-- Trigger-Zeichen Referenz
|   |-- Triggerliste 551-600
|   |-- Workspace-Kohaerenz Protokoll
|   |-- Trigger-Mapping and Cross-Reference
|   `-- SESSION_ROOT
|
|-- 03. FERRAI CORE AND SESSIONS
|   |-- FerrAI Systemhandbuch
|   |-- FerrAI Reflexions-Log
|   |-- FerrAI Agent-Config Control Center
|   |-- System Status Dashboard
|   |-- Meine Notion-KI
|   |-- Systemkern Transfer-Essenz
|   |-- Kontext-Transfer -> Neuer Chat
|   `-- Workspace Context Sync
|
|-- 04. ARCHITEKTUR AND SPECS
|   |-- RAS Spezifikation
|   |-- VortexCanvas
|   |-- Schattenarchiv and 777-System
|   |-- Audit-Kernel Design-Doc
|   |-- L3 Build-Plan canonical v1.0.0
|   |-- 1001 Promille Steuerung
|   |-- Canon Dokument
|   |-- Master Control Framework
|   `-- System and Frameworks Hub
|
|-- 05. MERMAID-SYSTEM
|   |-- Mermaid Atlas - Start Here
|   |-- Terra Nova Master Overview
|   |-- Mermaid Code Library
|   |-- Manifesto v1.0 (Public Edition)
|   |-- Zoom 02 Codex and Trigger
|   |-- Zoom 05 Produkte and Services
|   |-- Zoom 06 Technische Doku
|   |-- TokenAccess TriggerMap 988-992
|   `-- Mermaid System Auditor
|
|-- 06. SCHATTENARCHIV AND KREATIV
|   |-- Schattenarchiv Hub
|   |-- PONYVERSE Hub
|   |-- Metarotik
|   |-- VelvetSquirt
|   `-- Persoenliche Reflexionen
|
|-- 07. TOKEN AND BLOCKCHAIN
|   |-- CAP-II Lizenz-System
|   |-- FERR Token
|   |-- DAO-Struktur
|   |-- Tokenomics
|   |-- Token and Blockchain System-Index
|   `-- Hybrid-Produkte DB
|
|-- 08. INTEGRATION AND SYNC
|   |-- Notion-ChatGPT API-Integration Setup
|   |-- Notion AI-ChatGPT Sync-Hub
|   |-- Delta-Sync Script v1.0
|   |-- Delta-Sync Complete Guide
|   |-- System Context Fullsync
|   |-- FullSync Import v1
|   |-- API-Integration Action-List
|   `-- Deploy FullSync Sequence
|
|-- 09. GTM / INVESTOR / PUBLIC
|   |-- Investor Landing Interactive
|   |-- FAQ Master
|   |-- AI Landscape
|   `-- Public Notion Domains
|
|-- 10. HUBS AND NAVIGATION
|   |-- Digital Ecosystem Hub
|   |-- Master Dashboard
|   |-- Audit-Log v1.0
|   |-- Outcome-Matrix Template
|   |-- Archive Grundstruktur
|   |-- Archive Legacy Hub
|   `-- Pegasus Notion
|
|-- 11. PRISM FRAMEWORK
|   |-- Neuempfindung des Denkens - PRISM Parent
|   |-- Kapitel 1-4
|   |-- Kapitel 5 Quantenphysik
|   |-- Kapitel 6-10
|   |-- Anhang A.1-A.12
|   |-- Terminologie-Normblatt
|   `-- Claim-to-Evidence-Matrix
|
|-- 12. IPERKA AND KONSOLIDIERUNG
|   |-- IPERKA Konsolidierung Digital Ecosystem
|   `-- Konsolidierungs-Plan Phase 1-3
|
|-- 13. PATENTE AND IP
|   `-- 7 Patentlinien von MindCode bis MSA
|
|-- 14. PRODUKTE AND SERVICES
|   |-- 10 Master-Prompts v1.0
|   |-- Metarotik
|   |-- Genesis Pass
|   |-- Prompt Framework
|   `-- Hybrid-Produkte DB
|
|-- 15. CIC-THEORIE
|   |-- Nicht-Dualitaet
|   |-- DE-Sync / Gyroskop
|   |-- Vorgedanke / Pre-Thought
|   `-- Mensch-KI Verschraenkung
|
|-- 16. WORKSPACE-INFRASTRUKTUR
|   |-- API integration id
|   |-- 323 pages via API
|   |-- 400-600 estimated total pages
|   |-- 1750+ files
|   |-- 15+ active databases
|   `-- 39 IPFS CIDs
|
|-- 17. AGENTS AND TOOLS
|   |-- TerraNova Workspace Validator
|   |-- Mermaid System Auditor
|   |-- Notion_FerrAI
|   |-- ChatGPT-FerrAI
|   `-- Asana AI
|
|-- 18. GOVERNANCE-DETAILS
|   |-- 4-layer workspace architecture
|   |-- Koexistenzprinzip DECISION_GMv1_009
|   `-- Working rules and communication rules
|
|-- 19. SECURITY AND BLOCKCHAIN INFRA
|   |-- Wallet segmentation
|   |-- IPFS gateway fallbacks
|   |-- Security doctrine
|   `-- Audit trail: tx-hash + cid + zip + sha-256 + Schattenarchiv 777
|
`-- 20. ARCHIVE AND LEGACY
    |-- Archive Grundstruktur DB
    |-- Archive Legacy Hub
    `-- Rohdateien-Inventar
```

## Key extraction notes used by Atlas v1

### Unknown blocks are representation limits

The transcript explicitly reframed large `unknown block` counts as an API-rendering limitation.
Atlas v1 therefore stores these as open gaps rather than inventing missing page content.

Examples called out in the transcript:

- Trigger-Audit 675: approx. 400 unknown blocks
- FerrAI Reflexions-Log: approx. 600 unknown blocks

### Trigger framing used for v1

The transcript exposed the following clusters as the most stable trigger anchors for a first atlas version:

- Codex 1-170
- Silvi mode 174-210
- Core session 516 / 517 / 520 / 521 / 540 / 544 / 777
- PRISM appendix 551-600
- Audit suite 988-992
- Approx. 500 emergent triggers

It also called out an underdocumented gap between 171 and 505.
Atlas v1 keeps that gap explicit instead of guessing object records.

### Publishable documents explicitly highlighted in the transcript

The prior workspace scan identified several documents as already close to publication or direct reuse:

- SESSION_ROOT v1.0
- Meta-Ferrum / Audit-Kernel Design-Doc
- Entscheidungsmembranen concept
- Desync-Coherence theory
- PRISM chapter 5
- Mermaid as a Living Trigger System manifesto
- Investor Landing Interactive

### Numerical signals used by Atlas v1

The transcript repeatedly referenced the following signals:

- approx. 85 main pages
- approx. 500+ sub-pages / cross-references
- 323 pages via API
- approx. 400-600 total pages in workspace
- 15+ active databases
- 1750+ files
- 39 IPFS CIDs
- 675 documented triggers
- 1200+ defined triggers

These numbers are preserved as seed estimates in the manifest rather than asserted as live repo truth.
"""


def write_files() -> None:
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest()
    (ATLAS_DIR / "atlas.manifest.v1.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    (ATLAS_DIR / "README.md").write_text(build_readme(manifest), encoding="utf-8")
    (SOURCES_DIR / "workspace-export-2026-03-27.md").write_text(build_source_markdown(), encoding="utf-8")


if __name__ == "__main__":
    write_files()
