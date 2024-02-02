import os
import re
from pyrogram import Client, filters

# Initialize the bot
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
print("Bot Started")  # Print "Bot Started" right after bot initialization

# Dictionary to store user states
user_states = {}

# Handler for /start command
@bot.on_message(filters.command("start"))
async def start_command(_, message):
    user_states[message.chat.id] = {"paragraph": ""}  # Initialize paragraph
    await message.reply_text("Send me a paragraph containing links.")

# Handler for receiving messages
@bot.on_message(filters.private)
async def receive_message(client, message):
    if not message.text or message.text.startswith("/"):
        return
    chat_id = message.chat.id
    if chat_id in user_states:
        if not user_states[chat_id]["paragraph"]:
            user_states[chat_id]["paragraph"] = message.text  # Save paragraph
            await message.reply_text("Now send me the argument to put after the links.")
        else:
            paragraph = user_states[chat_id]["paragraph"]
            links = re.findall(r'https?://[^\s]+', paragraph)  # Updated regex
            formatted_links = [f"{link} {message.text}" for link in links]
            reply_text = "\n".join(formatted_links)
            await message.reply_text(reply_text)
            user_states[chat_id]["paragraph"] = ""  # Reset paragraph

if __name__ == '__main__':
    bot.run()
    
