import os
import re
from flask import Flask

from pyrogram import Client, filters

# Initialize Flask app
app = Flask(__name__)

# Initialize the bot
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

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

# Keep-alive endpoint
@app.route('/keep-alive', methods=['GET'])
def keep_alive():
    return 'Bot is alive!'

# Run Flask app and bot using Gunicorn
if __name__ == '__main__':
    # Use Gunicorn as the WSGI server with 4 worker processes
    # You can adjust the number of workers based on your server's resources
    # For example: gunicorn -w 4 -b 0.0.0.0:5000 bot:app
    import multiprocessing
    multiprocessing.set_start_method("fork")  # Required for Gunicorn on some platforms
    from gunicorn.app.base import BaseApplication

    class StandaloneApplication(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            for key, value in self.options.items():
                self.cfg.set(key, value)

        def load(self):
            return self.application

    options = {
        "bind": "0.0.0.0:5000",
        "workers": 4,
    }

    StandaloneApplication(app, options).run()
