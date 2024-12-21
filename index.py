import logging
from flask import Flask, request
from pyrogram import Client, filters
from pyrogram.types import Update

# Your Telegram API credentials (get these from https://my.telegram.org/auth)
API_ID = 7405235
API_HASH = "5c9541eefe8452186e9649e2effc1f3f"
BOT_TOKEN = "7598711599:AAHEBdcy4de_TxbIKCOhwqiKwWSsIBw0Bd8"
API_URL = 'https://teleservicesapi.vercel.app/check-phishing'

# Create the Pyrogram Client
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Create Flask application
flask_app = Flask(__name__)

@flask_app.route("/", methods=["GET"])
def home():
    return "Telegram Bot is running!"

@flask_app.route(f"/bot{BOT_TOKEN}", methods=["POST"])
def webhook():
    if request.method == "POST":
        json_data = request.get_json()
        update = Update.de_json(json_data)  # Deserialize the JSON update
        app.process_update(update)
        return "OK", 200
    return "Method Not Allowed", 405

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "Welcome! Send me a URL, and I will check if it’s a phishing link."
    )

@app.on_message(filters.text)
async def check_url(client, message):
    url = message.text

    if url.startswith("/"):
        return

    try:
        # Example API URL for phishing check
        API_URL = "https://teleservicesapi.vercel.app/check-phishing"
        response = await app.http.get(API_URL, params={"url": url})
        data = response.json()

        if data.get("result"):
            await message.reply_text(
                f"⚠️ *Phishing Detected!*\n\n"
                f"🔗 URL: {data['url']}\n"
                f"🔀 Redirect URL: {data['redirect_url']}\n"
                f"📊 Probability: {data['phishing_probability']}%\n",
                parse_mode="markdown",
            )
        else:
            await message.reply_text("✅ This URL seems safe!")
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.reply_text("❌ Error checking the URL. Please try again later.")

# Start Pyrogram Client
@app.on_event("startup")
async def startup():
    await app.start()

@app.on_event("shutdown")
async def shutdown():
    await app.stop()

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=int(os.getenv("PORT", 3000)))
