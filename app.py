from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from support_demo_service import SupportDemoError, SupportDemoService


app = Flask(__name__)
service = SupportDemoService()


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/session/create")
def create_session():
    return jsonify(service.create_session())


@app.post("/api/reset")
def reset_demo():
    return jsonify(service.reset_demo())


@app.post("/api/state")
def get_state():
    payload = request.get_json(silent=True) or {}
    session_id = payload.get("session_id")
    return jsonify(service.get_state(session_id))


@app.post("/api/message")
def send_message():
    payload = request.get_json(silent=True) or {}
    session_id = payload.get("session_id")
    message = payload.get("message", "")
    try:
        return jsonify(service.send_message(session_id, message))
    except SupportDemoError as exc:
        return jsonify({"error": str(exc)}), 400


@app.post("/api/approval")
def decide_workflow():
    payload = request.get_json(silent=True) or {}
    workflow_id = payload.get("workflow_id")
    decision = payload.get("decision")
    approver = payload.get("approver", "demo-operator")
    try:
        return jsonify(service.decide_workflow(workflow_id, decision, approver))
    except SupportDemoError as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=13001, debug=True)
