"""Local web server for GrokBot Free.
Uses standard Python http.server (no pip install required).
"""
from __future__ import annotations

import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
from pathlib import Path

import bot_engine as BE

HERE = Path(__file__).resolve().parent
STATIC_DIR = HERE / "static"
PORT = 8088

# In-memory session history
SESSION_HISTORY: list[dict] = []


class GrokHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_POST(self):
        if self.path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
                user_msg = data.get("message", "")
                bot_name = data.get("bot", "Grok Lead")

                if bot_name == "Chat Friendly":
                    q = user_msg.lower()
                    if any(w in q for w in ["hi", "hello", "yo", "hey", "sup"]):
                        resp_text = "Hey there! Great to chat with you. What's on your mind today?"
                    elif "joke" in q:
                        resp_text = "Why do programmers prefer dark mode? Because light attracts bugs! 😄"
                    elif "how are you" in q:
                        resp_text = "Running great and totally free! Ready to chat about games, movies, tech, or whatever you want."
                    else:
                        resp_text = f"That sounds awesome! Tell me more about it. I'm here for fun casual chats whenever you want."
                    result = {"response": resp_text, "actions": []}
                else:
                    result = BE.execute_turn(user_msg, SESSION_HISTORY)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(result).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


def run():
    server = HTTPServer(("127.0.0.1", PORT), GrokHandler)
    print(f"🚀 Grok Bot Free running at http://127.0.0.1:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Grok Bot server.")
        server.server_close()


if __name__ == "__main__":
    run()
