from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)  # Разрешаем все источники (в т.ч. mail.google.com)

# Ключ OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return jsonify({"status": "Gmail AI Stub is running"})

@app.route("/generate", methods=["POST"])
def generate_reply():
    try:
        data = request.get_json()
        user_text = data.get("text", "").strip()

        if not user_text:
            return jsonify({"error": "No text provided"}), 400

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты — AI помощник для Gmail. Отвечай кратко, профессионально и дружелюбно."},
                {"role": "user", "content": user_text}
            ],
            max_tokens=200,
            temperature=0.7
        )

        reply = completion.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        print("Ошибка сервера:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
