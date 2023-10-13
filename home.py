import random
import requests
TOKEN = '6336938910:AAH8Veaf5uRCJIL_pH7kdV6R_9mmmBWt_pw'
sample_medicines = [
    "Aspirin",
    "Ibuprofen",
    "Acetaminophen",
    "Amoxicillin",
    "Lisinopril",
]        
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
        send_message(chat_id, "Hello! I'm your medicine bot. How can I assist you?")
    elif text == "/help":
        send_message(chat_id, "Here are some available commands:\n"
                              "/start - Start a conversation with the bot\n"
                              "/help - Display this help message\n"
                              "/info - Get information\n"
                              "/status - Check status\n"
                              "/medicine - Get a random medicine suggestion")
    elif text == "/info":
        send_message(chat_id, "This is a simple medicine suggestion bot. It provides random medicine suggestions.")
    elif text == "/status":
        send_message(chat_id, "Bot is currently online and operational.")
    elif text == "/medicine":
        random_medicine = random.choice(sample_medicines)
        send_message(chat_id, f"Here's a random medicine suggestion: {random_medicine}")

def main():
    offset = None

    while True:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        params = {"offset": offset}
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("ok"):
            for update in data.get("result"):
                offset = update.get("update_id") + 1
                if "message" in update:
                    handle_command(update)
        else:
            print("Failed to fetch updates.")

if __name__ == '__main__':
    main()
