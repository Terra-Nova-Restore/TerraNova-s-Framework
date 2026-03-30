# Notion-GitHub Sync – Setup Runbook

**Einmalige Konfiguration** für sauberes, automatisiertes Syncing über GitHub Actions.

Nachdem dies einmal gemacht ist, läuft alles automatisch – keine lokalen Secrets, keine tägliche Frustration.

---

## Setup-Schritte (ca. 10 Minuten)

### Step 1: Notion Integration mit Database verbinden (2 min)

**In Notion:**
1. Notion Workspace öffnen
2. **Settings** (oben rechts) → **Integrations** → **Installed integrations**
3. Die Integration finden, die du für GitHub-Sync nutzen willst
4. Click **Settings** auf der Integration
5. Kopier den **Internal Integration Token** (Format: `ntn_xxxxx...`)
   - **Du brauchst diesen Wert für Step 3!**

**In der Notion Database:**
1. Die Database öffnen, die synchen soll (z.B. "Changes")
2. **Share** (oben rechts)
3. Die Integration selecten und geben ihr **Edit** Zugriff
4. ✓ Fertig – Integration kann jetzt diese DB lesen/schreiben

---

### Step 2: GitHub Personal Access Token erstellen (2 min)

**In GitHub:**
1. https://github.com/settings/tokens öffnen
2. Click **Generate new token** → **Generate new token (classic)**
3. **Token name**: `TNV-Notion-Sync` (oder was du willst)
4. **Expiration**: `90 days` (GitHub default)
5. **Select scopes**:
   - ☑️ `repo` (full control of private repositories)
   - ☑️ `issues` (manage issues)
6. Click **Generate token**
7. **KOPIER DEN TOKEN SOFORT** (danach siehst du ihn nicht mehr!)
   - Format: `ghp_xxxxx...`
   - **Du brauchst diesen Wert für Step 3!**

---

### Step 3: GitHub Repository Secrets konfigurieren (5 min)

**Infos sammeln, die du jetzt brauchst:**
- **NOTION_TOKEN**: Von Step 1 (Integration Token)
- **GH_PAT**: Von Step 2 (GitHub Token)
- **NOTION_DATABASE_ID_CHANGES**: Database ID aus Notion URL
  - Notion öffnen → Database öffnen → URL kopieren
  - ID ist dieser lange String: `https://www.notion.so/workspace/[ID]?v=xyz`
  - Nur die `[ID]` Teil (32 Zeichen)

**In GitHub:**
1. Repository öffnen
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** (3x)

Erstelle diese 3 Secrets:

| Name | Value | Beispiel |
|------|-------|----------|
| `NOTION_TOKEN` | Dein Notion Integration Token | `ntn_abc123...` |
| `NOTION_DATABASE_ID_CHANGES` | Database ID | `abc123def456...` (32 Zeichen) |
| `GH_PAT` | Dein GitHub Token | `ghp_abc123...` |

`GITHUB_REPO` wird im Workflow automatisch aus `${{ github.repository }}` gesetzt.

**Wichtig:** 
- ⚠️ Secrets sind nach Erstellung **unsichtbar** – kopier den Wert BEVOR du speicherst!
- ✓ GitHub speichert diese sicher verschlüsselt
- ✓ Workflow liest sie automatisch

---

## Workflow testen

### Option A: Automatic (10-minütlich)
Der Workflow läuft automatisch alle 10 Minuten in der GitHub Actions.
- GitHub Repository → **Actions** Tab
- Workflow `TNV – Notion → GitHub Sync` läuft und zeigt Status

### Option B: Manual (on-demand)
```bash
# In VS Code oder lokal:
# Repository öffnen
# GitHub CLI install: https://cli.github.com

gh workflow run tnv_notion_to_github.yml --repo owner/repo
```

Dann in GitHub Actions Tab checken, ob das Workflow-Run erfolgreich ist.

---

## Fehlerdiagnose

**Wenn der Workflow fehlschlägt:**

1. **GitHub Actions Tab öffnen** → Failed Run clicken
2. **Logs anschauen**: Die Preflight-Checks zeigen exakt was falsch ist:
   ```
   ✗ Notion permission denied: integration lacks database access
   → In Notion: Open database → Share → Select your integration
   ```
3. **Häufige Fehler**:
   - `Notion auth failed` → Token ist falsch/abgelaufen
   - `Database not found` → Database ID ist falsch
   - `GitHub token lacks write permission` → Token hat nicht die richtigen Scopes

**Wenn alles passt:**
- Sync läuft automatisch
- GitHub Issues werden erstellt/aktualisiert
- Notion Records werden mit GitHub Issue URL gefüllt

---

## Nach dem Setup

**Danach:** Nichts mehr zu tun. Der Workflow:
- ✓ Läuft alle 10 Minuten automatisch
- ✓ Liest Secrets sicher aus GitHub
- ✓ Validiert alle Zugriffe (Notion, GitHub)
- ✓ Syncht Daten automatisch
- ✓ Loggt alles zum Debuggen

**Wenn du Token erneuern musst:**
- GitHub Secrets aktualisieren (Settings → Secrets)
- Fertig – nächster Workflow-Run nutzt den neuen Token

---

## Sicherheit

✓ **Sicher:**
- Secrets sind GitHub-verschlüsselt, nicht im Code
- Nur GitHub Actions Runtime kann sie lesen
- Nicht auf deinem PC, nicht im Git History
- Tokens haben minimale Scopes (nur `repo` + `issues`)

⚠️ **Nicht vergessen:**
- Tokens rotieren (GitHub PAT: 90 Tage default)
- Notion Integration Token vor GitHub Sharing clearen (1Password etc.)
- Wenn kompromittiert: GitHub UI → Secret löschen und neu erstellen

---

## Nächste Schritte

1. ✓ Mache die 3 Setup-Schritte oben
2. ✓ Triggere den Workflow manuell oder warte auf nächsten Auto-Run
3. ✓ Schau die GitHub Actions Logs an
4. ✓ Falls erfolgreich: Fertig! Läuft danach automatisch

Bei Fragen: Check die Logs im GitHub Actions Tab – die Preflight-Checks sind sehr konkret in ihren Fehlermeldungen.
