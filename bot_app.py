import os
import telebot
from telebot.types import LabeledPrice
from chat_manager import ChatManager


class AnonymousBot:
    def __init__(self):
        self.bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
        self.chat_manager = ChatManager()
        self.REVEAL_PRICE_STARS = 50
        self._register_handlers()

    def _register_handlers(self):
        self.bot.message_handler(commands=['start'])(self.send_welcome)
        self.bot.message_handler(commands=['help'])(self.send_help)
        self.bot.message_handler(commands=['findrandom'])(self.find_random)
        self.bot.message_handler(commands=['stop'])(self.stop_chat)
        self.bot.message_handler(commands=['reveal'])(self.request_reveal)

        self.bot.pre_checkout_query_handler(func=lambda query: True)(self.pre_checkout_handler)
        self.bot.message_handler(content_types=['successful_payment'])(self.successful_payment_handler)

        self.bot.message_handler(content_types=[
            'text', 'sticker', 'photo', 'video', 'voice',
            'video_note', 'document', 'animation'
        ])(self.relay_message)

    def send_welcome(self, message):
        welcome_text = (
            "Привет! Добро пожаловать в анонимный чат!\n\n"
            "Команды:\n"
            "/findrandom - найти собеседника\n"
            "/stop - завершить чат\n"
            "/reveal - узнать, с кем общаешься (50 ⭐️)\n"
            "/help - справка"
        )
        self.bot.reply_to(message, welcome_text)

    def send_help(self, message):
        self.bot.reply_to(message, "Используй /findrandom для поиска и /stop для выхода.")

    def find_random(self, message):
        user_id = message.from_user.id

        if self.chat_manager.is_banned(user_id):
            self.bot.reply_to(message, "⚠️ Доступ ограничен. Вы забанены за нарушение правил.")
            return

        if self.chat_manager.is_in_chat(user_id):
            self.bot.reply_to(message, "❌ Ты уже в чате! Используй /stop.")
            return

        if self.chat_manager.is_in_queue(user_id):
            self.bot.reply_to(message, "⏳ Ты уже в очереди.")
            return

        result = self.chat_manager.try_create_chat(user_id)

        if result == "banned":
            self.bot.reply_to(message, "⚠️ Доступ ограничен.")
        elif result:
            partner_id = result
            self.bot.send_message(user_id, "✅ Собеседник найден! Начни общаться.")
            self.bot.send_message(partner_id, "✅ Собеседник найден! Начни общаться.")
        else:
            self.bot.reply_to(message, "⏳ Добавлен в очередь. Ожидаем участника...")

    def stop_chat(self, message):
        user_id = message.from_user.id
        partner_id = self.chat_manager.end_chat(user_id)
        if partner_id:
            self.bot.send_message(user_id, "🚪 Чат завершен.")
            self.bot.send_message(partner_id, "🚪 Собеседник покинул чат.")
        else:
            self.bot.reply_to(message, "❌ Ты не в чате.")

    def request_reveal(self, message):
        user_id = message.from_user.id
        if not self.chat_manager.is_in_chat(user_id):
            self.bot.reply_to(message, "❌ Функция доступна только во время активного чата.")
            return

        self.bot.send_invoice(
            chat_id=user_id,
            title="Раскрытие личности",
            description="Узнайте профиль вашего текущего собеседника.",
            invoice_payload="reveal_payload",
            provider_token="",
            currency="XTR",
            prices=[LabeledPrice(label="Reveal", amount=self.REVEAL_PRICE_STARS)]
        )

    def pre_checkout_handler(self, pre_checkout_query):
        self.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

    def successful_payment_handler(self, message):
        user_id = message.from_user.id
        charge_id = message.successful_payment.telegram_payment_charge_id
        partner_id = self.chat_manager.get_partner(user_id)

        if not partner_id:
            self.bot.send_message(user_id, "❌ Чат завершен. Мы вернуливам ваши ⭐️.")
            self.refund_stars(user_id, charge_id)
            return

        try:
            partner_info = self.bot.get_chat(partner_id)
            username = f"@{partner_info.username}" if partner_info.username else f"ID: {partner_id}"

            self.bot.send_message(partner_id, "🔔 Собеседник раскрыл ваш профиль!")

            self.bot.send_message(user_id, f"🎉 Личность раскрыта: {username}")
        except Exception as e:
            print(f"Ошибка при Reveal: {e}")
            self.bot.send_message(user_id, "⚠️ Ошибка сервиса. Звезды вернутся на баланс.")
            self.refund_stars(user_id, charge_id)

    def refund_stars(self, user_id, charge_id):
        try:
            self.bot.refund_star_payment(user_id, charge_id)
        except Exception as e:
            print(f"Не удалось сделать Refund для {user_id}: {e}")

    def relay_message(self, message):
        user_id = message.from_user.id
        partner_id = self.chat_manager.get_partner(user_id)

        if partner_id:
            self.bot.copy_message(
                chat_id=partner_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
        else:
            self.bot.reply_to(message, "💬 Ты не в чате. Используй /findrandom.")

    def run(self):
        print("Бот запущен. Ожидание сообщений...")
        self.bot.infinity_polling()