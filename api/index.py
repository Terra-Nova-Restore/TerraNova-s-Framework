from http.server import BaseHTTPRequestHandler
import json


LANDING_HTML = """<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>TerraNovaCIC — Digital workflows & AI systems</title>
  <meta name="description" content="TerraNovaCIC builds AI workflow templates, artifact pipelines, databases and automation systems. A digital initiative by Terra'Nova'Restore.">
  <style>
    :root { color-scheme: dark; --bg:#090b10; --card:#121722; --text:#f4f7fb; --muted:#aab4c3; --line:#263044; --accent:#8ee6c8; }
    * { box-sizing: border-box; }
    body { margin:0; font-family: Inter, system-ui, -apple-system, Segoe UI, sans-serif; background: radial-gradient(circle at top left,#182235,#090b10 45%); color:var(--text); }
    main { max-width:1100px; margin:0 auto; padding:56px 20px; }
    header { display:flex; justify-content:space-between; gap:24px; align-items:center; margin-bottom:72px; }
    .brand { font-weight:800; letter-spacing:.02em; }
    .pill { border:1px solid var(--line); border-radius:999px; padding:8px 12px; color:var(--muted); font-size:14px; }
    h1 { font-size:clamp(42px,7vw,82px); line-height:.95; margin:0 0 24px; letter-spacing:-.06em; }
    h2 { font-size:30px; margin:0 0 16px; }
    p { color:var(--muted); font-size:18px; line-height:1.65; }
    .hero { max-width:850px; }
    .cta { display:flex; flex-wrap:wrap; gap:12px; margin:32px 0 56px; }
    a.button { color:#07100d; background:var(--accent); text-decoration:none; font-weight:800; padding:14px 18px; border-radius:14px; }
    a.secondary { color:var(--text); background:transparent; border:1px solid var(--line); }
    .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:16px; margin:24px 0 56px; }
    .card { background:linear-gradient(180deg,rgba(255,255,255,.045),rgba(255,255,255,.015)); border:1px solid var(--line); border-radius:22px; padding:22px; }
    .card h3 { margin:0 0 10px; font-size:21px; }
    .small { font-size:14px; color:var(--muted); }
    footer { border-top:1px solid var(--line); padding-top:24px; color:var(--muted); }
  </style>
</head>
<body>
<main>
  <header>
    <div class="brand">TerraNovaCIC</div>
    <div class="pill">A digital initiative by Terra'Nova'Restore</div>
  </header>

  <section class="hero">
    <h1>AI workflows, artifact pipelines and automation systems.</h1>
    <p>TerraNovaCIC turns AI chats, ideas and decisions into structured artifacts, source-aware records, publishable outputs and practical databases.</p>
    <div class="cta">
      <a class="button" href="https://artifact-pipeline.notion.site">View templates</a>
      <a class="button secondary" href="https://github.com/Terra-Nova-Restore/TerraNova-s-Framework">Open GitHub</a>
      <a class="button secondary" href="/api">API status</a>
    </div>
  </section>

  <section class="grid">
    <div class="card">
      <h3>AI Workflow Starter</h3>
      <p>Entry-level Notion template for turning scattered AI work into repeatable workflow structure.</p>
    </div>
    <div class="card">
      <h3>Artifact Pipeline</h3>
      <p>Workflow and artifact system for decisions, source tracking, publishable outputs and operational clarity.</p>
    </div>
    <div class="card">
      <h3>KI-Workflow Pipeline</h3>
      <p>German workflow edition for structured AI usage, templates, documentation and practical implementation.</p>
    </div>
  </section>

  <section class="grid">
    <div class="card">
      <h3>Terra'Nova'Restore</h3>
      <p>Möbel, Handwerk, Restaurierung, Einzelanfertigungen und Massanfertigungen nach Kundenwunsch.</p>
    </div>
    <div class="card">
      <h3>TerraNovaCIC</h3>
      <p>Digitale Systeme, KI-Workflows, Templates, Automationen, Datenbanken und Governance-Strukturen.</p>
    </div>
  </section>

  <section class="card">
    <h2>Public-safe boundary</h2>
    <p>No secrets. No raw Notion. No private page IDs. No investment, token, NFT, legal, medical or financial claim. Public means synthesized, not raw.</p>
    <p class="small">Contact: terra.nova.restore@gmail.com · DOI: https://doi.org/10.5281/zenodo.20073579</p>
  </section>

  <footer>
    <p class="small">© Terra'Nova'Restore / TerraNovaCIC — Switzerland</p>
  </footer>
</main>
</body>
</html>
"""


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?", 1)[0].rstrip("/") or "/"

        if path == "/api":
            payload = {
                "service": "terra-nova-s-framework",
                "status": "ok",
                "boundary": "public-safe; no secrets, no raw Notion",
            }
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "public, max-age=0, must-revalidate")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        body = LANDING_HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "public, max-age=0, must-revalidate")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
