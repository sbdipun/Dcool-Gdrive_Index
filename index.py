import requests
from telethon import TelegramClient, events

# Your Telegram API credentials (get these from https://my.telegram.org/auth)
API_ID = "7405235'  # Your API ID
API_HASH = "5c9541eefe8452186e9649e2effc1f3f  # Your API Hash
BOT_TOKEN = "7598711599:AAHEBdcy4de_TxbIKCOhwqiKwWSsIBw0Bd8"
API_URL = 'https://teleservicesapi.vercel.app/check-phishing'

# Set up the TelegramClient with Telethon
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("Welcome! Send me a URL, and I will check if it’s a phishing link.")

@client.on(events.NewMessage)
async def check_phishing(event):
    url = event.message.text

    # Skip commands like /start
    if url.startswith('/'):
        return

    try:
        # Call the phishing detection API
        response = requests.get(API_URL, params={'url': url})
        data = response.json()

        if data['result']:
            message = (f"⚠️ *Phishing Detected!*\n\n"
                       f"🔗 URL: {data['url']}\n"
                       f"🔀 Redirect URL: {data['redirect_url']}\n"
                       f"📊 Probability: {data['phishing_probability']}%")
        else:
            message = "✅ This URL seems safe!"

        await event.reply(message, parse_mode='markdown')
    except Exception as e:
        await event.reply('❌ Error checking the URL. Try again later.')

# Start the bot
async def main():
    # This will run the bot and keep it running
    await client.start()
    print("Bot is running...")
    await client.run_until_disconnected()

# Run the bot
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
