import os
import sqlite3
from flask import Flask, request, render_template_string
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from threading import Thread

# Настройки Flask-приложения
app = Flask(__name__)

# Настройки бота Telegram
TOKEN = 'ВАШ_ТЕЛЕГРАМ_ТОКЕН'  # Замените на ваш токен
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Путь к базе данных
DATABASE = 'database.db'

# Подключение к базе данных
conn = sqlite3.connect(DATABASE, check_same_thread=False)
cursor = conn.cursor()

# Инициализация базы данных (если она не создана)
def init_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            filepath TEXT,
            keywords TEXT
        )
    ''')
    conn.commit()

init_db()

# Встроенные шаблоны HTML
index_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Добро пожаловать</title>
</head>
<body>
    <h1>Привет, {{ username }}!</h1>
    <p>Ваш ID: {{ user_id }}</p>
</body>
</html>
"""

results_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Результаты поиска</title>
</head>
<body>
    <h1>Результаты поиска</h1>
    {% for result in results %}
        <p>Файл: <a href="{{ result[0] }}">{{ result[0] }}</a></p>
        <p>Ключевые слова: {{ result[1] }}</p>
    {% endfor %}
</body>
</html>
"""

# Flask маршруты
@app.route('/webapp/<username>')
def webapp(username):
    user_id = request.args.get('id', type=int)
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    if not result or result[0] != user_id:
        return "Это не ваша ссылка.", 403
    return render_template_string(index_template, username=username, user_id=user_id)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    cursor.execute('SELECT filepath, keywords FROM files WHERE LOWER(keywords) LIKE ?', (f'%{query}%',))
    results = cursor.fetchall()
    return render_template_string(results_template, results=results)

# Telegram-бот
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    username = message.from_user.username
    user_id = message.from_user.id

    # Добавляем пользователя в базу данных, если его нет
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
        conn.commit()

    # Отправляем приветственное сообщение
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Каталог", url=f"https://yourapp.onrender.com/webapp/{username}?id={user_id}")
    )
    await message.reply(f"{username}, Добро пожаловать в бот ЭдитСт! Здесь вы найдете всякие фоны, эдиты и прочее для ваших видео.", reply_markup=keyboard)

@dp.message_handler(commands=['addvideo'])
async def add_video_handler(message: types.Message):
    await message.reply("Пришлите фото/видео, и оно будет добавлено в приложение.")

@dp.message_handler(content_types=['photo', 'video'])
async def handle_media(message: types.Message):
    if message.photo:
        file_id = message.photo[-1].file_id
    elif message.video:
        file_id = message.video.file_id

    file_info = await bot.get_file(file_id)
    file_path = f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'
    await message.reply("Напишите ключевые слова для поиска файла, например: зима, эдит, нефор.")

@dp.message_handler()
async def save_keywords_handler(message: types.Message):
    keywords = message.text.split(', ')
    file_path = 'https://example.com/path/to/your/file'

    cursor.execute('INSERT INTO files (filename, filepath, keywords) VALUES (?, ?, ?)',
                   (message.caption or "unknown", file_path, ', '.join(keywords)))
    conn.commit()

    await message.reply("Файл успешно добавлен!")

# Запуск Flask-приложения и бота
if __name__ == '__main__':
    def run_flask():
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port, debug=True)

    Thread(target=run_flask).start()
    executor.start_polling(dp, skip_updates=True)
