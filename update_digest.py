import urllib.request
import json
import os
from datetime import datetime, timezone

# Deteksi otomatis nama akun dan repositori dari GitHub Actions
repo_full = os.environ.get("GITHUB_REPOSITORY", "username/ai-tech-trends-digest")
owner = repo_full.split("/")[0]

# 1. Ambil 6 Repositori AI Terpopuler dari GitHub API
gh_url = "https://api.github.com/search/repositories?q=topic:ai&sort=stars&order=desc&per_page=6"
req_gh = urllib.request.Request(gh_url, headers={"User-Agent": "AI-Tech-Digest"})
with urllib.request.urlopen(req_gh) as res:
    gh_data = json.loads(res.read().decode())["items"]

# 2. Ambil 6 Model Terpopuler dari Hugging Face API
hf_url = "https://huggingface.co/api/models?sort=likes&direction=-1&limit=6"
req_hf = urllib.request.Request(hf_url, headers={"User-Agent": "AI-Tech-Digest"})
with urllib.request.urlopen(req_hf) as res:
    hf_data = json.loads(res.read().decode())

now = datetime.now(timezone.utc).strftime("%d %B %Y, %H:%M UTC")

# 3. Susun Header & Badge Status
md = f"""# 🤖 AI & Tech Trends Automated Digest

[![Auto-Update Digest](https://github.com/{repo_full}/actions/workflows/digest-cron.yml/badge.svg)](https://github.com/{repo_full}/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Maintained by](https://img.shields.io/badge/Maintained%20by-@{owner}-00C2FF?style=flat-square&logo=github)](https://github.com/{owner})
[![Update Cadence](https://img.shields.io/badge/Cadence-Every%202%20Days-38ef7d?style=flat-square&logo=clock)](https://github.com/{repo_full})

> 🚀 **An automated intelligence radar tracking high-growth AI repositories, state-of-the-art Hugging Face models, and modern full-stack development trends.**
> 
> *Generated automatically via GitHub Actions every 2 days.*

---

## 📅 Latest Snapshot: `{now}`

### 🔥 Top Trending Open-Source AI Repositories
Repositories gaining high momentum across the open-source developer ecosystem:

| Repository | Stars | Language | Key Focus & Topics |
| :--- | :---: | :---: | :--- |
"""

for repo in gh_data:
    name = repo["full_name"]
    url = repo["html_url"]
    stars = f"{repo['stargazers_count']:,}"
    lang = repo["language"] or "N/A"
    desc = (repo["description"] or "").replace("|", "-").replace("\n", " ")[:85]
    topics_list = repo.get("topics", [])[:4]
    topics_str = " ".join([f"`{t}`" for t in topics_list]) if topics_list else "`ai`"
    md += f"| **[{name}]({url})** — *{desc}...* | ⭐ {stars} | `{lang}` | {topics_str} |\n"

# 4. Susun Tabel Hugging Face
md += """
---

### 🧠 Trending Hugging Face Models
State-of-the-art architectures and checkpoints trending on Hugging Face:

| Model Identifier | Primary Task | Community Likes | Direct Link |
| :--- | :---: | :---: | :---: |
"""

for model in hf_data:
    m_id = model["id"]
    task = model.get("pipeline_tag", "other")
    likes = f"{model.get('likes', 0):,}"
    md += f"| **`{m_id}`** | `{task}` | ❤️ {likes} | [Inspect Model →](https://huggingface.co/{m_id}) |\n"

# 5. Susun Tabel Ecosystem Watch, Arsip, dan Kurator
md += f"""
---

### 🛠️ Ecosystem Watch: Core Frameworks & Tooling

| Ecosystem | Focus Area | Latest Tracked Highlight |
| :--- | :--- | :--- |
| **Next.js / React** | Full-Stack & SSR | React 19 Server Actions, Turbopack optimizations, Partial Prerendering (PPR) |
| **Python & AI Agents** | Agentic Workflows | Multi-agent orchestration, LangGraph, vLLM acceleration, Ollama local runners |
| **PHP / Laravel** | Web Services & APIs | Modern Laravel 11 architectures, Octane concurrency, dynamic RBAC integrations |
| **TypeScript / Node** | Cloud Infrastructure | Bun & Node.js 22 LTS runtime performance, typed OpenAPI generation |

---

## 📂 Historical Archives

All bi-daily snapshots are automatically versioned and archived inside the [`/digests`](./digests) directory.

---

### 👤 Curator
Curated and automated by **[@{owner}](https://github.com/{owner})**
"""

# 6. Simpan ke README.md dan Folder Arsip (/digests)
with open("README.md", "w", encoding="utf-8") as f:
    f.write(md)

os.makedirs("digests", exist_ok=True)
date_slug = datetime.now(timezone.utc).strftime("%Y-%m-%d")
with open(f"digests/digest-{date_slug}.md", "w", encoding="utf-8") as f:
    f.write(md)
