from webapp import create_app
from bot import run_bot
from threading import Thread

# Создаем экземпляр приложения Flask
app = create_app()

if __name__ == "__main__":
    # Запускаем Flask и бота в отдельных потоках
    flask_thread = Thread(target=lambda: app.run(host="0.0.0.0", port=5000))
    bot_thread = Thread(target=run_bot)
    flask_thread.start()
    bot_thread.start()
    flask_thread.join()
    bot_thread.join()
