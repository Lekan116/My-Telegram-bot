from keep_alive import keep_alive
keep_alive()

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile, BotCommand

# === CONFIG ===
BOT_TOKEN = '7811176060:AAE6wUWQ_HSX8XP4Lgv98uZCpA0qm_YB16o'
ADMIN_ID = 738264476
BTC_ADDRESS = 'bc1qhw4h2p4jx7q48mg2sedkc5xws6sw6xtsl8rujh'
LTC_ADDRESS = 'LZzszQJdALyakT5Q662d935xCKMyd6ypmb'
ETH_ADDRESS = '0x8CF962Abd81997dE5598e23569E6107d75909C45'
USDT_ADDRESS = '0x8CF962Abd81997dE5598e23569E6107d75909C45'

bot = telebot.TeleBot(BOT_TOKEN)

# === SET COMMAND SUGGESTIONS ===
bot.set_my_commands([
    BotCommand("start", "Start the bot and view menu"),
    BotCommand("menu", "Show the country selection again"),
    BotCommand("checkbalance", "View crypto payment wallet addresses"),
    BotCommand("help", "How to use the bot & contact admin"),
])

# === START COMMAND ===
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🇺🇸 USA Leads", callback_data="usa"),
        InlineKeyboardButton("🇨🇦 Canada Leads", callback_data="canada"),
        InlineKeyboardButton("🇬🇧 UK Leads", callback_data="uk"),
        InlineKeyboardButton("🇫🇷 France Leads", callback_data="france"),
        InlineKeyboardButton("🇩🇪 Germany Leads", callback_data="germany"),
        InlineKeyboardButton("💬 Live Chat with Admin", callback_data="chat")
    )
    bot.send_message(
        message.chat.id,
        "👋 *Welcome to SMS LEAD BOT!*\n\nWe sell premium *SMS leads* only.\n\nEach country has its own pricing. Join our channel @canadasmsleads.\n\nWe accept *BTC*, *LTC*, *ETH*, and *USDT*.\n\nChoose your country below:",
        parse_mode="Markdown",
        reply_markup=markup
    )

# === HELP COMMAND ===
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "*📖 SMS Lead Bot Help Menu*\n\n"
        "*Available Commands:*\n"
        "🟢 /start - Start and show country menu\n"
        "🧭 /menu - Show country options again\n"
        "💸 /checkbalance - Wallets for payment\n"
        "📨 /help - Show this help message\n\n"
        "*How to Order:*\n"
        "1. Choose a country\n"
        "2. Pay using one of the wallet addresses\n"
        "3. Send screenshot, country, and quantity\n\n"
        "📬 Contact admin: [@streaks100](https://t.me/streaks100)"
    )
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

# === MENU COMMAND ===
@bot.message_handler(commands=['menu'])
def send_menu(message):
    send_welcome(message)

# === CALLBACK HANDLER ===
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    country_data = {
        "usa": "🇺🇸 *USA SMS Leads*\n💵 Price: $15 per 1,000 leads",
        "canada": "🇨🇦 *Canada SMS Leads*\n💵 Price: $15 per 1,000 leads",
        "uk": "🇬🇧 *UK SMS Leads*\n💵 Price: $15 per 1,000 leads",
        "france": "🇫🇷 *France SMS Leads*\n💵 Price: $15 per 1,000 leads",
        "germany": "🇩🇪 *Germany SMS Leads*\n💵 Price: $15 per 1,000 leads",
    }

    if call.data in country_data:
        msg = f"""{country_data[call.data]}

✅ *To order:*
1. Pay to one of the wallets below:

*BTC:*
`{BTC_ADDRESS}`

*LTC:*
`{LTC_ADDRESS}`

*ETH:*
`{ETH_ADDRESS}`

*USDT (ERC20):*
`{USDT_ADDRESS}`

2. Send payment screenshot, country, and quantity here.

⏳ Delivery is fast and private."""
        bot.send_message(call.message.chat.id, msg, parse_mode="Markdown")

    elif call.data == "chat":
        bot.send_message(
            call.message.chat.id,
            "📩 Send your message below and the admin will reply shortly."
        )
        username = call.from_user.username or f"id:{call.from_user.id}"
        bot.send_message(
            ADMIN_ID,
            f"👤 User @{username} started a live chat."
        )

# === SMART KEYWORDS REPLY ===
@bot.message_handler(func=lambda m: m.text and m.text.lower() in [
    "help", "order", "how to order", "buy", "leads", "price", "payment"
])
def smart_reply(message):
    bot.send_message(message.chat.id, "ℹ️ To order leads:\n1. Use /menu to pick a country\n2. Pay\n3. Send your screenshot & quantity here.")

# === FORWARD TO ADMIN ===
@bot.message_handler(func=lambda m: m.chat.id != ADMIN_ID and not m.text.startswith('/'))
def forward_all_messages(message):
    username = message.from_user.username or f"id:{message.from_user.id}"
    bot.send_message(ADMIN_ID, f"📨 Message from {message.chat.id} (@{username}):\n{message.text}")

# === ADMIN SEND MESSAGE ===
@bot.message_handler(commands=['send'])
def admin_send(message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        bot.reply_to(message, "Usage: /send <user_id> <message>")
        return
    user_id, msg_text = parts[1], parts[2]
    try:
        bot.send_message(int(user_id), f"📩 Admin: {msg_text}")
        bot.reply_to(message, "✅ Message sent.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

# === CHECK BALANCE ===
@bot.message_handler(commands=['checkbalance'])
def check_balance(message):
    msg = (
        "🧾 *Wallet Addresses:*\n\n"
        f"💰 *BTC:* `{BTC_ADDRESS}`\n"
        f"💸 *LTC:* `{LTC_ADDRESS}`\n"
        f"🪙 *ETH:* `{ETH_ADDRESS}`\n"
        f"💵 *USDT (ERC20):* `{USDT_ADDRESS}`\n\n"
        "🔎 Use explorers:\n"
        "- https://blockchair.com\n"
        "- https://etherscan.io\n"
        "- https://blockstream.info\n"
        "- https://tronscan.org"
    )
    bot.send_message(message.chat.id, msg, parse_mode="Markdown")

# === RUN BOT ===
bot.polling()
