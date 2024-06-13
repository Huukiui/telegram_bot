from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
import os

# Увімкнення логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Отримання токену з змінної оточення
TOKEN = os.getenv('TELEGRAM_TOKEN')
# Ваш Telegram user ID
ADMIN_ID = os.getenv('ADMIN_ID')

# Обробник команди /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привіт! Я бот для відстеження реакцій.')

# Обробник повідомлень з реакціями
def reaction_handler(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    reaction = update.message.text
    log_message = f'Користувач {user.username} поставив реакцію: {reaction}'
    
    # Логування реакції
    logger.info(log_message)
    
    # Збереження реакції у файл
    with open('reactions.txt', 'a') as file:
        file.write(log_message + '\n')
    
    # Надсилання повідомлення адміну
    context.bot.send_message(chat_id=ADMIN_ID, text=log_message)

def main() -> None:
    # Створення Updater і передача йому токену вашого бота
    updater = Updater(TOKEN)

    # Отримання диспетчера для реєстрації обробників
    dispatcher = updater.dispatcher

    # Реєстрація обробників команд
    dispatcher.add_handler(CommandHandler("start", start))

    # Реєстрація обробника повідомлень
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reaction_handler))

    # Запуск бота
    updater.start_polling()

    # Робота бота доки не буде зупинений вручну
    updater.idle()

if __name__ == '__main__':
    main()
