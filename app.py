from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# Инициализация клиента
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return jsonify({"status": "Gmail AI Stub is running"})

@app.route("/generate", methods=["POST"])
def generate_reply():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        language = data.get("language", "ru")
        tone = data.get("tone", "polite")

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # 🎯 Настройки стиля ответа
        tone_prompts = {
            "polite": "Отвечай вежливо и дружелюбно.",
            "short": "Составь очень краткий ответ, не более 2 предложений.",
            "business": "Составь ответ в деловом стиле, как в корпоративной переписке.",
            "creative": "Сделай ответ нестандартным, с лёгким креативом.",
            "thanks": "Составь ответ с благодарностью, доброжелательный тон."
        }
        tone_instruction = tone_prompts.get(tone, tone_prompts["polite"])

        # 🧠 Формируем запрос к модели
        prompt = (
            f"Ты — AI помощник для Gmail. Пользователь получил письмо на {language} языке. "
            f"{tone_instruction} Ответь на это письмо в корректной форме на {language} языке.\n\n"
            f"Письмо:\n{text}"
        )

        # 🚀 Основной запрос к OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — AI помощник Gmail. Помогаешь пользователям писать ответы на письма."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400
        )

        reply = completion.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        print("⚠️ Ошибка на сервере:", e)
        # 🛟 Fallback: если OpenAI не отвечает
        fallback_reply = (
            "Извините, сейчас AI временно недоступен. "
            "Попробуйте снова через минуту 🙏"
        )
        return jsonify({"reply": fallback_reply, "error": str(e)}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
