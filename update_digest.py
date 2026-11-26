import urllib.request
import json
import os
from datetime import datetime, timezone

# 1. Ambil 5 Repositori AI Terpopuler dari GitHub API
gh_url = "https://api.github.com/search/repositories?q=topic:ai&sort=stars&order=desc&per_page=5"
req_gh = urllib.request.Request(gh_url, headers={"User-Agent": "AI-Tech-Digest"})
with urllib.request.urlopen(req_gh) as res:
    gh_data = json.loads(res.read().decode())["items"]

# 2. Ambil 5 Model Terpopuler dari Hugging Face API
hf_url = "https://huggingface.co/api/models?sort=likes&direction=-1&limit=5"
req_hf = urllib.request.Request(hf_url, headers={"User-Agent": "AI-Tech-Digest"})
with urllib.request.urlopen(req_hf) as res:
    hf_data = json.loads(res.read().decode())

now = datetime.now(timezone.utc).strftime("%d %B %Y, %H:%M UTC")

# 3. Susun Tabel Markdown
md = f"# 🤖 AI & Tech Trends Automated Digest\n\n"
md += f"> 🚀 **Radar otomatis pemantau repositori AI dan model Hugging Face terpopuler.**\n\n"
md += f"## 📅 Latest Snapshot: `{now}`\n\n"
md += "### 🔥 Top Trending Open-Source AI Repositories\n\n"
md += "| Repository | Stars | Language | Description |\n"
md += "| :--- | :---: | :---: | :--- |\n"

for repo in gh_data:
    name = repo["full_name"]
    url = repo["html_url"]
    stars = f"{repo['stargazers_count']:,}"
    lang = repo["language"] or "N/A"
    desc = (repo["description"] or "").replace("|", "-").replace("\n", " ")[:80]
    md += f"| **[{name}]({url})** | ⭐ {stars} | `{lang}` | {desc}... |\n"

md += "\n---\n\n### 🧠 Trending Hugging Face Models\n\n"
md += "| Model Identifier | Primary Task | Community Likes | Direct Link |\n"
md += "| :--- | :---: | :---: | :---: |\n"

for model in hf_data:
    m_id = model["id"]
    task = model.get("pipeline_tag", "other")
    likes = f"{model.get('likes', 0):,}"
    md += f"| **`{m_id}`** | `{task}` | ❤️ {likes} | [Inspect Model](https://huggingface.co/{m_id}) |\n"

# 4. Simpan ke README.md dan Folder Arsip (/digests)
with open("README.md", "w", encoding="utf-8") as f:
    f.write(md)

os.makedirs("digests", exist_ok=True)
date_slug = datetime.now(timezone.utc).strftime("%Y-%m-%d")
with open(f"digests/digest-{date_slug}.md", "w", encoding="utf-8") as f:
    f.write(md)
