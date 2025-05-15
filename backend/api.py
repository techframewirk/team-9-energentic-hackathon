# backend/api.py

import os
import signal
import subprocess
import atexit
import sys
from flask import Flask, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Paths for logs and script
AGENT_LOG   = os.path.join(os.path.dirname(__file__), "logs", "agent_actions.log")
CONSOLE_LOG = os.path.join(os.path.dirname(__file__), "logs", "main_console.log")
MAIN_SCRIPT = os.path.join(os.path.dirname(__file__), "main.py")

# Process handle
agent_proc = None

def cleanup_agent():
    """Ensure any running agent subprocess is terminated."""
    global agent_proc
    if agent_proc and agent_proc.poll() is None:
        os.killpg(os.getpgid(agent_proc.pid), signal.SIGTERM)
        try:
            agent_proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            os.killpg(os.getpgid(agent_proc.pid), signal.SIGKILL)
    agent_proc = None

# Register cleanup on normal exit
atexit.register(cleanup_agent)

# Also handle OS signals for forced shutdown
def _handle_exit(sig, frame):
    cleanup_agent()
    sys.exit(0)

signal.signal(signal.SIGINT, _handle_exit)
signal.signal(signal.SIGTERM, _handle_exit)

@app.route("/api/agent/toggle", methods=["POST"])
def toggle_agent():
    """
    POST {"active": true|false}
    Starts or stops the main.py agent subprocess.
    """
    global agent_proc
    data   = request.get_json() or {}
    active = data.get("active", True)

    if active:
        # Start agent if not already running
        if agent_proc is None or agent_proc.poll() is not None:
            os.makedirs(os.path.dirname(CONSOLE_LOG), exist_ok=True)
            console_f = open(CONSOLE_LOG, "a", buffering=1, encoding="utf-8")
            agent_proc = subprocess.Popen(
                ["python", "-u", MAIN_SCRIPT],
                cwd=os.path.dirname(MAIN_SCRIPT),
                stdout=console_f,
                stderr=console_f,
                bufsize=1,
                universal_newlines=True,
                preexec_fn=os.setsid
            )
    else:
        # Stop the running agent
        if agent_proc and agent_proc.poll() is None:
            os.killpg(os.getpgid(agent_proc.pid), signal.SIGTERM)
            try:
                agent_proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                os.killpg(os.getpgid(agent_proc.pid), signal.SIGKILL)
        agent_proc = None

    return ("", 204)

@app.route("/api/logs", methods=["GET"])
def stream_agent_logs():
    """Tail the LAAM/context log (agent_actions.log)."""
    if not os.path.exists(AGENT_LOG):
        return Response("", mimetype="text/plain")
    with open(AGENT_LOG, "rb") as f:
        try:
            f.seek(-20000, os.SEEK_END)
        except OSError:
            f.seek(0)
        data = f.read().decode("utf-8", errors="replace")
    return Response(data, mimetype="text/plain")

@app.route("/api/console", methods=["GET"])
def stream_console():
    """Tail main.py’s stdout/stderr log (main_console.log)."""
    if not os.path.exists(CONSOLE_LOG):
        return Response("", mimetype="text/plain")
    with open(CONSOLE_LOG, "rb") as f:
        try:
            f.seek(-20000, os.SEEK_END)
        except OSError:
            f.seek(0)
        data = f.read().decode("utf-8", errors="replace")
    return Response(data, mimetype="text/plain")

if __name__ == "__main__":
    # Launch Flask API on port 5001
    app.run(host="0.0.0.0", port=5001)
