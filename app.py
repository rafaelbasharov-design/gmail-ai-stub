from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# ✅ Настройка API ключа
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "Gmail AI Stub is running"})

@app.route("/generate", methods=["POST"])
def generate_reply():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()

        if not prompt:
            return jsonify({"error": "Empty prompt"}), 400

        # ✅ Совместимая версия с OpenAI API любого поколения
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Ты — вежливый и лаконичный помощник, отвечающий на письма в Gmail.",
                },
                {
                    "role": "user",
                    "content": f"Ответь на письмо: {prompt}",
                },
            ],
            max_tokens=150,
            temperature=0.7,
        )

        reply_text = response.choices[0].message["content"].strip()
        return jsonify({"reply": reply_text})

    except Exception as e:
        print("❌ SERVER ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
