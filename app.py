from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Подключаем ключ из переменных окружения Render
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Gmail AI Stub is running"}), 200

@app.route("/generate", methods=["POST"])
def generate_reply():
    try:
        data = request.get_json()
        user_prompt = data.get("prompt", "").strip()

        if not user_prompt:
            return jsonify({"error": "Empty prompt"}), 400

        # Генерация AI-ответа
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — вежливый помощник, который пишет ответы на письма Gmail."},
                {"role": "user", "content": f"Составь короткий, вежливый ответ на это письмо:\n{user_prompt}"}
            ],
            temperature=0.7,
            max_tokens=150
        )

        ai_reply = completion.choices[0].message.content.strip()
        return jsonify({"reply": ai_reply}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
