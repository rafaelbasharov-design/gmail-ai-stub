from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# Подключаем OpenAI с ключом из Render
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
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — AI для Gmail. Отвечай кратко, дружелюбно и по существу."},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7,
            max_tokens=200
        )

        reply = completion.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        print("Ошибка на сервере:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
