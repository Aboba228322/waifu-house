from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
import config

async def payment_handler(message: types.Message):
    response_text = f"Для оплаты через Boosty, перейдите по следующей ссылке: {config.BOOSTY_URL}"
    await message.reply(response_text)

def register_handlers_payment(dp: Dispatcher):
    dp.register_message_handler(payment_handler, Text(equals="Оплатить подписку", ignore_case=True))
