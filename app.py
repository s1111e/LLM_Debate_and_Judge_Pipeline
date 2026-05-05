from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from debate.debate_orchestrator import DebateOrchestrator


BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path="")


@app.get("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/style.css")
def stylesheet():
    return send_from_directory(BASE_DIR, "style.css")


@app.post("/api/debate")
def run_debate_api():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("question", "")).strip()

    if not question:
        return jsonify({"error": "Question is required."}), 400

    try:
        debate = DebateOrchestrator()
        _, result = debate.run_debate(question)
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.get("/api/health")
def health():
    import os

    return jsonify({
        "ok": True,
        "has_api_key": bool(os.getenv("UTSA_API_KEY") or os.getenv("OPENAI_API_KEY")),
        "base_url": os.getenv("UTSA_BASE_URL") or os.getenv("OPENAI_BASE_URL"),
        "model": os.getenv("UTSA_MODEL") or os.getenv("OPENAI_MODEL")
    })


@app.get("/api/logs")
def get_logs():
    log_path = BASE_DIR / "logs" / "debate_logs.json"
    if not log_path.exists():
        return jsonify([])
    return send_from_directory(log_path.parent, log_path.name)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
