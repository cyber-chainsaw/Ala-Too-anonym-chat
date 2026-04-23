import telebot

bot = telebot.TeleBot("8658610805:AAGKRMQ-shp_XxtJFPm38ntQAw1odnSQG2U")

queue = []

active_chats = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Команда /start - приветствие"""
    user_id = message.from_user.id
    welcome_text = (
        "Привет! Добро пожаловать в анонимный чат!\n\n"
        "Доступные команды:\n"
        "/findRandom - найти случайного собеседника\n"
        "/stop - завершить текущий чат\n"
        "/help - справка"
    )
    bot.reply_to(message, welcome_text)


@bot.message_handler(commands=['help'])
def send_help(message):
    """Команда /help - справка"""
    help_text = (
        "📌 Справка по командам:\n\n"
        "/findRandom - поиск случайного собеседника для анонимного чата\n"
        "/stop - разорвать соединение с собеседником\n"
        "/help - показать эту справку"
    )
    bot.reply_to(message, help_text)


@bot.message_handler(commands=['findRandom'])
def find_random(message):
    """Команда /findRandom - поиск собеседника"""
    user_id = message.from_user.id
    
    if user_id in active_chats:
        bot.reply_to(message, "❌ Ты уже в чате! Используй /stop для выхода.")
        return
    
    if user_id in queue:
        bot.reply_to(message, "⏳ Ты уже в очереди на поиск собеседника.")
        return
    
    if queue:
        partner_id = queue.pop(0)
        
        active_chats[user_id] = partner_id
        active_chats[partner_id] = user_id
        
        bot.send_message(
            user_id,
            "✅ Собеседник найден! Начни писать сообщения.\n"
            "Используй /stop для завершения чата."
        )
        
        
        bot.send_message(
            partner_id,
            "✅ Собеседник найден! Начни писать сообщения.\n"
            "Используй /stop для завершения чата."
        )
    else:
        
        queue.append(user_id)
        bot.reply_to(
            message,
            "⏳ Ты добавлен в очередь на поиск собеседника.\n"
            "Ожидаем второго участника..."
        )


@bot.message_handler(commands=['stop'])
def stop_chat(message):
    """Команда /stop - разорвать соединение"""
    user_id = message.from_user.id
    
    
    if user_id not in active_chats:
        bot.reply_to(message, "❌ Ты не в чате. Используй /findRandom для поиска собеседника.")
        return
    
    partner_id = active_chats[user_id]
    
    del active_chats[user_id]
    del active_chats[partner_id]
    
    
    bot.send_message(user_id, "🚪 Чат завершен. Спасибо за общение!")
    
    bot.send_message(partner_id, "🚪 Собеседник покинул чат.")


@bot.message_handler(func=lambda message: True)
def relay_message(message):
    """Пересылка сообщений между собеседниками"""
    user_id = message.from_user.id
    
    
    if user_id not in active_chats:
        bot.reply_to(
            message,
            "💬 Ты не в чате. Используй /findRandom для поиска собеседника."
        )
        return
    
    partner_id = active_chats[user_id]
    
    bot.send_message(
        partner_id,
        {message.text}
    )


print("Бот запущен. ")
bot.infinity_polling()
