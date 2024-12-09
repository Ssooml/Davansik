from flask import Flask, render_template_string, request
import telebot
from threading import Thread

# --- Настройки ---
API_TOKEN = '7676387813:AAGchhB9OE9w4YkCPf0gOyazCxSoiiYohIQ'  # Замените на ваш токен
PORT = 5000  # Порт для Flask-приложения
app = Flask(__name__)
bot = telebot.TeleBot(API_TOKEN)

# Главная страница веб-приложения с никнеймом
@app.route('/webapp/<username>', methods=['GET'])
def webapp(username):
    return render_template_string("""
    !DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Web App</title>
        <style>
            body {
                margin: 0;
                display: flex;
                flex-direction: column;
                height: 100vh;
                font-family: Arial, sans-serif;
                background-color: #454343;
            }
            header {
                background-color: #333;
                color: white;
                text-align: center;
                padding: 10px;
            }
            main {
                flex: 1;
                display: none;
                justify-content: center;
                align-items: center;
                padding: 10px;
            }
            .active {
                display: flex;
            }
            .card {
                width: 100%;
                height: 100%;
                max-width: 800px;
                background-color: #ffffff;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                padding: 20px;
                box-sizing: border-box;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            .card-content {
                flex: 1;
            }
            .button-container {
                display: flex;
                justify-content: flex-end; /* Располагает кнопки справа */
                gap: 20px; /* Расстояние между кнопками */
            }
            .button {
                padding: 12px 24px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                transition: background-color 0.3s;
            }
            .button:hover {
                background-color: #0056b3;
            }
            footer {
                display: flex;
                justify-content: center;
                background-color: #f1f1f1;
                padding: 10px;
            }
        </style>
        <script>
            function showPage(pageId) {
                document.querySelectorAll('main').forEach(page => page.classList.remove('active'));
                document.getElementById(pageId).classList.add('active');
            }
        </script>
    </head>
    <body>
        <main id="page1" class="active">
            <div class="card">
                <div class="card-content">
                    <h1>Это первая страница</h1>
                </div>
                <div class="button-container">
                    <button class="button" onclick="showPage('page1')">Страница 1</button>
                    <button class="button" onclick="showPage('page2')">Страница 2</button>
                </div>
            </div>
        </main>
        <main id="page2">
            <div class="card">
                <div class="card-content">
                    <h1>Это вторая страница</h1>
                    <p>Ваш никнейм: {{ username }}</p>
                </div>
                <div class="button-container">
                    <button class="button" onclick="showPage('page1')">Страница 1</button>
                    <button class="button" onclick="showPage('page2')">Страница 2</button>
                </div>
            </div>
        </main>
    </body>
    </html>
    """, username=username)

# Обработчик команды /start для бота
@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.username or "Unknown"  # Если никнейм не установлен

    # Создаём кнопку для перехода на веб-приложение
    keyboard = telebot.types.InlineKeyboardMarkup()
    web_app_button = telebot.types.InlineKeyboardButton(
        text="Открыть веб-приложение",
        web_app=telebot.types.WebAppInfo(
            url=f"https://davansik.onrender.com/webapp/{username}"  # Замените на ваш домен
        )
    )
    keyboard.add(web_app_button)

    bot.send_message(message.chat.id, "Нажмите кнопку для перехода в веб-приложение", reply_markup=keyboard)

# Запуск Flask-приложения и бота в отдельных потоках
if __name__ == "__main__":
    # Запуск Flask-приложения в отдельном потоке
    Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': PORT}).start()
    # Запуск бота
    bot.polling(non_stop=True)
