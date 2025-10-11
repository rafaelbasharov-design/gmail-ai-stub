from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os, threading, time, requests

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "AI Gmail server active 🚀"})

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        user_text = data.get("text", "").strip()
        if not user_text:
            return jsonify({"error": "No text provided"}), 400

        prompt = f"Составь вежливый и осмысленный ответ на следующее письмо:\n\n{user_text}"
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# === KEEP-ALIVE ПИНГ ===
def keep_alive():
    while True:
        try:
            requests.get("https://gmail-ai-stub.onrender.com", timeout=10)
            print("[KeepAlive] Ping OK")
        except Exception as e:
            print("[KeepAlive] Error:", e)
        time.sleep(240)  # каждые 4 минуты


if __name__ == "__main__":
    threading.Thread(target=keep_alive, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
