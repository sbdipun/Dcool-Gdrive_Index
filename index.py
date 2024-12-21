import requests
import logging
from pyrogram import Client, filters

# Your Telegram API credentials (get these from https://my.telegram.org/auth)
API_ID = 7405235
API_HASH = "5c9541eefe8452186e9649e2effc1f3f"
BOT_TOKEN = "7598711599:AAHEBdcy4de_TxbIKCOhwqiKwWSsIBw0Bd8"
API_URL = 'https://teleservicesapi.vercel.app/check-phishing'

# Create the Pyrogram Client
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Root command: /start
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "Welcome! Send me a URL, and I will check if it’s a phishing link."
    )

# URL checking logic
@app.on_message(filters.text & ~filters.command)
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

# Run the bot
if __name__ == "__main__":
    app.run()
