from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os, threading, time, requests

app = Flask(__name__)
CORS(app)

# Подключение клиента OpenAI с ключом из Render
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

        # Шаг 1. Определяем язык текста
        detect_prompt = f"Определи язык этого текста: ```{user_text}```. Ответь только кодом языка, например: en, ru, es, fr, de, it."
        detect_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": detect_prompt}],
        )
        lang = detect_response.choices[0].message.content.strip().lower()
        if len(lang) > 3 or not lang.isalpha():
            lang = "en"  # fallback

        # Шаг 2. Генерация ответа на том же языке
        generate_prompt = (
            f"Ты — вежливый и краткий ассистент. Ответь на следующем письме "
            f"на том же языке ({lang}), корректно и естественно:\n\n{user_text}"
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": generate_prompt}],
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply, "language": lang})

    except Exception as e:
        print("[Server Error]", e)
        return jsonify({"error": str(e)}), 500


# === KEEP-ALIVE, чтобы Render не засыпал ===
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
