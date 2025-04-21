from keep_alive import keep_alive
keep_alive()

import os
from dotenv import load_dotenv
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile, BotCommand

# === CONFIG ===
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
BTC_ADDRESS = os.getenv("BTC_ADDRESS")
LTC_ADDRESS = os.getenv("LTC_ADDRESS")
ETH_ADDRESS = os.getenv("ETH_ADDRESS")
USDT_ADDRESS = os.getenv("USDT_ADDRESS")

bot = telebot.TeleBot(BOT_TOKEN)

# === REPLY KEYBOARD FUNCTION ===
def main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🇨🇦 Canada SMS Leads", "🇺🇸 USA Leads")
    markup.row("💸 Payment Info", "🛒 Order Now")
    return markup

# === BOT COMMANDS ===
bot.set_my_commands([
    BotCommand("start", "Start the bot and view menu"),
    BotCommand("menu", "Show the country selection again"),
    BotCommand("checkbalance", "View crypto payment wallet addresses"),
    BotCommand("help", "How to use the bot & contact admin"),
])

# === /START and /MENU ===
@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🇺🇸 USA Leads", callback_data="usa"),
        InlineKeyboardButton("🇨🇦 Canada Leads", callback_data="canada"),
        InlineKeyboardButton("🇬🇧 UK Leads", callback_data="uk"),
        InlineKeyboardButton("🇫🇷 France Leads", callback_data="france"),
        InlineKeyboardButton("🇩🇪 Germany Leads", callback_data="germany"),
        InlineKeyboardButton("📋 Smart Commands", callback_data="smart"),
        InlineKeyboardButton("💬 Live Chat with Admin", callback_data="chat")
    )
    bot.send_message(
        message.chat.id,
        "👋 *Welcome to SMS LEAD BOT!*\n\nWe sell premium *SMS leads* only. Each country has its own pricing.\n\nJoin our channel @canadasmsleads. We accept:\n₿ *BTC*, Ł *LTC*, Ξ *ETH*, and 💲*USDT*.\n\nChoose your country below:",
        parse_mode="Markdown",
        reply_markup=markup
    )

# === CALLBACK HANDLER ===
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    country_data = {
        "usa": "🇺🇸 *USA SMS Leads*\n💰 Price: $15 per 1,000 leads",
        "canada": "🇨🇦 *Canada SMS Leads*\n💰 Price: $15 per 1,000 leads",
        "uk": "🇬🇧 *UK SMS Leads*\n💰 Price: $15 per 1,000 leads",
        "france": "🇫🇷 *France SMS Leads*\n💰 Price: $15 per 1,000 leads",
        "germany": "🇩🇪 *Germany SMS Leads*\n💰 Price: $15 per 1,000 leads",
    }

    if call.data in country_data:
        msg = f"""{country_data[call.data]}

🛒 *To order:*
1️⃣ Pay to one of the wallets below:

₿ *BTC:* `{BTC_ADDRESS}`
Ł *LTC:* `{LTC_ADDRESS}`
Ξ *ETH:* `{ETH_ADDRESS}`
💲 *USDT (ERC20):* `{USDT_ADDRESS}`

2️⃣ Send payment screenshot, country, and quantity here.

⚡ Delivery is fast and private."""
        bot.send_message(call.message.chat.id, msg, parse_mode="Markdown")

    elif call.data == "chat":
        bot.send_message(call.message.chat.id, "💬 Send your message below and the admin will reply shortly.")
        bot.send_message(ADMIN_ID, f"👤 User @{call.from_user.username or call.from_user.id} started a live chat.")

    elif call.data == "smart":
        smart_text = (
            "📋 *Smart Commands & Keywords:*\n\n"
            "📎 */start* — Show main menu\n"
            "📎 */menu* — Country lead options\n"
            "📎 */checkbalance* — Wallet addresses\n"
            "📎 */help* — How to order & support\n\n"
            "💬 Smart keywords (just type):\n"
            "`help`, `order`, `buy`, `leads`, `price`, `payment`\n\n"
            "Bot will auto-reply when you use any of these."
        )
        bot.send_message(call.message.chat.id, smart_text, parse_mode="Markdown")

