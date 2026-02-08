#!/usr/bin/env python3
"""
TerraNova – Notion -> GitHub Controller (minimal, audit-friendly)

Core:
- Poll a Notion database (e.g., AI_Incidents_and_Changes)
- For rows marked Export_to_GitHub == true and missing GitHub_Issue_URL:
  - Create a GitHub Issue
  - (Optional) Add that Issue to a GitHub Project (Projects v2)
  - (Optional) Set Project Status field (e.g., Todo/In Progress/Done)
  - Write back Issue URL + timestamp to Notion

Security:
- NO tokens in code.
- Use environment variables and GitHub repository Secrets.

Required env vars:
  NOTION_TOKEN
  NOTION_DATABASE_ID_CHANGES
  GITHUB_TOKEN
  GITHUB_REPO                 # "owner/repo"

Optional env vars:
  NOTION_VERSION              # default: "2022-06-28"
  GITHUB_API                  # default: "https://api.github.com"
  DRY_RUN                     # "1" to not create issues / not write back
  PROJECTV2_ID                # GitHub ProjectV2 node id (e.g., "PVT_...")
  PROJECT_STATUS_FIELD_NAME   # default: "Status"
  PROJECT_STATUS_OPTION_NAME  # default: "Todo"

Notes:
- Your GitHub token must have permission to:
  - create issues in the repo
  - read/write Projects v2 (if PROJECTV2_ID is set)
"""

import os
import sys
import time
import json
import requests
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

NOTION_TOKEN = os.getenv("NOTION_TOKEN", "").strip()
NOTION_DB = os.getenv("NOTION_DATABASE_ID_CHANGES", "").strip()
NOTION_VERSION = os.getenv("NOTION_VERSION", "2022-06-28").strip()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()
GITHUB_REPO = os.getenv("GITHUB_REPO", "").strip()
GITHUB_API = os.getenv("GITHUB_API", "https://api.github.com").strip()

PROJECTV2_ID = os.getenv("PROJECTV2_ID", "").strip()
PROJECT_STATUS_FIELD_NAME = os.getenv("PROJECT_STATUS_FIELD_NAME", "Status").strip()
PROJECT_STATUS_OPTION_NAME = os.getenv("PROJECT_STATUS_OPTION_NAME", "Todo").strip()

DRY_RUN = os.getenv("DRY_RUN", "").strip() in ("1", "true", "TRUE", "yes", "YES")


def must_env(name: str, value: str) -> None:
    if not value:
        print(f"[FATAL] Missing env var: {name}", file=sys.stderr)
        sys.exit(2)


# ---- Notion helpers ----

def notion_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def safe_get_title(props: Dict[str, Any]) -> str:
    for _, v in props.items():
        if isinstance(v, dict) and v.get("type") == "title":
            chunks = v.get("title", [])
            return "".join(c.get("plain_text", "") for c in chunks).strip() or "(untitled)"
    return "(untitled)"


def safe_get_richtext(props: Dict[str, Any], key: str) -> str:
    v = props.get(key, {})
    if not isinstance(v, dict):
        return ""
    t = v.get("type")
    if t == "rich_text":
        return "".join(c.get("plain_text", "") for c in v.get("rich_text", [])).strip()
    if t == "url":
        return (v.get("url") or "").strip()
    if t == "select":
        sel = v.get("select")
        return (sel.get("name") if sel else "").strip()
    if t == "checkbox":
        return str(bool(v.get("checkbox")))
    return ""


