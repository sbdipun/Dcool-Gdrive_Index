import os
import tempfile
import logging
from flask import Flask, request
from pyrogram import Client, filters
from pyrogram.types import Update

# Set up logging
logging.basicConfig(level=logging.INFO)

# Telegram API credentials
API_ID = int(os.getenv("API_ID", 7))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
API_URL = "

# Create a temporary directory for the session file
temp_dir = tempfile.gettempdir()
session_file_path = os.path.join(temp_dir, "my_bot.session")
logging.info(f"Session file will be stored at: {session_file_path}")

# Initialize the Pyrogram client
app = Client(
    session_file_path,  # Use session file path as the first argument
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# Initialize Flask
flask_app = Flask(__name__)

# Start the Pyrogram client
logging.info("Starting Pyrogram client...")
app.start()


# Flask route for handling Telegram Webhook
@flask_app.route(f"/bot{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    json_data = request.get_json()
    try:
        app.process_update(Update.de_json(json_data))
        return "OK", 200
    except Exception as e:
        logging.error(f"Error processing update: {e}")
        return "Internal Server Error", 500


# Flask route for health check
@flask_app.route("/", methods=["GET"])
def home():
    return "Telegram Bot is running!"


# Pyrogram handlers
@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "Welcome! Send me a URL, and I will check if it’s a phishing link."
    )


@app.on_message(filters.text)
async def check_url(client, message):
    url = message.text.strip()

    # Skip commands
    if url.startswith("/"):
        return

    try:
        # Make a request to the phishing check API
        response = await app.http.get(API_URL, params={"url": url})
        data = response.json()

        if data.get("result"):
            # Phishing detected
            await message.reply_text(
                f"⚠️ *Phishing Detected!*\n\n"
                f"🔗 URL: {data['url']}\n"
                f"🔀 Redirect URL: {data['redirect_url']}\n"
                f"📊 Probability: {data['phishing_probability']}%\n",
                parse_mode="markdown",
            )
        else:
            # Safe URL
            await message.reply_text("✅ This URL seems safe!")
    except Exception as e:
        logging.error(f"Error checking URL: {e}")
        await message.reply_text("❌ Error checking the URL. Please try again later.")


# Gracefully stop the Pyrogram client
def shutdown_client():
    logging.info("Stopping Pyrogram client...")
    app.stop()


# Register shutdown handler
import atexit
atexit.register(shutdown_client)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    flask_app.run(host="0.0.0.0", port=port)
