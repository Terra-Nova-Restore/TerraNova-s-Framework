# CAP-RT-001 - Control Tower Runtime Planning

Status: repo-local plan created on 2026-05-18
Date: 2026-05-18
Parent gate: `PR-048-REVIEW-DECISION`
Mutation policy: GitHub trace only. No Notion mutation, no Zenodo mutation and
no Notion AI credit use.

## Purpose

`CAP-RT-001` defines the first runtime contract for the Control Tower after PR
#48 was merged.

Runtime does not mean autonomous Notion agency. Runtime means a repeatable
control loop that can route work across Notion, GitHub and Zenodo without
losing source authority, boundary state or causal trace.

## Runtime Definition

The Control Tower runtime is the operational layer that answers five questions
before work expands:

1. What is the current object or lane?
2. Which system is the source of record?
3. Which claims are allowed, blocked or unverified?
4. Which gate decides the next action?
5. Where is the feedback written?

## Runtime Loop

```plain text
Intake
-> Source routing
-> Boundary check
-> Gate selection
-> Small action
-> Validation
-> Feedback trace
```

This loop is intentionally smaller than a full autonomous agent. It is designed
for human/Codex cooperation, GPT-assisted synthesis and Copilot-assisted
mechanical edits while avoiding Notion Custom Agents and credit-consuming
automation.

## Dashboard Contract

The dashboard must expose these runtime surfaces:

- Active gate
- Source of record
- Current lane
- Canon level
- Sensitivity state
- Allowed claims
- Blocked claims
- Next source action
- GitHub trace
- Zenodo/live-source state when relevant

The first implementation target is not a polished application. It is a
workspace-control dashboard that can survive interrupted sessions and resume
without reconstructing the whole thread.

## No-Credit Policy

Allowed:

- Notion manual review and narrow search/fetch through the connector
- repo-local manifests, CSVs and causal logs
- GPT for bounded synthesis against supplied excerpts
- GitHub Copilot for mechanical edits
- live Zenodo API reads for public release verification

Blocked by default:

- Notion Custom Agents
- scheduled Notion AI runs
- database-wide Notion AI autofill
- mass summarization of all pages
- Zenodo writes or workflow dispatch
- raw private Notion IDs in public GitHub trace

## Deliverables

Created in this gate:

```plain text
docs/atlas/control-tower/cap-rt-001.runtime-contract.md
docs/atlas/control-tower/cap-rt-001.bedienungshandbuch.md
docs/atlas/control-tower/cap-rt-001.dashboard-lanes.csv
docs/atlas/control-tower/cap-rt-001.source-routing.csv
docs/atlas/control-tower/cap-rt-001.guardrails.csv
docs/atlas/control-tower/cap-rt-001.action-queue.csv
docs/atlas/control-tower/cap-rt-001.review-summary.json
docs/atlas/control-tower/causal-log.cap-rt-001-plan-2026-05-18.json
```

## Decision

`CAP-RT-001` is a planning gate only.

Next best action:

```plain text
CAP-RT-002
```

`CAP-RT-002` should create the first dashboard skeleton or Notion-facing view
package, but only after deciding whether the first visible runtime surface
lives primarily in Notion, GitHub Markdown, or a small local dashboard.
