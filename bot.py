from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
TOKEN = '6336938910:AAH8Veaf5uRCJIL_pH7kdV6R_9mmmBWt_pw'

SELECT_DISEASE, HAVE_SYMPTOMS, DURATION, FEVER_LEVEL, HOME_REMEDIES = range(5)

options = [['Fever with/without Cold and Cough', 'Only Loose Motion'],
           ['Only Vomiting', 'Only Cold and Cough'],
           ['Only Stomachache', 'Only Headache', 'None of the Above']]

reply_keyboard = ReplyKeyboardMarkup(options, one_time_keyboard=True)

def start(update, context):
    update.message.reply_text("Hello! I'm your healthcare bot. How can I assist you? Type /cancel to stop the conversation.")

    return SELECT_DISEASE

def select_disease(update, context):
    update.message.reply_text("Okay, please select the disease you are suffering from:", reply_markup=reply_keyboard)

    return HAVE_SYMPTOMS

def have_symptoms(update, context):
    user_response = update.message.text
    context.user_data['disease'] = user_response
    update.message.reply_text("Okay, along with fever, do you also have Cold and Cough?", reply_markup=reply_keyboard)

    return DURATION

def duration(update, context):
    user_response = update.message.text
    context.user_data['symptoms'] = user_response
    update.message.reply_text("From how many days are you suffering from cold, cough, and fever?", reply_markup=reply_keyboard)

    return FEVER_LEVEL

def fever_level(update, context):
    user_response = update.message.text
    context.user_data['duration'] = user_response
    update.message.reply_text("Select the level of your fever:", reply_markup=reply_keyboard)

    return HOME_REMEDIES

def home_remedies(update, context):
    user_response = update.message.text
    context.user_data['fever_level'] = user_response
    update.message.reply_text("Have you tried any home remedies or any other medicine?"
                              "\n1. Yes with improvement"
                              "\n2. Yes without improvement"
                              "\n3. No", reply_markup=reply_keyboard)

    return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user
    update.message.reply_text(f"Okay, {user.first_name}, you can start the conversation again anytime you want. Type /start to begin.")

    return ConversationHandler.END

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECT_DISEASE: [MessageHandler(Filters.text, select_disease)],
            HAVE_SYMPTOMS: [MessageHandler(Filters.text, have_symptoms)],
            DURATION: [MessageHandler(Filters.text, duration)],
            FEVER_LEVEL: [MessageHandler(Filters.text, fever_level)],
            HOME_REMEDIES: [MessageHandler(Filters.text, home_remedies)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('help', start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
