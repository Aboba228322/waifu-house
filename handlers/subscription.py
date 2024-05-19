from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

BOOSTY_PAYMENT_URL = "https://boosty.to/test555777"

async def subscription_handler(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    btn_paypal = types.InlineKeyboardButton("PayPal", url="https://www.paypal.com")
    btn_credit_card = types.InlineKeyboardButton("Кредитная карта", url="https://www.yourcreditcardprocessor.com")
    btn_crypto = types.InlineKeyboardButton("Криптовалюта", url="https://www.yourcryptoprocessor.com")
    btn_boosty = types.InlineKeyboardButton("Boosty", url=BOOSTY_PAYMENT_URL)

    keyboard.add(btn_paypal, btn_credit_card, btn_crypto, btn_boosty)

    await message.reply("Выберите способ оплаты:", reply_markup=keyboard)

def register_handlers_subscription(dp: Dispatcher):
    dp.register_message_handler(subscription_handler, Text(equals="Оплатить подписку", ignore_case=True))
