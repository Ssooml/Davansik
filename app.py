from flask import Flask, request, jsonify
import telebot
import sqlite3
import secrets
from threading import Thread

# --- Настройки ---
API_TOKEN = "7676387813:AAGchhB9OE9w4YkCPf0gOyazCxSoiiYohIQ"
PORT = 5000
DATABASE = "users.db"

# Инициализация бота и Flask-приложения
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Функции работы с базой данных
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            nickname TEXT,
            phone TEXT,
            token TEXT
        )
        """)
        conn.commit()

def save_user(telegram_id, nickname, phone, token):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO users (telegram_id, nickname, phone, token)
        VALUES (?, ?, ?, ?)
        """, (telegram_id, nickname, phone, token))
        conn.commit()

def get_user(telegram_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        return cursor.fetchone()

# Telegram-бот
@bot.message_handler(commands=['start'])
def start(message):
    telegram_id = message.from_user.id
    user = get_user(telegram_id)
    if user:
        bot.send_message(message.chat.id, "Вы уже зарегистрированы! Откройте веб-приложение через меню бота.")
    else:
        bot.send_message(message.chat.id, "Отправьте номер телефона для регистрации.",
                         reply_markup=phone_request_keyboard())

@bot.message_handler(content_types=['contact'])
def handle_phone(message):
    if message.contact:
        telegram_id = message.from_user.id
        phone = message.contact.phone_number
        nickname = message.from_user.username or f"User{telegram_id}"
        token = secrets.token_hex(16)
        save_user(telegram_id, nickname, phone, token)
        bot.send_message(message.chat.id, "Регистрация завершена! Откройте веб-приложение через меню бота.")

def phone_request_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = telebot.types.KeyboardButton("Отправить номер телефона", request_contact=True)
    keyboard.add(button)
    return keyboard

# Flask-приложение
@app.route('/webapp/<int:telegram_id>', methods=['GET'])
def webapp(telegram_id):
    user = get_user(telegram_id)
    if user:
        nickname = user[1]
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Telegram Web App</title>
            <style>
                body {{
                    margin: 0;
                    display: flex;
                    flex-direction: column;
                    height: 100vh;
                    font-family: Arial, sans-serif;
                }}
                header {{
                    background-color: #333;
                    color: white;
                    text-align: center;
                    padding: 10px;
                }}
                main {{
                    flex: 1;
                    display: none;
                    justify-content: center;
                    align-items: center;
                }}
                .active {{
                    display: flex;
                }}
                footer {{
                    display: flex;
                    justify-content: space-around;
                    background-color: #f1f1f1;
                    padding: 10px;
                }}
                .button {{
                    padding: 10px;
                    background-color: #007bff;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }}
            </style>
            <script>
                function showPage(pageId) {{
                    document.querySelectorAll('main').forEach(page => page.classList.remove('active'));
                    document.getElementById(pageId).classList.add('active');
                }}
            </script>
        </head>
        <body>
            <header>Добро пожаловать, {nickname}</header>
            <main id="page1" class="active">
                <h1>Это первая страница</h1>
            </main>
            <main id="page2">
                <h1>Это вторая страница</h1>
            </main>
            <footer>
                <button class="button" onclick="showPage('page1')">Страница 1</button>
                <button class="button" onclick="showPage('page2')">Страница 2</button>
            </footer>
        </body>
        </html>
        """
    return "Пользователь не найден", 404

# Запуск приложения
if __name__ == "__main__":
    init_db()
    Thread(target=lambda: bot.polling(non_stop=True)).start()
    app.run(host="0.0.0.0", port=PORT)
