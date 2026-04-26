# FULL NOTION MIRROR EXTENSION
# Exports full page blocks (NOT only DB properties)

import requests, json, os
from pathlib import Path

NOTION_API = "https://api.notion.com/v1"

class NotionFull:
    def __init__(self, token):
        self.s = requests.Session()
        self.s.headers.update({
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        })

    def get_blocks(self, page_id):
        blocks = []
        cursor = None
        while True:
            url = f"{NOTION_API}/blocks/{page_id}/children"
            params = {"page_size": 100}
            if cursor:
                params["start_cursor"] = cursor
            r = self.s.get(url, params=params)
            r.raise_for_status()
            data = r.json()
            blocks += data.get("results", [])
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
        return blocks

    def export_page(self, page_id, out_dir):
        blocks = self.get_blocks(page_id)
        Path(out_dir).mkdir(parents=True, exist_ok=True)

        # JSON dump
        with open(f"{out_dir}/{page_id}.json", "w") as f:
            json.dump(blocks, f, indent=2)

        # VERY simple markdown
        md = []
        for b in blocks:
            t = b.get("type")
            if t == "paragraph":
                text = "".join(x.get("plain_text", "") for x in b[t]["rich_text"])
                md.append(text)
        with open(f"{out_dir}/{page_id}.md", "w") as f:
            f.write("\n".join(md))

        return len(blocks)

if __name__ == "__main__":
    token = os.environ.get("NOTION_TOKEN")
    page = os.environ.get("NOTION_PAGE_ID")
    out = "mirror/notion/pages"

    nf = NotionFull(token)
    count = nf.export_page(page, out)
    print(f"Exported {count} blocks")
