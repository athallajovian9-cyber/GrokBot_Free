"""Persistent memory & learning module for Grok Bot Free.

Mimics Hermes Agent memory architecture:
- Auto-extracts durable facts, user traits, preferences, and project context.
- Stores memories across sessions in `memory.json`.
- Injects recalled facts into the system prompt for every turn so Grok learns
  and gets smarter the longer you chat with it.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEM_FILE = HERE / "memory.json"


def load_memory() -> dict:
    if MEM_FILE.is_file():
        try:
            return json.loads(MEM_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "user_profile": [],
        "learned_facts": [],
        "interaction_count": 0,
    }


def save_memory(data: dict):
    try:
        MEM_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception:
        pass


def extract_and_learn(user_text: str, bot_reply: str):
    """Scan dialogue turns to discover stable preferences, names, and project context."""
    mem = load_memory()
    mem["interaction_count"] = mem.get("interaction_count", 0) + 1

    text = user_text.strip()
    profile = set(mem.get("user_profile", []))
    facts = set(mem.get("learned_facts", []))

    # Name patterns
    m_name = re.search(r"\b(?:my name is|i am called|call me)\s+([A-Za-z0-9_-]+)", text, re.I)
    if m_name:
        profile.add(f"User's name is {m_name.group(1).capitalize()}")

    # Likes / Preferences
    m_pref = re.search(r"\b(?:i like|i love|i prefer|my favorite is)\s+([^.!?\n]+)", text, re.I)
    if m_pref:
        profile.add(f"Prefers/Likes: {m_pref.group(1).strip()[:80]}")

    # Projects / Goals
    m_proj = re.search(r"\b(?:i am building|i am making|working on|my project is)\s+([^.!?\n]+)", text, re.I)
    if m_proj:
        facts.add(f"Project context: {m_proj.group(1).strip()[:100]}")

    # Tech stack
    for lang in ["Python", "Luau", "Roblox", "JavaScript", "HTML", "C++", "Rust", "Unity"]:
        if re.search(rf"\b{lang}\b", text, re.I):
            facts.add(f"Uses technology: {lang}")

    mem["user_profile"] = sorted(list(profile))
    mem["learned_facts"] = sorted(list(facts))
    save_memory(mem)


def get_memory_context() -> str:
    """Format stored memories into a prompt block for the AI."""
    mem = load_memory()
    turns = mem.get("interaction_count", 0)
    profile = mem.get("user_profile", [])
    facts = mem.get("learned_facts", [])

    if not profile and not facts and turns < 2:
        return ""

    lines = ["\n[PERSISTENT MEMORY & ACCUMULATED KNOWLEDGE]"]
    lines.append(f"- Total interactions with this user: {turns} turns")
    if profile:
        lines.append("- What you know about the user:")
        for p in profile:
            lines.append(f"  • {p}")
    if facts:
        lines.append("- Facts & project context learned over time:")
        for f in facts:
            lines.append(f"  • {f}")
    lines.append("[Use this learned knowledge naturally to personalize your replies.]\n")
    return "\n".join(lines)
