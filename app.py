from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler
import json
import os

TOKEN = os.environ.get("TOKEN")
DATA_FILE = "data.json"

bot = Bot(token=TOKEN)
app = Flask(__name__)

dispatcher = Dispatcher(bot, None, workers=4, use_context=True)


# ---------- utils ----------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ---------- handlers ----------
def start(update, context):
    chat_id = str(update.effective_chat.id)
    user = update.effective_user
    username = user.username or user.first_name

    data = load_data()

    if chat_id not in data["users"]:
        data["users"][chat_id] = {
            "username": username,
            "balance": 0
        }
        save_data(data)

    update.message.reply_text("Регистрация прошла успешно ✔")


def button(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text("Кнопка нажата")


dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(button))


# ---------- webhook ----------
@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"


@app.route("/", methods=["GET"])
def index():
    return "Bot is running"
