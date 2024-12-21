require('dotenv').config();
const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');
const express = require('express');

const BOT_TOKEN = process.env.BOT_TOKEN;
const API_URL = 'https://teleservicesapi.vercel.app/check-phishing';
const bot = new TelegramBot(BOT_TOKEN);
const app = express();

app.use(express.json());

// Set Webhook
bot.setWebHook(`https://your-vercel-deployment-url.vercel.app/bot${BOT_TOKEN}`);

// Handle Webhook
app.post(`/bot${BOT_TOKEN}`, (req, res) => {
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
    const chatId = msg.chat.id;
    const url = msg.text;

    if (url.startsWith('/')) return;

    try {
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
        bot.sendMessage(chatId, '❌ Error checking the URL. Try again later.');
    }
});

// Start Express Server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
