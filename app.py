# app.py
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import os
import openai
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("gmail-ai-stub")

app = Flask(__name__)

# Настройка CORS: указываем origins, можно поставить '*' для теста, но лучше конкретный домен.
CORS(app, origins=["https://mail.google.com", "chrome-extension://*"], supports_credentials=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    log.error("OPENAI_API_KEY не задан в environment variables!")
openai.api_key = OPENAI_API_KEY

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "AI Gmail server active 🚀", "status": "ok"})

@app.route("/generate", methods=["POST", "OPTIONS"])
def generate():
    # OPTIONS будет автоматически обработан flask_cors, но держим на всякий
    if request.method == "OPTIONS":
        resp = make_response()
        resp.status_code = 204
        return resp

    try:
        data = request.get_json(force=True, silent=True) or {}
        text = (data.get("text") or "").strip()
        if not text:
            return jsonify({"error": "Empty text"}), 400

        # Пример с ChatCompletion (gpt-3.5-turbo) — старый/широко поддерживаемый интерфейс
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — вежливый помощник, коротко отвечай на письма."},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
            max_tokens=300
        )

        # Варианты извлечения ответа
        reply = ""
        try:
            reply = resp["choices"][0]["message"]["content"].strip()
        except Exception:
            reply = resp.get("choices", [{}])[0].get("text", "").strip()

        if not reply:
            return jsonify({"error": "Empty reply from OpenAI"}), 502

        return jsonify({"reply": reply})

    except openai.error.RateLimitError as e:
        log.exception("OpenAI RateLimit")
        return jsonify({"error": "Rate limit / quota exceeded"}), 429
    except openai.error.OpenAIError as e:
        log.exception("OpenAI error")
        return jsonify({"error": "OpenAI error: " + str(e)}), 502
    except Exception as e:
        log.exception("Server error")
        return jsonify({"error": "Server error: " + str(e)}), 500

if __name__ == "__main__":
    # Для локального теста:
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)), debug=False)