def notion_query_database(db_id: str, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Auto-paginated query."""
    results: List[Dict[str, Any]] = []
    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    data = payload.copy()
    while True:
        r = requests.post(url, headers=notion_headers(), json=data, timeout=60)
        if r.status_code >= 400:
            raise RuntimeError(f"Notion query failed: {r.status_code} {r.text}")
        j = r.json()
        results.extend(j.get("results", []))
        if not j.get("has_more"):
            break
        data["start_cursor"] = j.get("next_cursor")
        time.sleep(0.2)
    return results


def notion_update_page(page_id: str, properties: Dict[str, Any]) -> None:
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"properties": properties}
    if DRY_RUN:
        print("[DRY_RUN] Would update Notion page:", page_id)
        return
    r = requests.patch(url, headers=notion_headers(), json=payload, timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f"Notion update failed: {r.status_code} {r.text}")


# ---- GitHub helpers ----

def github_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "TerraNova-Notion2GitHub-Controller",
    }


def github_create_issue(repo: str, title: str, body: str, labels: Optional[List[str]] = None) -> Tuple[str, str]:
    """Returns (html_url, node_id)."""
    url = f"{GITHUB_API}/repos/{repo}/issues"
    payload: Dict[str, Any] = {"title": title, "body": body}
    if labels:
        payload["labels"] = labels
    if DRY_RUN:
        print("[DRY_RUN] Would create GitHub issue:", repo, title)
        return "https://example.invalid/issue/DRY_RUN", "NODE_ID_DRY_RUN"
    r = requests.post(url, headers=github_headers(), json=payload, timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f"GitHub issue create failed: {r.status_code} {r.text}")
    j = r.json()
    return j.get("html_url", ""), j.get("node_id", "")


def github_graphql(query: str, variables: dict) -> dict:
    url = f"{GITHUB_API}/graphql"
    if DRY_RUN:
        print("[DRY_RUN] Would call GitHub GraphQL.")
        return {}
    r = requests.post(url, headers=github_headers(), json={"query": query, "variables": variables}, timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f"GitHub GraphQL failed: {r.status_code} {r.text}")
    j = r.json()
    if "errors" in j and j["errors"]:
        raise RuntimeError(f"GitHub GraphQL errors: {j['errors']}")
    return j.get("data", {})


_project_field_cache: Optional[Tuple[str, str]] = None  # (field_id, option_id)


def github_get_project_status_field_and_option(project_id: str, field_name: str, option_name: str) -> Tuple[str, str]:
    """Returns (field_id, option_id) for a single-select field like 'Status'."""
    global _project_field_cache
    if _project_field_cache:
        return _project_field_cache

    q = """
    query($projectId:ID!) {
      node(id:$projectId) {
        ... on ProjectV2 {
          fields(first: 50) {
            nodes {
              __typename
              ... on ProjectV2SingleSelectField {
                id
                name
                options { id name }
              }
            }
          }
        }
      }
    }
    """
    data = github_graphql(q, {"projectId": project_id})
    node = (data or {}).get("node") or {}
    fields = ((node.get("fields") or {}).get("nodes") or [])

    for f in fields:
        if f.get("__typename") == "ProjectV2SingleSelectField" and f.get("name") == field_name:
            field_id = f.get("id", "")
            for opt in f.get("options") or []:
                if opt.get("name") == option_name:
                    option_id = opt.get("id", "")
                    _project_field_cache = (field_id, option_id)
                    return field_id, option_id
            raise RuntimeError(f"Project field '{field_name}' found, but option '{option_name}' not found.")
    raise RuntimeError(f"Project single-select field '{field_name}' not found on project.")


def github_add_issue_to_project(project_id: str, content_node_id: str) -> str:
    """Returns project item id."""
    q = """
    mutation($projectId:ID!, $contentId:ID!) {
      addProjectV2ItemById(input:{projectId:$projectId, contentId:$contentId}) {
        item { id }
      }
    }
    """
    data = github_graphql(q, {"projectId": project_id, "contentId": content_node_id})
    item_id = (((data or {}).get("addProjectV2ItemById") or {}).get("item") or {}).get("id", "")
    if not item_id and DRY_RUN:
        return "ITEM_ID_DRY_RUN"
    if not item_id:
        raise RuntimeError("Failed to add item to project (no item id returned).")
    return item_id


def github_set_project_single_select(project_id: str, item_id: str, field_id: str, option_id: str) -> None:
    q = """
    mutation($projectId:ID!, $itemId:ID!, $fieldId:ID!, $optionId:String!) {
      updateProjectV2ItemFieldValue(input:{
        projectId:$projectId,
        itemId:$itemId,
        fieldId:$fieldId,
        value:{ singleSelectOptionId:$optionId }
      }) {
        projectV2Item { id }
      }
    }
    """
    github_graphql(q, {"projectId": project_id, "itemId": item_id, "fieldId": field_id, "optionId": option_id})


# ---- Main logic ----

def build_issue_body(page_url: str, props: Dict[str, Any]) -> Tuple[str, List[str]]:
    """Build a stable, audit-friendly issue body from Notion properties."""
    change_id = safe_get_richtext(props, "Change_ID") or safe_get_richtext(props, "Change ID")
    change_type = safe_get_richtext(props, "Change_Type") or safe_get_richtext(props, "Change Type")
    beschr = safe_get_richtext(props, "Beschreibung") or safe_get_richtext(props, "Description")
    severity = safe_get_richtext(props, "Incident_Severity") or safe_get_richtext(props, "Severity")
    is_incident = bool((props.get("Incident_Flag") or {}).get("checkbox")) if isinstance(props.get("Incident_Flag"), dict) else False

    labels: List[str] = []
    if is_incident:
        labels.append("incident")
    if change_type:
        labels.append(f"type:{change_type}".replace(" ", "-").lower())
    if severity:
        labels.append(f"sev:{severity}".lower())

    body = f"""\
### TerraNova Change Log (auto-export)

**Notion:** {page_url}

**Change_ID:** {change_id or "(missing)"}
**Type:** {change_type or "(missing)"}
**Incident:** {"YES" if is_incident else "no"}
**Severity:** {severity or "-"}

#### Beschreibung
{beschr or "-"}

#### Evidence
- Evidence_URL: {safe_get_richtext(props, "Evidence_URL") or safe_get_richtext(props, "Evidence URL") or "-"}
- Evidence_SHA256: {safe_get_richtext(props, "Evidence_SHA256") or safe_get_richtext(props, "Evidence SHA256") or "-"}
- Evidence_CID: {safe_get_richtext(props, "Evidence_CID") or safe_get_richtext(props, "Evidence CID") or "-"}

#### Governance
- Wesentliche_Aenderung: {safe_get_richtext(props, "Wesentliche_Aenderung") or safe_get_richtext(props, "Wesentliche Änderung") or "-"}
- Human_Oversight: {safe_get_richtext(props, "Human_Oversight") or safe_get_richtext(props, "Human Oversight") or "-"}
"""
    return body, labels


def main() -> None:
    must_env("NOTION_TOKEN", NOTION_TOKEN)
    must_env("NOTION_DATABASE_ID_CHANGES", NOTION_DB)
    must_env("GITHUB_TOKEN", GITHUB_TOKEN)
    must_env("GITHUB_REPO", GITHUB_REPO)

    payload = {
        "filter": {
            "and": [
                {"property": "Export_to_GitHub", "checkbox": {"equals": True}},
                {"property": "GitHub_Issue_URL", "url": {"is_empty": True}},
            ]
        },
        "page_size": 50,
    }

    rows = notion_query_database(NOTION_DB, payload)
    print(f"[INFO] Found {len(rows)} rows to export.")

    # Fail fast if project configured (and not DRY_RUN)
    if PROJECTV2_ID and not DRY_RUN:
        github_get_project_status_field_and_option(PROJECTV2_ID, PROJECT_STATUS_FIELD_NAME, PROJECT_STATUS_OPTION_NAME)

    for row in rows:
        page_id = row.get("id")
        page_url = row.get("url")
        props = row.get("properties", {}) or {}

        title = safe_get_title(props)
        change_id = safe_get_richtext(props, "Change_ID") or safe_get_richtext(props, "Change ID")
        issue_title = f"{change_id + ': ' if change_id else ''}{title}"

        body, labels = build_issue_body(page_url, props)

        print(f"[INFO] Creating issue for: {issue_title}")
        issue_url, issue_node_id = github_create_issue(GITHUB_REPO, issue_title, body, labels=labels or None)

        if PROJECTV2_ID and issue_node_id:
            print("[INFO] Adding issue to GitHub Project…")
            item_id = github_add_issue_to_project(PROJECTV2_ID, issue_node_id)
            try:
                field_id, option_id = github_get_project_status_field_and_option(
                    PROJECTV2_ID, PROJECT_STATUS_FIELD_NAME, PROJECT_STATUS_OPTION_NAME
                )
                github_set_project_single_select(PROJECTV2_ID, item_id, field_id, option_id)
                print(f"[OK] Project status set: {PROJECT_STATUS_OPTION_NAME}")
            except Exception as e:
                print("[WARN] Could not set Project status:", str(e))

        now_iso = datetime.now(timezone.utc).isoformat()
        notion_update_page(page_id, {
            "GitHub_Issue_URL": {"url": issue_url},
            "Exported_At": {"date": {"start": now_iso}},
        })

        print(f"[OK] Exported -> {issue_url}")
        time.sleep(0.4)


if __name__ == "__main__":
    main()
