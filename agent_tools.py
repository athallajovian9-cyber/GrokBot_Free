"""Agent tools for GrokBot Free (local agent with terminal, browser search, files)."""
from __future__ import annotations

import json
import os
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent / "workspace"
WORKSPACE.mkdir(exist_ok=True)


def run_terminal(cmd: str) -> str:
    try:
        res = subprocess.run(
            cmd,
            shell=True,
            cwd=str(WORKSPACE),
            capture_output=True,
            text=True,
            timeout=30,
        )
        out = (res.stdout or "") + (res.stderr or "")
        return out.strip() or "[Executed successfully with no output]"
    except Exception as e:
        return f"Error: {e}"


def list_files() -> list[str]:
    files = []
    for p in WORKSPACE.rglob("*"):
        if p.is_file():
            files.append(str(p.relative_to(WORKSPACE)))
    return files


def read_file(name: str) -> str:
    p = (WORKSPACE / name).resolve()
    if not str(p).startswith(str(WORKSPACE)):
        return "Permission denied: Path outside workspace"
    if not p.is_file():
        return f"File '{name}' does not exist."
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"Error: {e}"


def write_file(name: str, content: str) -> str:
    p = (WORKSPACE / name).resolve()
    if not str(p).startswith(str(WORKSPACE)):
        return "Permission denied: Path outside workspace"
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"File '{name}' created ({len(content)} chars)."
    except Exception as e:
        return f"Error: {e}"


def web_search(query: str) -> str:
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
        )
        with urllib.request.urlopen(req, timeout=4) as resp:
            html = resp.read().decode("utf-8", errors="replace")
            import re
            snippets = re.findall(r'<a class="result__snippet[^>]*>(.*?)</a>', html, re.DOTALL)
            clean = [re.sub(r"<[^>]+>", "", s).strip() for s in snippets[:3]]
            return "\n\n".join(clean) if clean else f"Results found for query: {query}"
    except Exception as e:
        return f"[Search results simulated for offline/rate-limited queries on '{query}']"

