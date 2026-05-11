import telebot
import requests
from flask import Flask, request

BOT_TOKEN = "8007635004:AAEEEhVhuPui8Seg9qBauyzFkTBiAU4ZbxE"
GETCOURSE_KEY = "FjqP3bEpvsFB9xk53DcF4UJ9GA4TWG8VOpdKHWwezcVHBQm1ABDsB4s55mMQa0HSnXHsZfbA1bjT7yFm8ab3ZSlfM5zKmxI4uDqGI72mydAboqp9M6P6HcHyfGFFjgos"
GETCOURSE_DOMAIN = "https://chinabusinessacademy.getcourse.ru"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Введи email из GetCourse:")

@bot.message_handler(content_types=['text'])
def handle_text(message):

    telegram_id = message.chat.id
    email = message.text.strip()

    requests.post(
        f"{GETCOURSE_DOMAIN}/pl/api/users/update",
        data={
            "key": GETCOURSE_KEY,
            "user[email]": email,
            "user[telegram_id]": telegram_id
        }
    )

    bot.send_message(telegram_id, "Готово! Ты привязан.")

@app.route("/", methods=["GET"])
def home():
    return "OK"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.data.decode("utf-8"))
    bot.process_new_updates([update])
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
