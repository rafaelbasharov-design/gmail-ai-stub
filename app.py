from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# --- Настройки ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Gmail AI Stub is running"})

@app.route("/generate", methods=["POST"])
def generate_reply():
    try:
        data = request.get_json()
        user_text = data.get("text", "").strip()

        if not user_text:
            return jsonify({"error": "Пустое письмо. Введите текст."}), 400

        # Генерация текста
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=f"Составь короткий, вежливый и профессиональный ответ на письмо:\n\n{user_text}"
        )

        ai_reply = response.output[0].content[0].text.strip()
        return jsonify({"reply": ai_reply})

    except Exception as e:
        return jsonify({"error": f"Ошибка на сервере: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
