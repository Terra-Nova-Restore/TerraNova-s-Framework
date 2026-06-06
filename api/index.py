from http.server import BaseHTTPRequestHandler
import json


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        body = {
            "service": "terra-nova-s-framework",
            "status": "ok",
            "boundary": "public-safe; no secrets, no raw Notion",
        }
        self.wfile.write(json.dumps(body).encode("utf-8"))
