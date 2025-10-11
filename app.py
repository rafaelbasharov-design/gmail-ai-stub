from flask import Flask, request, jsonify
import os
import threading
import time
import requests
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🩵 Keep-alive пинг (чтобы Render не засыпал)
def keep_alive():
    while True:
        try:
            url = "https://gmail-ai-stub.onrender.com/"
            requests.get(url, timeout=5)
            print("✅ Keep-alive ping sent")
        except Exception as e:
            print("⚠️ Keep-alive error:", e)
        time.sleep(540)  # каждые 9 минут

threading.Thread(target=keep_alive, daemon=True).start()

@app.route("/")
def home():
    return jsonify({"status": "Gmail AI Stub is running"})

@app.route("/generate", methods=["POST"])
def generate_reply():
    try:
        data = request.get_json()
        email_text = data.get("text", "").strip()

        if not email_text:
            return jsonify({"error": "No email text provided"}), 400

        # 🔍 AI анализирует текст письма, а не просто поле ввода
        prompt = f"""
        Ты — вежливый и лаконичный помощник для Gmail. 
        На основе следующего письма создай короткий ответ от имени пользователя. 
        Используй стиль делового общения. Вот текст письма:
        ---
        {email_text}
        ---
        """

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты помощник по написанию писем Gmail."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=250
        )

        reply = completion.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        print("Ошибка сервера:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
