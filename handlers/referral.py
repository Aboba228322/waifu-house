from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from sqlalchemy.orm import Session
from database import SessionLocal, User

async def referral_handler(message: types.Message):
    telegram_id = message.from_user.id
    session: Session = SessionLocal()
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id, username=message.from_user.username)
        session.add(user)
        session.commit()
        session.refresh(user)
    bot_info = await message.bot.get_me()
    referral_link = f"https://t.me/{bot_info.username}?start={user.id}"
    response_text = f"Ваша реферальная ссылка: {referral_link}\nПригласите друга и получите бонус!"
    await message.reply(response_text)
    session.close()

def register_handlers_referral(dp: Dispatcher):
    dp.register_message_handler(referral_handler, Text(equals="🤝Пригласить друга", ignore_case=True))
