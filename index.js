require('dotenv').config();
const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');
const express = require('express');

const BOT_TOKEN = process.env.BOT_TOKEN;
const API_URL = 'https://teleservicesapi.vercel.app/check-phishing'; // Make sure the API URL is correct
const bot = new TelegramBot(BOT_TOKEN);
const app = express();

app.use(express.json());

// Root Route to check if the bot is running
app.get('/', (req, res) => {
    res.send('Telegram Bot is running!');
});

// Set Webhook Programmatically (called on server start)
const TELEGRAM_API_URL = `https://api.telegram.org/bot${BOT_TOKEN}`;
async function setWebhook() {
    const webhookUrl = `https://${process.env.VERCEL_URL}/bot${BOT_TOKEN}`; // Vercel URL is automatically populated in production

    try {
        const response = await axios.post(`${TELEGRAM_API_URL}/setWebhook`, {
            url: webhookUrl
        });
        if (response.data.ok) {
            console.log('Webhook set successfully!');
        } else {
            console.error('Failed to set webhook:', response.data.description);
        }
    } catch (error) {
        console.error('Error setting webhook:', error);
    }
}

// Call setWebhook when the server starts
setWebhook();

// Handle Webhook Requests (Telegram sends updates to this endpoint)
app.post(`/bot${BOT_TOKEN}`, (req, res) => {
    console.log('Webhook received:', req.body);  // Debugging log
    bot.processUpdate(req.body);
    res.sendStatus(200);
});

// Define Bot Logic
bot.onText(/\/start/, (msg) => {
    bot.sendMessage(
        msg.chat.id,
        'Welcome! Send me a URL, and I will check if it’s a phishing link.'
    );
});

bot.on('message', async (msg) => {
    console.log('Received message:', msg); // Debugging log
    const chatId = msg.chat.id;
    const url = msg.text;

    if (url.startsWith('/')) return; // Ignore commands like /start

    try {
        console.log(`Checking URL: ${url}`); // Debugging log
        const response = await axios.get(API_URL, { params: { url } });
        const data = response.data;

        if (data.result) {
            bot.sendMessage(
                chatId,
                `⚠️ *Phishing Detected!*\n\n` +
                    `🔗 URL: ${data.url}\n` +
                    `🔀 Redirect URL: ${data.redirect_url}\n` +
                    `📊 Probability: ${data.phishing_probability}%\n`,
                { parse_mode: 'Markdown' }
            );
        } else {
            bot.sendMessage(chatId, '✅ This URL seems safe!');
        }
    } catch (error) {
        console.error('Error checking URL:', error); // Debugging log
        bot.sendMessage(chatId, '❌ Error checking the URL. Try again later.');
    }
});

// Start Express Server on Vercel
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
