from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

# Получаем ключ из переменных окружения Render
openai.api_key = os.getenv("OPENAI_API_KEY")

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

        # Основной запрос к OpenAI
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — AI-ассистент для Gmail. Отвечай вежливо и кратко."},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7,
            max_tokens=200
        )

        reply = completion.choices[0].message["content"].strip()
        return jsonify({"reply": reply})

    except Exception as e:
        print("Ошибка сервера:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
