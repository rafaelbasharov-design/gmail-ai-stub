from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

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
            return jsonify({"error": "Пустое письмо"}), 400

        # Используем Chat API вместо responses (надёжнее и быстрее)
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты вежливый ассистент, пиши краткие и дружелюбные ответы на письма."},
                {"role": "user", "content": user_text}
            ],
            max_tokens=120,
            temperature=0.7,
            timeout=20  # предотвращает зависание
        )

        ai_reply = completion.choices[0].message.content.strip()
        return jsonify({"reply": ai_reply})

    except Exception as e:
        print("SERVER ERROR:", str(e))
        return jsonify({"error": f"Ошибка на сервере: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
