import telebot

API_TOKEN = '7676387813:AAGchhB9OE9w4YkCPf0gOyazCxSoiiYohIQ'  # Замените на ваш токен
bot = telebot.TeleBot(API_TOKEN)

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