
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import sqlite3

# Бот токен
TOKEN = '7676387813:AAGchhB9OE9w4YkCPf0gOyazCxSoiiYohIQ'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Подключение к базе данных
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблиц
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    file_path TEXT,
    keywords TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')
conn.commit()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Сохраняем пользователя в базу данных
    cursor.execute('INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)', (user_id, username))
    conn.commit()

    # Приветственное сообщение
    buttons = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("Каталог", url=f"https://davansik.onrender.com/webapp/{username}"),
        InlineKeyboardButton("Добавить видео", callback_data="add_video")
    )
    await message.answer(f"{username}, Добро пожаловать в бот ЭдитСт!", reply_markup=buttons)


@dp.callback_query_handler(lambda c: c.data == 'add_video')
async def add_video(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Пришлите фото/видео, и оно будет добавлено в приложение.")


@dp.message_handler(content_types=['photo', 'video'])
async def handle_file(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Получение файла
    file_id = message.photo[-1].file_id if message.photo else message.video.file_id
    file_info = await bot.get_file(file_id)
    file_path = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"

    # Сохраняем временный путь
    cursor.execute('INSERT INTO files (user_id, file_path, keywords) VALUES (?, ?, ?)',
                   (user_id, file_path, ""))
    conn.commit()

    await message.answer("Напишите ключевые слова для поиска файла, пример: зима, эдит, нефор")


@dp.message_handler()
async def handle_keywords(message: types.Message):
    user_id = message.from_user.id
    keywords = message.text

    # Обновляем ключевые слова для последнего добавленного файла пользователя
    cursor.execute('''
    UPDATE files SET keywords = ? WHERE user_id = ? AND keywords = ""
    ''', (keywords, user_id))
    conn.commit()

    await message.answer("Файл добавлен. Спасибо!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
