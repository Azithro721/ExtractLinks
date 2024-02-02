import os
import re
from pyrogram import Client, filters

# Read sensitive information from environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize the bot
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Dictionary to store user states
user_states = {}

# Print "Bot started"
print("Bot started")

# Handler for /start command
@app.on_message(filters.command("start"))
def start_command(_, message):
    user_states[message.chat.id] = {"paragraph": ""}  # Initialize paragraph
    message.reply_text("Send me a paragraph containing links.")

# Handler for receiving messages
@app.on_message(filters.private)
def receive_message(client, message):
    if not message.text or message.text.startswith("/"):
        return
    chat_id = message.chat.id
    if chat_id in user_states:
        if not user_states[chat_id]["paragraph"]:
            user_states[chat_id]["paragraph"] = message.text  # Save paragraph
            message.reply_text("Now send me the argument to put after the links.")
        else:
            paragraph = user_states[chat_id]["paragraph"]
            links = re.findall(r'https?://[^\s]+', paragraph)  # Updated regex
            print("Extracted links:", links)  # Debug print
            formatted_links = [f"{link} {message.text}" for link in links]
            reply_text = "\n".join(formatted_links)
            message.reply_text(reply_text)
            user_states[chat_id]["paragraph"] = ""  # Reset paragraph

# Start the bot
app.run()
