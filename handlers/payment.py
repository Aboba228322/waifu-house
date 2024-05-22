import hashlib
from datetime import datetime
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
from database import SessionLocal, User
from sqlalchemy.orm import Session

def get_payment_url(user_id, amount, requests_count):
    order_id = f"{user_id}_{int(datetime.utcnow().timestamp())}"
    sign_data = f"{config.MERCHANT_ID}:{amount}:{config.SECRET_WORD_1}:RUB:{order_id}"
    sign = hashlib.md5(sign_data.encode()).hexdigest()

    return (f"https://pay.freekassa.ru/?m={config.MERCHANT_ID}&oa={amount}&currency=RUB&o={order_id}&s={sign}"
            f"&us_user_id={user_id}&us_requests_count={requests_count}"), sign_data, sign

async def payment_handler(message: types.Message):
    telegram_id = message.from_user.id
    amount = 100.00
    requests_count = 50

    session: Session = SessionLocal()
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id, username=message.from_user.username)
        session.add(user)
        session.commit()

    payment_url, sign_data, sign = get_payment_url(user.id, amount, requests_count)
    keyboard_markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton("Оплатить", url=payment_url)]]
    )

    await message.reply(
        f"Для оплаты нажмите на кнопку ниже:\n\n"
        f"Sign Data: {sign_data}\n"
        f"Signature: {sign}",
        reply_markup=keyboard_markup
    )

def register_handlers_payment(dp: Dispatcher):
    dp.register_message_handler(payment_handler, Text(equals="💲Оплатить подписку", ignore_case=True))
