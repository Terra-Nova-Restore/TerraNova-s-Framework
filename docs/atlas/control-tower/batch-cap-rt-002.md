# CAP-RT-002 - Control Tower Dashboard View Package

Status: planned on 2026-05-18
Date: 2026-05-18
Parent gate: `CAP-RT-001`
Mutation policy: GitHub trace only. No Notion mutation performed in this PR.

## Purpose
Executes CAP-RT-ACT-01, ACT-02, and ACT-03 from the CAP-RT-001 action queue.

## Decisions
1. **Visible runtime surface**: The Notion Dashboard is chosen as the primary surface (No external app prototype yet).
2. **Registry Mapping**: Mapped `canon_level`, `source_class`, and `review_status` to Notion status/select properties.
3. **View Package**: Defined a Notion-safe View Package that uses standard views without relying on Notion Custom Agents or the Notion SQL Query Tool.
