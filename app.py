# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
# Для удобства разработки и работы расширения разрешаем CORS.
# В production можно сузить список origins.
CORS(app, resources={r"/*": {"origins": ["*"]}})

# Используем классический API клиента openai (v0.27.x style)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "AI Gmail server active 🚀", "status": "ok"})

@app.route("/generate", methods=["POST"])
def generate_reply():
    """
    Ожидает JSON: { "text": "...", "max_tokens": 200, "temperature": 0.7 }
    Возвращает JSON: { "reply": "..." } или { "error": "..."} с соответствующим HTTP-кодом.
    """
    try:
        data = request.get_json(force=True, silent=False)
    except Exception as e:
        return jsonify({"error": "Invalid JSON payload", "details": str(e)}), 400

    if not data or "text" not in data:
        return jsonify({"error": "Empty text"}), 400

    user_text = (data.get("text") or "").strip()
    if not user_text:
        return jsonify({"error": "Empty text"}), 400

    # Параметры модели — допускаем переопределение через payload
    model = data.get("model", "gpt-3.5-turbo")
    temperature = float(data.get("temperature", 0.7))
    max_tokens = int(data.get("max_tokens", 200))

    # Формируем system prompt — можно менять
    system_prompt = data.get("system_prompt") or (
        "Ты — вежливый и краткий AI-ассистент для помощи в написании ответов на электронную почту."
    )

    try:
        # Используем ChatCompletion.create (совместимо с openai==0.27.x)
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            n=1
        )

        # Попытка получить текст из ответа
        reply = ""
        if completion and getattr(completion, "choices", None):
            choice = completion.choices[0]
            # структура: choice.message.content (для chat)
            if getattr(choice, "message", None) and choice.message.get("content"):
                reply = choice.message["content"].strip()
            elif getattr(choice, "text", None):
                reply = choice.text.strip()

        if not reply:
            return jsonify({"error": "Empty reply from model", "raw": completion}), 500

        return jsonify({"reply": reply})

    except openai.error.APIError as e:
        logging.exception("OpenAI APIError")
        return jsonify({"error": f"OpenAI APIError: {str(e)}"}), 502
    except openai.error.RateLimitError as e:
        logging.exception("OpenAI RateLimitError")
        return jsonify({"error": f"OpenAI RateLimitError: {str(e)}"}), 429
    except openai.error.InvalidRequestError as e:
        logging.exception("OpenAI InvalidRequestError")
        return jsonify({"error": f"OpenAI InvalidRequestError: {str(e)}"}), 400
    except Exception as e:
        logging.exception("Unexpected server error")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
