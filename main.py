import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# ====== CONFIGURATION ======
BOT_TOKEN = "7629093125:AAGOesJNygyr-iAbAWHIIDac6HvZxofKtYI"
GROUP_LINK = "https://t.me/+qcXP_M-I7aY2N2Y0"
PAYMENT_NAME = "shinetechnology"

# ====== USER DATA STORE ======
user_free_rounds = {}

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== COMMAND HANDLERS ======
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in user_free_rounds:
        user_free_rounds[user_id] = 5
    update.message.reply_text("Karibu! Utapata rounds 5 za bure za utabiri.")

def predict(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_free_rounds.get(user_id, 0) > 0:
        user_free_rounds[user_id] -= 1
        update.message.reply_text(f"Utabiri wako: Crash at 2.70x\nZimebaki: {user_free_rounds[user_id]}")
        if user_free_rounds[user_id] == 0:
            send_payment_options(update)
    else:
        send_payment_options(update)

def send_payment_options(update: Update):
    keyboard = [
        [InlineKeyboardButton("Lipa Kifurushi", callback_data="pay")],
    ]
    update.message.reply_text(
        "Umefikia kikomo cha free rounds.\nLipa ili kuendelea kutumia huduma.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "pay":
        keyboard = [
            [InlineKeyboardButton("Siku - 10,000 TZS", callback_data="pay_day")],
            [InlineKeyboardButton("Siku 3 - 20,000 TZS", callback_data="pay_3days")],
            [InlineKeyboardButton("Wiki - 30,000 TZS", callback_data="pay_week")],
            [InlineKeyboardButton("Mwezi - 50,000 TZS", callback_data="pay_month")],
            [InlineKeyboardButton("Miezi 3 - 120,000 TZS", callback_data="pay_3months")],
            [InlineKeyboardButton("Mwaka - 500,000 TZS", callback_data="pay_year")],
        ]
        query.edit_message_text("Chagua kifurushi:", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        handle_payment(query, query.data)

def handle_payment(query, package):
    price_map = {
        "pay_day": "10,000",
        "pay_3days": "20,000",
        "pay_week": "30,000",
        "pay_month": "50,000",
        "pay_3months": "120,000",
        "pay_year": "500,000"
    }
    price = price_map.get(package, "0")
    msg = f"""
Lipa {price} kwa jina la huduma *{PAYMENT_NAME}*.

Chagua mojawapo ya njia za malipo:
- Airtel: 0686823297
- Vodacom: 0756196420
- Tigo: 0654542433
- TTCL: 0613542433
- Bitcoin: bc1ql0x8j6rqcp5hr9x7hzts98phxsn84pmrvtla5s
- TRX (TRC20): TSgtTsmabWghWgXnYU765NG3HCKwmLkrtg
- USDT (ERC20/BEP20): 0x528581c64e39015b371b7d6b2f1a2605821c8170

Baada ya malipo, tuma screenshot kwa admin kuongezewa muda.
"""
    query.edit_message_text(msg, parse_mode="Markdown")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("predict", predict))
    dp.add_handler(CallbackQueryHandler(button_callback))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()