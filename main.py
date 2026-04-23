import telebot
bot = telebot.TeleBot("8658610805:AAGKRMQ-shp_XxtJFPm38ntQAw1odnSQG2U")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Anonym Ala-Too bot на связи. Чем займемся?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Ты написал: {message.text}")

print("Бот запущен...")
bot.infinity_polling()