# TerraNova Atlas v1

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

- Themes: 20
- Objects: 111
- Relations: 94
- Open gaps: 5
- Documented trigger estimate in source: 675
- Defined trigger estimate in source: 1200+
- Main page estimate in source: 85
- Sub-page and cross-reference estimate in source: 500+

## Object kinds

| Kind | Count |
| --- | ---: |
| `agent` | 5 |
| `contract` | 3 |
| `database` | 16 |
| `formula` | 8 |
| `framework` | 12 |
| `page` | 44 |
| `patent` | 7 |
| `product` | 4 |
| `public_domain` | 5 |
| `trigger_cluster` | 7 |

## Themes

| Theme ID | Title | Priority | Objects |
| --- | --- | --- | ---: |
| `theme_code_ethics` | CodeX and Ethics | critical | 11 |
| `theme_trigger_system` | Trigger System | critical | 16 |
| `theme_ferrai_core_sessions` | FerrAI Core and Sessions | critical | 13 |
| `theme_architecture_specs` | Architecture and Specs | critical | 14 |
| `theme_mermaid_system` | Mermaid System | high | 7 |
| `theme_shadow_archive_creative` | Shadow Archive and Creative | high | 4 |
| `theme_token_blockchain` | Token and Blockchain | high | 12 |
| `theme_integration_sync` | Integration and Sync | high | 5 |
| `theme_gtm_investor_public` | GTM, Investor and Public | high | 8 |
| `theme_hubs_navigation` | Hubs, Navigation and Dashboards | high | 13 |
| `theme_prism_framework` | PRISM Framework | high | 12 |
| `theme_iperka_consolidation` | IPERKA and Consolidation | high | 4 |
| `theme_patents_ip` | Patents and IP | medium | 9 |
| `theme_products_services` | Products and Services | medium | 6 |
| `theme_cic_theory` | CIC Theory | high | 17 |
| `theme_workspace_infrastructure` | Workspace Infrastructure | medium | 10 |
| `theme_agents_tools` | Agents and Tools | medium | 7 |
| `theme_governance_details` | Governance Details | high | 10 |
| `theme_security_blockchain_infra` | Security and Blockchain Infra | high | 16 |
| `theme_archive_legacy` | Archive and Legacy | medium | 7 |

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
