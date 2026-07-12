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

### Step 2: GitHub Actions-Berechtigungen prüfen (1 min)

Der TNV-Sync läuft im selben Repository. GitHub Actions stellt pro Workflow-Run
automatisch `GITHUB_TOKEN` bereit. Dafür brauchst du keinen Personal Access
Token und kein `GH_PAT`-Repository-Secret.

Der Job in `.github/workflows/tnv_notion_to_github.yml` muss diese
Berechtigungen behalten:

~~~yaml
permissions:
  contents: write
  issues: write
~~~

---

### Step 3: GitHub Repository Secrets konfigurieren (5 min)

**Infos sammeln, die du jetzt brauchst:**
- **NOTION_TOKEN**: Von Step 1 (Integration Token)
- **NOTION_DATABASE_ID_CHANGES**: Database ID aus Notion URL
  - Notion öffnen → Database öffnen → URL kopieren
  - ID ist dieser lange String: `https://www.notion.so/workspace/[ID]?v=xyz`
  - Nur die `[ID]` Teil (32 Zeichen)

**In GitHub:**
1. Repository öffnen
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** (2x)

Erstelle diese 2 Secrets:

| Name | Value | Beispiel |
|------|-------|----------|
| `NOTION_TOKEN` | Dein Notion Integration Token | `ntn_abc123...` |
| `NOTION_DATABASE_ID_CHANGES` | Database ID | `abc123def456...` (32 Zeichen) |

GitHub Actions stellt `GITHUB_TOKEN` automatisch bereit; dafür wird kein
weiteres GitHub-Secret angelegt.
`GITHUB_REPO` wird im Workflow automatisch aus `${{ github.repository }}` gesetzt.
Optionaler Override für Cross-Repo-Sync: `TARGET_GITHUB_REPO` als Secret oder Variable im Format `owner/repo`.
Für ein Cross-Repo-Ziel muss der Zugriff auf das Ziel-Repository separat
konfiguriert werden; der automatische Token garantiert nur den Same-Repo-Zugriff.

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
   - `GitHub token lacks write permission` → Prüfe, ob der Workflow-Job weiterhin
     `contents: write` und `issues: write` hat; bei einem Cross-Repo-Override
     zusätzlich den Zugriff auf das Ziel-Repository prüfen

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

**Wenn die Notion-Verbindung aktualisiert werden muss:**
- Betroffenes Notion-Secret in **Settings → Secrets** aktualisieren
- Fertig – der nächste Workflow-Run nutzt den neuen Wert
- `GITHUB_TOKEN` wird von GitHub Actions pro Workflow-Run automatisch bereitgestellt

---

## Sicherheit

✓ **Sicher:**
- Secrets sind GitHub-verschlüsselt, nicht im Code
- Nur GitHub Actions Runtime kann sie lesen
- Nicht auf deinem PC, nicht im Git History
- GitHub Actions stellt `GITHUB_TOKEN` automatisch bereit; der Job braucht nur
  `contents: write` und `issues: write`

⚠️ **Nicht vergessen:**
- Notion Integration Token gemäss deiner Sicherheitsroutine prüfen und bei Bedarf rotieren
- Workflow-Berechtigungen `contents: write` und `issues: write` beibehalten
- Notion Integration Token vor GitHub Sharing clearen (1Password etc.)
- Wenn kompromittiert: GitHub UI → Secret löschen und neu erstellen

---

## Nächste Schritte

1. ✓ Mache die 3 Setup-Schritte oben
2. ✓ Triggere den Workflow manuell oder warte auf nächsten Auto-Run
3. ✓ Schau die GitHub Actions Logs an
4. ✓ Falls erfolgreich: Fertig! Läuft danach automatisch

Bei Fragen: Check die Logs im GitHub Actions Tab – die Preflight-Checks sind sehr konkret in ihren Fehlermeldungen.
