import requests
import json
TOKEN = '6336938910:AAH8Veaf5uRCJIL_pH7kdV6R_9mmmBWt_pw'

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    response = requests.post(url, json=payload)
    return response.json()

def handle_command(update):
    message = update["message"]
    chat_id = message["chat"]["id"]
    text = message["text"]

    if text == "/start":
        send_message(chat_id, "Hello! I'm your bot. How can I assist you?")
    elif text == "/help":
        send_message(chat_id, "Here are some available commands:\n"
                              "/start - Start a conversation with the bot\n"
                              "/help - Display this help message\n"
                              "/info - Get information\n"
                              "/status - Check status\n"
                              "/about - Learn more about this bot")
    elif text == "/info":
        send_message(chat_id, "This is a simple Telegram bot created to demonstrate command handling.")
    elif text == "/status":
        send_message(chat_id, "Bot is currently online and operational.")
    elif text == "/about":
        send_message(chat_id, "This bot was created by ChatGPT, a language model developed by OpenAI.")

def main():
    offset = None

    while True:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        params = {"offset": offset}
        response = requests.get(url, params=params)
        data = response.json()

        if data["ok"]:
            for update in data["result"]:
                offset = update["update_id"] + 1
                if "message" in update:
                    handle_command(update)
        else:
            print("Failed to fetch updates.")

if __name__ == '__main__':
    main()