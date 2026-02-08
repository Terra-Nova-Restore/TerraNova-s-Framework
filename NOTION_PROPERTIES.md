# Notion Properties Needed (AI_Incidents_and_Changes)

This controller expects these properties in the **Changes** database:

Required:
- `Export_to_GitHub` (Checkbox) — mark rows to export
- `GitHub_Issue_URL` (URL) — will be filled after export
- `Exported_At` (Date) — will be filled after export

Recommended (for rich issue bodies):
- `Change_ID` (Rich text)
- `Change_Type` (Select)
- `Beschreibung` (Rich text)
- `Incident_Flag` (Checkbox)
- `Incident_Severity` (Select)
- `Evidence_URL` (URL)
- `Evidence_SHA256` (Rich text)
- `Evidence_CID` (Rich text)
- `Wesentliche_Aenderung` (Select)
- `Human_Oversight` (Checkbox)

If your property names differ, edit the filter + body builder in:
`scripts/notion_to_github.py`
