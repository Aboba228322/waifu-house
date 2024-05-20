from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from sqlalchemy.orm import Session
from database import SessionLocal, User

async def profile_handler(message: types.Message):
    telegram_id = message.from_user.id
    username = message.from_user.username

    session: Session = SessionLocal()

    user = session.query(User).filter(User.telegram_id == telegram_id).first()

    if not user:
        user = User(telegram_id=telegram_id, username=username)
        session.add(user)
        session.commit()
        session.refresh(user)

    response_text = (f"Ваш профиль:\n"
                     f"ID: {user.id}\n"
                     f"Telegram ID: {user.telegram_id}\n"
                     f"Username: @{user.username}\n"
                     f"Оставшиеся запросы: {user.daily_requests}\n"
                     f"Статус подписки: {user.subscription_status}")

    await message.reply(response_text)

    session.close()

def register_handlers_profile(dp: Dispatcher):
    dp.register_message_handler(profile_handler, Text(equals="Профиль", ignore_case=True))
