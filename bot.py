import telebot

API_TOKEN = 'YOUR_API_TOKEN'  # Укажите токен бота
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.username or "Unknown"

    # Создаём кнопку для перехода на веб-приложение
    keyboard = telebot.types.InlineKeyboardMarkup()
    web_app_button = telebot.types.InlineKeyboardButton(
        text="Открыть веб-приложение",
        web_app=telebot.types.WebAppInfo(
            url=f"https://your-domain.com/webapp/{username}"  # Замените на ваш домен
        )
    )
    keyboard.add(web_app_button)
    bot.send_message(message.chat.id, "Нажмите кнопку для перехода в веб-приложение", reply_markup=keyboard)

def run_bot():
    bot.polling(non_stop=True)
