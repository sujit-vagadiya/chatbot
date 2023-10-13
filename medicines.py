import random
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Replace 'YOUR_BOT_TOKEN' with your actual bot token obtained from BotFather
TOKEN = '6336938910:AAH8Veaf5uRCJIL_pH7kdV6R_9mmmBWt_pw'

# Conversation states
SELECT_ACTION = range(1)

# Keyboard options
actions_keyboard = ReplyKeyboardMarkup([['Health Tips', 'Ask a Question']],
                                       one_time_keyboard=True)

# Predefined health tips
health_tips = [
    "Tip 1: Drink plenty of water to stay hydrated.",
    "Tip 2: Get regular exercise for a healthy lifestyle.",
    "Tip 3: Eat a balanced diet with plenty of fruits and vegetables.",
]

def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(f"Hello, {user.first_name}! I'm Dr. HealthBot. How can I assist you today?", reply_markup=actions_keyboard)
    return SELECT_ACTION

def select_action(update: Update, context: CallbackContext) -> int:
    user_response = update.message.text
    if user_response == 'Health Tips':
        tip = random.choice(health_tips)
        update.message.reply_text(tip)
    elif user_response == 'Ask a Question':
        update.message.reply_text("Please ask your health-related question, and I'll do my best to provide information.")
    else:
        update.message.reply_text("I'm sorry, I couldn't understand your request. Please select an action from the provided options.")
    
    return SELECT_ACTION

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECT_ACTION: [MessageHandler(Filters.text & ~Filters.command, select_action)]
        },
        fallbacks=[]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r'/cancel'), select_action))  # Handle /cancel command

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