# === /HELP COMMAND ===
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "📖 *SMS Lead Bot Help Menu*\n\n"
        "💡 Commands:\n"
        "/start - Start and show country menu\n"
        "/menu - Show country options again\n"
        "/checkbalance - Wallets for payment\n"
        "/help - Show this help message\n\n"
        "🛒 *To order:*\n"
        "1️⃣ Choose a country\n"
        "2️⃣ Pay using the wallet address\n"
        "3️⃣ Send screenshot & order details\n\n"
        "📬 Contact admin: [@streaks100](https://t.me/streaks100)"
    )
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

# === /CHECKBALANCE COMMAND ===
@bot.message_handler(commands=['checkbalance'])
def check_balance(message):
    msg = (
        "💳 *Wallet Addresses:*\n\n"
        f"₿ *BTC:* `{BTC_ADDRESS}`\n"
        f"Ł *LTC:* `{LTC_ADDRESS}`\n"
        f"Ξ *ETH:* `{ETH_ADDRESS}`\n"
        f"💲 *USDT (ERC20):* `{USDT_ADDRESS}`\n\n"
        "🧾 Use explorers to verify:\n"
        "- https://blockchair.com\n"
        "- https://etherscan.io\n"
        "- https://blockstream.info\n"
        "- https://tronscan.org"
    )
    bot.send_message(message.chat.id, msg, parse_mode="Markdown")

# === SMART KEYWORDS AUTO REPLY ===
@bot.message_handler(func=lambda message: message.text and message.text.lower() in ["help", "order", "how to order", "buy", "leads", "price", "payment"])
def smart_reply(message):
    bot.send_message(message.chat.id, "🛒 Use /menu to pick a country, pay to the wallet, and send proof here. Admin will reply fast ⚡")

# === FORWARD ALL NON-ADMIN MESSAGES ===
@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID and not message.text.startswith('/'))
def forward_all_messages(message):
    bot.send_message(ADMIN_ID, f"📨 Message from {message.chat.id} (@{message.from_user.username}):\n{message.text}")

# === ADMIN TEXT REPLY TO USER ===
@bot.message_handler(commands=['send'])
def admin_send(message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        bot.reply_to(message, "⚠️ Usage: /send <user_id> <message>")
        return
    user_id, msg_text = parts[1], parts[2]
    try:
        bot.send_message(int(user_id), f"📩 Admin:\n{msg_text}")
        bot.reply_to(message, "✅ Message sent.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

# === ADMIN FILE TO USER ===
@bot.message_handler(commands=['file'])
def send_file(message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3 or not message.reply_to_message or not message.reply_to_message.document:
        bot.reply_to(message, "⚠️ Reply to a file with:\n/file <user_id> <filename>")
        return
    user_id, filename = parts[1], parts[2]
    try:
        file_info = bot.get_file(message.reply_to_message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        bot.send_document(int(user_id), InputFile(downloaded_file, filename), caption="📁 File from Admin")
        bot.reply_to(message, "✅ File sent.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error sending file: {e}")

# === FALLBACK DYNAMIC MENU ===
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    text = message.text

    if text == "🇨🇦 Canada SMS Leads":
        bot.send_message(
            message.chat.id,
            "🇨🇦 Canada SMS Leads:\n• Fresh leads\n• High engagement\n• Price: $15 per 1,000"
        )

    elif text == "🇺🇸 USA Leads":
        bot.send_message(
            message.chat.id,
            "🇺🇸 USA Leads:\n• SMS + Email\n• Price: $15 per 1,000"
        )

    elif text == "💸 Payment Info":
        bot.send_message(
            message.chat.id,
            f"💳 Payment Wallets:\n\n₿ BTC: `{BTC_ADDRESS}`\nŁ LTC: `{LTC_ADDRESS}`\nΞ ETH: `{ETH_ADDRESS}`\n💲 USDT: `{USDT_ADDRESS}`\n\nSend proof here after payment.",
            parse_mode="Markdown"
        )

    elif text == "🛒 Order Now":
        bot.send_message(message.chat.id, "🛒 Please send your lead type and quantity. We will confirm and deliver fast.")
        bot.send_message(ADMIN_ID, f"🛍️ New order interest from @{message.from_user.username or message.from_user.first_name}: {text}")

    else:
        bot.send_message(
            message.chat.id,
            "❗ Unrecognized command. Please use one of the options below.",
            reply_markup=main_menu()
        )

# === RUN THE BOT ===
bot.infinity_polling()
