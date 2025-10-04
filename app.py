# app.py (stub server — возвращает тестовый ответ)
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Gmail AI Stub server is running"

@app.route("/generate-reply", methods=["POST"])
def generate_reply():
    data = request.get_json(silent=True) or {}
    text = data.get("message", "") or data.get("email_text", "")
    # Возвращаем фиксированный безопасный ответ — для проверки end-to-end
    reply = "Здравствуйте! Это тестовый ответ сервера (stub)."
    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
