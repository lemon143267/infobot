import telebot
import json
import time
import threading
import traceback
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔑 Токен бота
TOKEN = "получить можно в @BotFather"
ADMIN_ID =   # Ваш Telegram ID

# 📂 Файл с командами
COMMANDS_FILE = "commands.json"

# 🤖 Инициализация бота с HTML-разметкой
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# 📥 Загрузка команд
def load_commands():
    try:
        with open(COMMANDS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# 💾 Сохранение команд
def save_commands(commands):
    with open(COMMANDS_FILE, "w", encoding="utf-8") as file:
        json.dump(commands, file, ensure_ascii=False, indent=4)

# 📌 Команды в памяти
commands = load_commands()

# ⏳ Время старта бота
start_time = time.time()

# 📜 Отправка текста с HTML-разметкой
@bot.message_handler(func=lambda message: message.text.lstrip("/") in commands)
def send_prepared_text(message):
    command_text = message.text.lstrip("/")
    if command_text in commands:
        bot.send_message(message.chat.id, commands[command_text], parse_mode="HTML")

# 🎛 **Админ-панель**
@bot.message_handler(commands=["admin"])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "⛔ У вас нет доступа к админ-панели.")
        return

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("📋 Список команд", callback_data="list_commands"))
    keyboard.add(InlineKeyboardButton("❌ Удалить команду", callback_data="delete_command"))

    bot.send_message(message.chat.id, "<b>🔧 Админ-панель</b>", reply_markup=keyboard, parse_mode="HTML")

# 📋 **Список команд**
@bot.callback_query_handler(func=lambda call: call.data == "list_commands")
def list_commands(call):
    if not commands:
        bot.send_message(call.message.chat.id, "<b>❌ Команд пока нет</b>", parse_mode="HTML")
        return

    text = "<b>📌 Список команд:</b>\n" + "\n".join([f"/{cmd}" for cmd in commands])
    bot.send_message(call.message.chat.id, text, parse_mode="HTML")

# ❌ **Удаление команды**
@bot.callback_query_handler(func=lambda call: call.data == "delete_command")
def delete_command_start(call):
    if not commands:
        bot.send_message(call.message.chat.id, "❌ Нет команд для удаления.")
        return

    keyboard = InlineKeyboardMarkup()
    for cmd in commands:
        keyboard.add(InlineKeyboardButton(f"Удалить /{cmd}", callback_data=f"del_{cmd}"))
    bot.send_message(call.message.chat.id, "<b>🗑 Выберите команду для удаления:</b>", reply_markup=keyboard, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith("del_"))
def delete_command_finish(call):
    command = call.data[4:]
    if command in commands:
        del commands[command]
        save_commands(commands)
        bot.send_message(call.message.chat.id, f"✅ Команда /{command} удалена!", parse_mode="HTML")

# ➕ **Добавление команды (только админ)**
@bot.message_handler(commands=["add"])
def add_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "⛔ У вас нет прав на добавление команд.")
        return

    args = message.text.split(" ", 2)
    if len(args) < 3:
        bot.send_message(message.chat.id, "Используйте: <code>/add команда текст_ответа</code> (поддерживается HTML)", parse_mode="HTML")
        return

    command, response = args[1], args[2]
    commands[command] = response
    save_commands(commands)

    bot.send_message(message.chat.id, f"✅ Команда <b>/{command}</b> добавлена!", parse_mode="HTML")

# 🕰 **Команда /uptime для вывода времени работы бота**
@bot.message_handler(commands=["uptime"])
def uptime(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "⛔ У вас нет прав на использование этой команды.")
        return

    uptime_seconds = time.time() - start_time
    days = uptime_seconds // (24 * 3600)
    hours = (uptime_seconds % (24 * 3600)) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60

    uptime_message = f"<b>⏳ Время работы бота:</b> {int(days)} дн. {int(hours)} ч. {int(minutes)} мин. {int(seconds)} сек."
    bot.send_message(message.chat.id, uptime_message, parse_mode="HTML")

# Функция для отправки сообщения о времени работы бота каждые 10 часов
def send_uptime_periodically():
    uptime_seconds = time.time() - start_time
    days = uptime_seconds // (24 * 3600)
    hours = (uptime_seconds % (24 * 3600)) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    uptime_message = f"<b>⏳ Время работы бота:</b> {int(days)} дн. {int(hours)} ч. {int(minutes)} мин. {int(seconds)} сек."
    bot.send_message(ADMIN_ID, uptime_message, parse_mode="HTML")

    # Запускаем таймер на 10 часов (36000 секунд)
    threading.Timer(36000, send_uptime_periodically).start()

# Логирование ошибок и отправка их в ЛС
def send_error_log(error_message):
    bot.send_message(ADMIN_ID, f"❌ Ошибка:\n<pre>{error_message}</pre>", parse_mode="HTML")

# Обработчик ошибок
def error_handler():
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        send_error_log(str(e))
        error_handler()  # Повторный запуск бота после ошибки

# 🚀 Запуск бота и периодическая отправка uptime
send_uptime_periodically()
error_handler()
