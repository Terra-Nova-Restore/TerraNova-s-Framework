from http.server import BaseHTTPRequestHandler
import json


LANDING_HTML = """<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>TerraNovaCIC — Products, workflows & AI systems</title>
  <meta name="description" content="TerraNovaCIC builds AI workflow templates, artifact pipelines, databases and automation systems. A digital initiative by Terra'Nova'Restore.">
  <style>
    :root { color-scheme: dark; --bg:#090b10; --card:#121722; --text:#f4f7fb; --muted:#aab4c3; --line:#263044; --accent:#8ee6c8; --accent2:#d8b4fe; }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body { margin:0; font-family: Inter, system-ui, -apple-system, Segoe UI, sans-serif; background: radial-gradient(circle at top left,#182235,#090b10 45%); color:var(--text); }
    main { max-width:1120px; margin:0 auto; padding:56px 20px; }
    header { display:flex; justify-content:space-between; gap:24px; align-items:center; margin-bottom:72px; }
    .brand { font-weight:900; letter-spacing:.02em; }
    .pill { border:1px solid var(--line); border-radius:999px; padding:8px 12px; color:var(--muted); font-size:14px; }
    h1 { font-size:clamp(42px,7vw,82px); line-height:.95; margin:0 0 24px; letter-spacing:-.06em; }
    h2 { font-size:32px; margin:0 0 16px; }
    p { color:var(--muted); font-size:18px; line-height:1.65; }
    .hero { max-width:880px; }
    .cta { display:flex; flex-wrap:wrap; gap:12px; margin:32px 0 56px; }
    a.button { color:#07100d; background:var(--accent); text-decoration:none; font-weight:900; padding:14px 18px; border-radius:14px; display:inline-block; }
    a.secondary { color:var(--text); background:transparent; border:1px solid var(--line); }
    .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:16px; margin:24px 0 56px; }
    .card { background:linear-gradient(180deg,rgba(255,255,255,.055),rgba(255,255,255,.018)); border:1px solid var(--line); border-radius:22px; padding:24px; }
    .card h3 { margin:0 0 10px; font-size:22px; }
    .price { color:var(--accent); font-size:34px; font-weight:950; margin:12px 0; }
    .tag { color:var(--accent2); font-size:13px; font-weight:800; text-transform:uppercase; letter-spacing:.08em; }
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
      <a class="button" href="#products">View products</a>
      <a class="button secondary" href="https://app.notion.com/p/de399ec6ae50416fb38fd82c3b08b461">Free Notion Starter</a>
      <a class="button secondary" href="https://github.com/Terra-Nova-Restore/TerraNova-s-Framework">Open GitHub</a>
      <a class="button secondary" href="/api">API status</a>
    </div>
  </section>

  <section id="products">
    <h2>Products</h2>
    <p>Start small, go deeper, then implement. The current product ladder is hosted on Gumroad.</p>
    <div class="grid">
      <div class="card">
        <div class="tag">Entry</div>
        <h3>Architecture Entry Pack v0.1</h3>
        <div class="price">$19</div>
        <p>A compact public-safe entry pack for understanding the architecture, boundaries and artifact structure.</p>
        <a class="button" href="https://silvanlenhard.gumroad.com/l/architecture-entry-pack-v0-1">Open product</a>
      </div>
      <div class="card">
        <div class="tag">Blueprint</div>
        <h3>CIC Blueprint Pack v0.1</h3>
        <div class="price">$49</div>
        <p>A deeper blueprint pack for CIC structure, governance logic, workflow mapping and reproducible system thinking.</p>
        <a class="button" href="https://silvanlenhard.gumroad.com/l/cic-blueprint-pack-v0-1">Open product</a>
      </div>
      <div class="card">
        <div class="tag">Implementation</div>
        <h3>CIC Implementation Workbook v0.1</h3>
        <div class="price">$99</div>
        <p>A workbook for applying CIC concepts to concrete workflows, databases, artifacts and operational decisions.</p>
        <a class="button" href="https://silvanlenhard.gumroad.com/l/cic-implementation-workbook-v0-1">Open product</a>
      </div>
    </div>
  </section>

  <section class="grid">
    <div class="card">
      <div class="tag">Free funnel</div>
      <h3>AI Workflow Starter — Entry Edition</h3>
      <p>Free Notion starter for turning scattered AI work into repeatable workflow structure.</p>
      <a class="button secondary" href="https://app.notion.com/p/de399ec6ae50416fb38fd82c3b08b461">Open free starter</a>
    </div>
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
