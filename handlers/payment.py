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
    sign = hashlib.md5(f"{config.MERCHANT_ID}:{amount}:{config.SECRET_WORD_1}:{order_id}".encode()).hexdigest()
    return (f"https://pay.freekassa.ru/?m={config.MERCHANT_ID}&oa={amount}¤cy=RUB&o={order_id}&s={sign}"
            f"&us_user_id={user_id}&us_requests_count={requests_count}")

async def payment_handler(message: types.Message):
    telegram_id = message.from_user.id
    amount = 100
    requests_count = 50

    session: Session = SessionLocal()
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id, username=message.from_user.username)
        session.add(user)
        session.commit()

    payment_url = get_payment_url(user.id, amount, requests_count)
    keyboard_markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton("Оплатить", url=payment_url)]]
    )

    await message.reply("Для оплаты нажмите на кнопку ниже:", reply_markup=keyboard_markup)

def register_handlers_payment(dp: Dispatcher):
    dp.register_message_handler(payment_handler, Text(equals="Оплатить подписку", ignore_case=True))
