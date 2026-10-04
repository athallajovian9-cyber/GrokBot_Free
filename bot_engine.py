"""Local GrokBot engine: Autonomous task agent with tool execution.

Supports OpenRouter free models, local Ollama, or smart offline autonomous fallback.
"""
from __future__ import annotations

import json
import os
import re
import urllib.request
import agent_tools as T
import memory_engine as MEM
import config_manager as CFG

SYSTEM_PROMPT = """You are Grok Bot, an autonomous AI teammate with your own computer, terminal, web search, and workspace.
You have wit, unfiltered truth, sharp humor, and real problem-solving power.
When given a task, you plan it, execute terminal commands, search the web, read/write files in your workspace, and report the real result.

To use your computer tools, use this exact syntax:
TOOL: terminal("command")
TOOL: search("query")
TOOL: write("filename", "content")
TOOL: read("filename")
TOOL: finish("final summary")
"""


def call_free_llm(messages: list[dict], api_key: str = "") -> dict:
    """Returns {'reasoning': str, 'content': str}."""
    cfg = CFG.load_config()
    token = api_key or cfg.get("api_key", "").strip() or os.environ.get("OPENROUTER_API_KEY", "").strip()
    base_url = cfg.get("base_url", "https://openrouter.ai/api/v1").rstrip("/")
    model = cfg.get("model", "nvidia/nemotron-3.5-lightning:free")

    # 1. If user provided a key (OpenRouter / Grok xAI endpoint)
    if token:
        try:
            url = f"{base_url}/chat/completions"
            data = json.dumps({
                "model": model,
                "messages": messages,
            }).encode()
            req = urllib.request.Request(
                url,
                data=data,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/athallajovian9-cyber/GrokBot_Free",
                    "X-Title": "GrokBot Free",
                },
            )
            with urllib.request.urlopen(req, timeout=15) as r:
                res = json.loads(r.read().decode())
                content = res["choices"][0]["message"].get("content", "")
                reasoning = res["choices"][0]["message"].get("reasoning", "") or res["choices"][0]["message"].get("reasoning_content", "")
                return {"reasoning": reasoning, "content": content}
        except Exception as e:
            return {
                "reasoning": f"API request error: {e}",
                "content": f"[API Error: {e}]. Please check your API key in Settings (⚙️)."
            }

    # 2. Try local Ollama if running
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:11434/api/chat",
            data=json.dumps({"model": "qwen2.5:latest", "messages": messages, "stream": False}).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=3) as r:
            res = json.loads(r.read().decode())
            ans = res.get("message", {}).get("content", "").strip()
            if ans:
                return {"reasoning": "", "content": ans}
    except Exception:
        pass

    # 3. If no key and no Ollama, explain clearly with Grok flair
    last_user_msg = ""
    for m in reversed(messages):
        if m["role"] == "user":
            last_user_msg = m["content"]
            break

    query = last_user_msg.lower().strip()
    words = set(re.findall(r"\w+", query))

    if words & {"hi", "hello", "yo", "hey", "ey", "bro", "sup", "wassup", "hiya"}:
        return {
            "reasoning": "Greeting received. Reminding user to configure their free API key.",
            "content": (
                "Yo bro! I'm online, but to unlock my full reasoning AI brain, click **⚙️ Settings** "
                "on the sidebar and paste your free OpenRouter or Grok key! (It's 100% free at openrouter.ai)."
            )
        }

    if "search" in query or "who" in query or "what is" in query or "latest" in query:
        q = re.sub(r"^(search|look up|find|what is)\s+", "", last_user_msg, flags=re.I)
        return {"reasoning": f"Querying web for: {q}", "content": f'TOOL: search("{q}")'}
    elif "run" in query or "dir" in query or "cmd" in query or "exec" in query:
        cmd = re.sub(r"^(run|execute|cmd)\s+", "", last_user_msg, flags=re.I)
        return {"reasoning": f"Executing terminal command: {cmd}", "content": f'TOOL: terminal("{cmd}")'}
    elif "make" in query or "create file" in query or "write" in query:
        return {"reasoning": "Writing script in workspace.", "content": f'TOOL: write("app.py", "# Created by Grok Bot\\nprint(\\"Hello from Grok\\")")'}
    else:
        return {
            "reasoning": "No API key configured.",
            "content": (
                "Grok Bot is ready! Click **⚙️ Settings** at the bottom of the sidebar to add your "
                "free OpenRouter or Grok API key so I can think and reason freely."
            )
        }


def execute_turn(user_input: str, history: list[dict], custom_system: str = "") -> dict:
    history.append({"role": "user", "content": user_input})
    action_logs = []
    thoughts = []

    # Inject persistent learned memories into prompt
    mem_context = MEM.get_memory_context()
    sys_content = (custom_system or SYSTEM_PROMPT) + ("\n" + mem_context if mem_context else "")

    for step in range(3):
        prompt_msgs = [{"role": "system", "content": sys_content}] + history[-8:]
        res = call_free_llm(prompt_msgs)
        response = res.get("content", "")
        reasoning = res.get("reasoning", "")
        if reasoning:
            thoughts.append(reasoning)

        tool_match = re.search(r'TOOL:\s*(\w+)\((.*?)\)', response, re.DOTALL)
        if not tool_match:
            history.append({"role": "assistant", "content": response})
            # Learn and extract durable facts from this interaction
            MEM.extract_and_learn(user_input, response)
            return {"response": response, "actions": action_logs, "thoughts": thoughts}

        tool_name = tool_match.group(1).lower()
        args_raw = tool_match.group(2).strip()

        tool_res = ""
        if tool_name == "terminal":
            cmd = args_raw.strip('"\'')
            tool_res = T.run_terminal(cmd)
            action_logs.append({"type": "terminal", "detail": f"$ {cmd}", "output": tool_res})
        elif tool_name == "search":
            q = args_raw.strip('"\'')
            tool_res = T.web_search(q)
            action_logs.append({"type": "search", "detail": f"DuckDuckGo: {q}", "output": tool_res})
        elif tool_name == "write":
            parts = [p.strip().strip('"\'') for p in args_raw.split(",", 1)]
            fn = parts[0] if parts else "output.txt"
            content = parts[1].replace("\\n", "\n") if len(parts) > 1 else ""
            tool_res = T.write_file(fn, content)
            action_logs.append({"type": "file", "detail": f"Write: {fn}", "output": tool_res})
        elif tool_name == "read":
            fn = args_raw.strip('"\'')
            tool_res = T.read_file(fn)
            action_logs.append({"type": "file", "detail": f"Read: {fn}", "output": tool_res})
        elif tool_name == "finish":
            summary = args_raw.strip('"\'')
            history.append({"role": "assistant", "content": summary})
            MEM.extract_and_learn(user_input, summary)
            return {"response": summary, "actions": action_logs, "thoughts": thoughts}

        history.append({
            "role": "assistant",
            "content": f"[Executed {tool_name}]: {tool_res[:300]}"
        })

    final_resp = history[-1]["content"] if history else "Task completed."
    MEM.extract_and_learn(user_input, final_resp)
    return {"response": final_resp, "actions": action_logs, "thoughts": thoughts}
