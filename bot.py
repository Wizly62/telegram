import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Настройки
TOKEN = "7393517628:AAEweqPfevdcExVRahjPa3fnC8iYTta_zRo"  # Твой токен
SERVER_URL = "https://license-server-production-dac6.up.railway.app"  # Твой сервер

# Команда /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🔑 *Бот для лицензий*\n\n"
        "Команды:\n"
        "🔸 /gen HWID – создать ключ\n"
        "🔸 /ban KEY – заблокировать ключ",
        parse_mode="Markdown"
    )

# Команда /gen
def gen(update: Update, context: CallbackContext):
    hwid = " ".join(context.args)  # HWID пользователя
    if not hwid:
        update.message.reply_text("❌ Укажи HWID: /gen HWID")
        return

    try:
        # Отправляем запрос на сервер
        response = requests.post(f"{SERVER_URL}/generate", json={"hwid": hwid})
        key = response.json().get("key")
        update.message.reply_text(f"✅ Ключ: `{key}`\nHWID: `{hwid}`", parse_mode="Markdown")
    except:
        update.message.reply_text("❌ Ошибка сервера!")

# Команда /ban
def ban(update: Update, context: CallbackContext):
    key = " ".join(context.args)  # Ключ для блокировки
    if not key:
        update.message.reply_text("❌ Укажи ключ: /ban KEY")
        return

    try:
        requests.post(f"{SERVER_URL}/ban", json={"key": key})
        update.message.reply_text(f"🔒 Ключ `{key}` заблокирован!", parse_mode="Markdown")
    except:
        update.message.reply_text("❌ Ошибка!")

# Запуск бота
updater = Updater(TOKEN)
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("gen", gen))
updater.dispatcher.add_handler(CommandHandler("ban", ban))
updater.start_polling()
updater.idle()
