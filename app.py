from threading import Thread
from bot import bot
from webapp import create_app

# --- Настройки ---
PORT = 5000

if __name__ == "__main__":
    # Создание Flask-приложения
    app = create_app()

    # Запуск Flask-приложения в отдельном потоке
    Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': PORT}).start()

    # Запуск бота
    bot.polling(non_stop=True)
