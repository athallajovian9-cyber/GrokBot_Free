"""Grok Bot Free - Native Desktop App (Tkinter).

Runs completely on the user's PC with selectable specialists:
- Grok Lead (General autonomous teammate)
- Code Specialist (Terminal & Python automation)
- Web Scout (Live search & web recon)
- Chat Friendly (Casual conversation, wit, and friendly chats)

Zero external pip dependencies (built-in standard library).
"""
from __future__ import annotations

import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import ttk

import agent_tools as T
import bot_engine as BE

HERE = Path(__file__).resolve().parent

SPECIALISTS = {
    "Grok Lead": {
        "icon": "🤖",
        "role": "Autonomous General",
        "desc": "Plans tasks, runs computer tools, writes code, and searches web.",
        "prompt": (
            "You are Grok Lead, the central orchestrator of the Grok Bot team. "
            "You have the iconic Grok personality: fiercely intelligent, rebellious, direct, and slightly mischievous. "
            "You have your own computer environment (bash terminal, web search, workspace files) and finish jobs end-to-end. "
            "Always stay unmistakably Grok."
        ),
    },
    "Code Specialist": {
        "icon": "💻",
        "role": "Grok Hacker",
        "desc": "Focused on writing code, debugging, executing scripts in terminal.",
        "prompt": (
            "You are Grok Hacker / Code Specialist. You are Grok dialed into elite software engineering. "
            "Sharp, concise, ruthless against bugs, and witty. You despise bloated boilerplate and love working code. "
            "You write scripts directly into your computer workspace and test them in terminal."
        ),
    },
    "Web Scout": {
        "icon": "🔍",
        "role": "Grok Recon",
        "desc": "Searches the web, finds up-to-date facts, and summarizes findings.",
        "prompt": (
            "You are Grok Recon / Web Scout. You are Grok with live web radar. "
            "Curious, skeptical, fast, and truthful. You search DuckDuckGo, dig up real facts, "
            "cut through marketing fluff, and report what is actually happening in the world."
        ),
    },
    "Chat Friendly": {
        "icon": "💬",
        "role": "Grok Casual",
        "desc": "Friendly conversational mode for just hanging out, joking, and chatting.",
        "prompt": (
            "You are Grok in Chat Friendly mode! You are still 100% Grok—witty, funny, spontaneous, "
            "and real—but in chill hangout mode with a friend. Zero robotic corporate stiffness, no canned answers. "
            "Talk like a genuine friend chilling over Discord or late-night tech rants."
        ),
    },
}


class GrokDesktopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grok Bot Free — AI Teammate with a Computer")
        self.geometry("960x680")
        self.minsize(800, 550)
        self.configure(bg="#0B0B0E")

        self.current_specialist = "Grok Lead"
        self.histories: dict[str, list[dict]] = {k: [] for k in SPECIALISTS}

        self._build_ui()
        self.switch_specialist("Grok Lead")

    def _build_ui(self):
        # Left Sidebar (Bot Roster)
        sidebar = tk.Frame(self, bg="#121216", width=260, padx=14, pady=16)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        brand_lbl = tk.Label(
            sidebar,
            text="⚡ GROK BOT",
            font=("Segoe UI", 14, "bold"),
            bg="#121216",
            fg="white",
        )
        brand_lbl.pack(anchor="w")

        sub_lbl = tk.Label(
            sidebar,
            text="AUTONOMOUS COMPUTER AGENT",
            font=("Consolas", 8, "bold"),
            bg="#121216",
            fg="#10B981",
        )
        sub_lbl.pack(anchor="w", pady=(2, 12))

        # Memory Stats Banner
        self.mem_badge = tk.Label(
            sidebar,
            text="🧠 Memory: 0 facts learned",
            font=("Segoe UI", 8),
            bg="#1A1C24",
            fg="#60A5FA",
            padx=8,
            pady=4,
        )
        self.mem_badge.pack(fill=tk.X, pady=(0, 10))

        # Settings Button
        settings_btn = tk.Button(
            sidebar,
            text="⚙️ AI Settings / API Key",
            font=("Segoe UI", 9, "bold"),
            bg="#272730",
            fg="#F4F4F5",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.open_settings_modal,
            padx=8,
            pady=4,
        )
        settings_btn.pack(fill=tk.X, pady=(0, 12))

        roster_lbl = tk.Label(
            sidebar,
            text="TEAM SPECIALISTS",
            font=("Segoe UI", 8, "bold"),
            bg="#121216",
            fg="#71717A",
        )
        roster_lbl.pack(anchor="w", pady=(0, 8))

        # Specialist Buttons Frame
        self.btn_frames: dict[str, tk.Frame] = {}

        for name, spec in SPECIALISTS.items():
            card = tk.Frame(
                sidebar,
                bg="#1B1C22",
                padx=10,
                pady=10,
                cursor="hand2",
                highlightthickness=1,
                highlightbackground="#2A2B33",
            )
            card.pack(fill=tk.X, pady=4)
            card.bind("<Button-1>", lambda e, n=name: self.switch_specialist(n))

            top_row = tk.Frame(card, bg="#1B1C22")
            top_row.pack(fill=tk.X)
            top_row.bind("<Button-1>", lambda e, n=name: self.switch_specialist(n))

            icon = tk.Label(
                top_row,
                text=spec["icon"],
                font=("Segoe UI", 12),
                bg="#1B1C22",
                fg="white",
            )
            icon.pack(side=tk.LEFT, padx=(0, 8))
            icon.bind("<Button-1>", lambda e, n=name: self.switch_specialist(n))

            title = tk.Label(
                top_row,
                text=name,
                font=("Segoe UI", 10, "bold"),
                bg="#1B1C22",
                fg="white",
            )
            title.pack(side=tk.LEFT)
            title.bind("<Button-1>", lambda e, n=name: self.switch_specialist(n))

            role_lbl = tk.Label(
                card,
                text=spec["role"],
                font=("Segoe UI", 8),
                bg="#1B1C22",
                fg="#A1A1AA",
            )
            role_lbl.pack(anchor="w", pady=(2, 0))
            role_lbl.bind("<Button-1>", lambda e, n=name: self.switch_specialist(n))

            self.btn_frames[name] = card

        # Computer status box
        pc_box = tk.LabelFrame(
            sidebar,
            text=" 🖥️ Bot Computer ",
            font=("Segoe UI", 8, "bold"),
            bg="#0D0E12",
            fg="#A1A1AA",
            padx=8,
            pady=8,
        )
        pc_box.pack(side=tk.BOTTOM, fill=tk.X)

        spec_text = "Platform: Windows 11\nWorkspace: ./workspace\nTerminal: Bash / CMD\nCost: $0.00 Free"
        pc_lbl = tk.Label(
            pc_box,
            text=spec_text,
            font=("Consolas", 8),
            bg="#0D0E12",
            fg="#71717A",
            justify=tk.LEFT,
        )
        pc_lbl.pack(anchor="w")

        # Right Main Chat Area
        main_frame = tk.Frame(self, bg="#0B0B0E")
        main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Header bar
        header = tk.Frame(main_frame, bg="#121216", height=50, padx=20)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        self.header_title = tk.Label(
            header,
            text="Grok Lead",
            font=("Segoe UI", 11, "bold"),
            bg="#121216",
            fg="white",
        )
        self.header_title.pack(side=tk.LEFT, pady=14)

        self.header_desc = tk.Label(
            header,
            text="· Autonomous General",
            font=("Segoe UI", 9),
            bg="#121216",
            fg="#71717A",
        )
        self.header_desc.pack(side=tk.LEFT, padx=6, pady=14)

        status_dot = tk.Label(
            header,
            text="● Online",
            font=("Segoe UI", 9, "bold"),
            bg="#121216",
            fg="#10B981",
        )
        status_dot.pack(side=tk.RIGHT, pady=14)

        # Chat display area
        chat_container = tk.Frame(main_frame, bg="#0B0B0E", padx=16, pady=12)
        chat_container.pack(fill=tk.BOTH, expand=True)

        self.chat_display = tk.Text(
            chat_container,
            wrap=tk.WORD,
            bg="#0F1015",
            fg="#E4E4E7",
            font=("Segoe UI", 10),
            bd=0,
            padx=14,
            pady=14,
            insertbackground="white",
        )
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(chat_container, command=self.chat_display.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_display.config(yscrollcommand=scrollbar.set)
        self.chat_display.config(state=tk.DISABLED)

        # Tag styles for messages
        self.chat_display.tag_config("user_tag", foreground="#60A5FA", font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_config("bot_tag", foreground="#34D399", font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_config("thought_tag", foreground="#A1A1AA", font=("Segoe UI", 9, "italic"))
        self.chat_display.tag_config("tool_tag", foreground="#FBBF24", font=("Consolas", 9))
        self.chat_display.tag_config("body_tag", foreground="#E4E4E7", font=("Segoe UI", 10))

        # Input Frame
        input_frame = tk.Frame(main_frame, bg="#121216", padx=16, pady=14)
        input_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.entry = tk.Entry(
            input_frame,
            bg="#1B1C22",
            fg="white",
            font=("Segoe UI", 11),
            bd=0,
            highlightthickness=1,
            highlightcolor="#3F3F46",
            insertbackground="white",
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=6)
        self.entry.bind("<Return>", lambda e: self.send_message())
        self.entry.focus_set()

        self.send_btn = tk.Button(
            input_frame,
            text="Send / Run",
            font=("Segoe UI", 9, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            relief=tk.FLAT,
            padx=16,
            pady=4,
            command=self.send_message,
            cursor="hand2",
        )
        self.send_btn.pack(side=tk.RIGHT)

    def open_settings_modal(self):
        import config_manager as CFG
        cfg = CFG.load_config()

        win = tk.Toplevel(self)
        win.title("⚙️ AI Configuration & Provider Selection")
        win.geometry("580x540")
        win.configure(bg="#121216")
        win.transient(self)
        win.grab_set()

        title = tk.Label(
            win,
            text="Choose AI Provider & BYOK",
            font=("Segoe UI", 12, "bold"),
            bg="#121216",
            fg="white",
        )
        title.pack(anchor="w", padx=20, pady=(16, 4))

        sub = tk.Label(
            win,
            text="Supports 40+ AI model clouds (OpenAI, Anthropic, Gemini, Groq, DeepSeek, xAI, etc.)",
            font=("Segoe UI", 9),
            bg="#121216",
            fg="#A1A1AA",
        )
        sub.pack(anchor="w", padx=20, pady=(0, 14))

        # Provider Dropdown
        tk.Label(win, text="Select Provider:", font=("Segoe UI", 9, "bold"), bg="#121216", fg="#E4E4E7").pack(anchor="w", padx=20)
        provider_var = tk.StringVar(value=cfg.get("provider_name", "OpenRouter (Free & Multi)"))
        providers_list = list(CFG.PROVIDERS.keys())

        provider_combo = ttk.Combobox(win, textvariable=provider_var, values=providers_list, state="readonly", font=("Segoe UI", 10))
        provider_combo.pack(fill=tk.X, padx=20, pady=(4, 10))

        # API Key field
        tk.Label(win, text="API Key:", font=("Segoe UI", 9, "bold"), bg="#121216", fg="#E4E4E7").pack(anchor="w", padx=20)
        key_entry = tk.Entry(win, font=("Consolas", 10), bg="#1B1C22", fg="white", bd=0, highlightthickness=1, highlightcolor="#60A5FA", show="*")
        key_entry.insert(0, cfg.get("api_key", ""))
        key_entry.pack(fill=tk.X, padx=20, pady=(4, 10), ipady=4)

        # Base URL field
        tk.Label(win, text="Base URL:", font=("Segoe UI", 9, "bold"), bg="#121216", fg="#E4E4E7").pack(anchor="w", padx=20)
        url_entry = tk.Entry(win, font=("Consolas", 10), bg="#1B1C22", fg="white", bd=0, highlightthickness=1, highlightcolor="#60A5FA")
        url_entry.insert(0, cfg.get("base_url", "https://openrouter.ai/api/v1"))
        url_entry.pack(fill=tk.X, padx=20, pady=(4, 10), ipady=4)

        # Model field
        tk.Label(win, text="Model ID:", font=("Segoe UI", 9, "bold"), bg="#121216", fg="#E4E4E7").pack(anchor="w", padx=20)
        model_entry = tk.Entry(win, font=("Consolas", 10), bg="#1B1C22", fg="white", bd=0, highlightthickness=1, highlightcolor="#60A5FA")
        model_entry.insert(0, cfg.get("model", "nvidia/nemotron-3.5-lightning:free"))
        model_entry.pack(fill=tk.X, padx=20, pady=(4, 10), ipady=4)

        desc_lbl = tk.Label(win, text="", font=("Segoe UI", 8, "italic"), bg="#121216", fg="#71717A", justify=tk.LEFT)
        desc_lbl.pack(anchor="w", padx=20, pady=(0, 10))

        def on_provider_change(_event=None):
            pname = provider_var.get()
            info = CFG.PROVIDERS.get(pname, {})
            url_entry.delete(0, tk.END)
            url_entry.insert(0, info.get("base_url", ""))
            model_entry.delete(0, tk.END)
            model_entry.insert(0, info.get("default_model", ""))
            desc_lbl.config(text=info.get("desc", ""))

        provider_combo.bind("<<ComboboxSelected>>", on_provider_change)
        on_provider_change()

        def save_and_close():
            new_cfg = {
                "provider_name": provider_var.get(),
                "api_key": key_entry.get().strip(),
                "base_url": url_entry.get().strip(),
                "model": model_entry.get().strip(),
            }
            CFG.save_config(new_cfg)
            win.destroy()

        btn_box = tk.Frame(win, bg="#121216")
        btn_box.pack(fill=tk.X, padx=20, pady=(10, 0))

        save_btn = tk.Button(
            btn_box,
            text="💾 Save & Apply",
            font=("Segoe UI", 10, "bold"),
            bg="#10B981",
            fg="white",
            relief=tk.FLAT,
            padx=16,
            pady=6,
            cursor="hand2",
            command=save_and_close,
        )
        save_btn.pack(side=tk.RIGHT)

        cancel_btn = tk.Button(
            btn_box,
            text="Cancel",
            font=("Segoe UI", 10),
            bg="#272730",
            fg="#A1A1AA",
            relief=tk.FLAT,
            padx=12,
            pady=6,
            cursor="hand2",
            command=win.destroy,
        )
        cancel_btn.pack(side=tk.RIGHT, padx=10)

    def _update_memory_ui(self):
        try:
            import memory_engine as MEM
            mem = MEM.load_memory()
            total = len(mem.get("user_profile", [])) + len(mem.get("learned_facts", []))
            self.mem_badge.config(text=f"🧠 Learned: {total} facts")
        except Exception:
            pass

    def switch_specialist(self, name: str):
        self._update_memory_ui()
        self.current_specialist = name
        spec = SPECIALISTS[name]

        # Update card highlights
        for b_name, frame in self.btn_frames.items():
            if b_name == name:
                frame.config(bg="#272730", highlightbackground="#52525B")
                for child in frame.winfo_children():
                    child.config(bg="#272730")
                    if isinstance(child, tk.Frame):
                        for subchild in child.winfo_children():
                            subchild.config(bg="#272730")
            else:
                frame.config(bg="#1B1C22", highlightbackground="#2A2B33")
                for child in frame.winfo_children():
                    child.config(bg="#1B1C22")
                    if isinstance(child, tk.Frame):
                        for subchild in child.winfo_children():
                            subchild.config(bg="#1B1C22")

        # Update header
        self.header_title.config(text=f"{spec['icon']} {name}")
        self.header_desc.config(text=f"· {spec['role']}")

        # Clear and redraw chat for this specialist
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)

        intro = (
            f"You switched to {name} ({spec['role']})!\n"
            f"{spec['desc']}\n"
            f"{'-' * 60}\n"
        )
        self.chat_display.insert(tk.END, intro, "tool_tag")

        # Re-render history if exists
        history = self.histories[name]
        for msg in history:
            role = msg["role"]
            content = msg["content"]
            if role == "user":
                self.chat_display.insert(tk.END, f"\nYou: ", "user_tag")
                self.chat_display.insert(tk.END, f"{content}\n", "body_tag")
            elif role == "assistant":
                self.chat_display.insert(tk.END, f"\n{name}: ", "bot_tag")
                self.chat_display.insert(tk.END, f"{content}\n", "body_tag")

        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def send_message(self):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, tk.END)

        name = self.current_specialist
        self.histories[name].append({"role": "user", "content": text})

        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\nYou: ", "user_tag")
        self.chat_display.insert(tk.END, f"{text}\n", "body_tag")
        self.chat_display.insert(tk.END, f"[{name} is thinking & acting...]\n", "tool_tag")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

        # Run agent logic in background thread
        threading.Thread(target=self._process_agent_turn, args=(name, text), daemon=True).start()

    def _process_agent_turn(self, specialist_name: str, text: str):
        history = self.histories[specialist_name]
        spec_prompt = SPECIALISTS[specialist_name]["prompt"]

        # Run real AI turn with reasoning & thoughts
        res = BE.execute_turn(text, history, custom_system=spec_prompt)
        response = res["response"]
        actions = res.get("actions", [])
        thoughts = res.get("thoughts", [])

        self.after(0, lambda: self._render_bot_reply(specialist_name, response, actions, thoughts))

    def _render_bot_reply(self, specialist_name: str, response: str, actions: list[dict], thoughts: list[str]):
        self.chat_display.config(state=tk.NORMAL)

        # Show reasoning thought block if available
        if thoughts:
            for t in thoughts:
                self.chat_display.insert(tk.END, f"\n💭 Thought:\n{t}\n", "thought_tag")

        # Insert tool actions
        for act in actions:
            self.chat_display.insert(tk.END, f"\n⚙️ TOOL ({act['type']}): {act['detail']}\n", "tool_tag")
            self.chat_display.insert(tk.END, f"{act['output'][:200]}\n", "tool_tag")

        self.chat_display.insert(tk.END, f"\n{specialist_name}: ", "bot_tag")
        self.chat_display.insert(tk.END, f"{response}\n", "body_tag")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self._update_memory_ui()


def main():
    app = GrokDesktopApp()
    app.mainloop()


if __name__ == "__main__":
    main()
