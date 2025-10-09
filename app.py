from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# Инициализация клиента OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return jsonify({"status": "Gmail AI Stub is running"})

@app.route("/generate", methods=["POST"])
def generate_reply():
    try:
        data = request.get_json()
        user_text = data.get("text", "").strip()
        language = data.get("language", "auto")

        if not user_text:
            return jsonify({"error": "No text provided"}), 400

        system_prompt = "Ты — вежливый и лаконичный AI-помощник для Gmail. Отвечай профессионально и дружелюбно."
        if language != "auto":
            system_prompt += f" Пиши ответ на {language}."

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7,
            max_tokens=300
        )

        reply = completion.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        print("Ошибка сервера:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
