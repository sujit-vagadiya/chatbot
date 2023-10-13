import random
import requests
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Replace 'YOUR_BOT_TOKEN' with your actual bot token obtained from BotFather
TOKEN = '6336938910:AAH8Veaf5uRCJIL_pH7kdV6R_9mmmBWt_pw'

# Conversation states
SELECT_SYMPTOMS, SUGGEST_MEDICINE = range(2)

# Keyboard options
symptoms_keyboard = ReplyKeyboardMarkup([['Fever', 'Cough', 'Headache'], ['Nausea', 'None of the Above']],
                                        one_time_keyboard=True)

def start(update, context):
    user = update.message.from_user
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello, {user.first_name}! I'm Dr. HealthBot. How can I assist you?")
    return SELECT_SYMPTOMS

def select_symptoms(update, context):
    update.message.reply_text("Please select your symptom(s) or type 'None of the Above':", reply_markup=symptoms_keyboard)
    return SUGGEST_MEDICINE

def search_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}  # Set a user agent to mimic a web browser
    response = requests.get(search_url, headers=headers)
    return response.text

def suggest_medicine(update, context):
    user_response = update.message.text
    if user_response in ["Fever", "Cough", "Headache", "Nausea"]:
        query = f"Medicine for {user_response}"
        search_results = search_google(query)

        # Simplified web scraping for search results
        if "No results found" not in search_results:
            start_index = search_results.find('<h3 class="r"><a href="/url?q=') + len('<h3 class="r"><a href="/url?q=')
            end_index = search_results.find('&amp;', start_index)
            if start_index != -1 and end_index != -1:
                search_link = search_results[start_index:end_index]
                search_link = requests.utils.unquote(search_link)

                response = f"For {user_response}, you can consider:\n{search_link}"
            else:
                response = f"I'm sorry, I couldn't find information for {user_response} at the moment."
        else:
            response = f"I'm sorry, I couldn't find information for {user_response} at the moment."
    else:
        response = "I'm sorry, I can only suggest medicine for the provided symptoms."

    context.bot.send_message(chat_id=update.effective_chat.id, text=response, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user
    update.message.reply_text(f"Okay, {user.first_name}, you can start the conversation again anytime you want. Type /start to begin.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECT_SYMPTOMS: [MessageHandler(Filters.text & ~Filters.command, select_symptoms)],
            SUGGEST_MEDICINE: [MessageHandler(Filters.text & ~Filters.command, suggest_medicine)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
