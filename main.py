from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_polling
import logging
import config
from handlers import profile, payment, referral, settings, chat
from database import init_db, SessionLocal, User

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
btn_profile = types.KeyboardButton("ℹ️Профиль")
btn_subscription = types.KeyboardButton("💲Оплатить подписку")
btn_referral = types.KeyboardButton("🤝Пригласить друга")
btn_settings = types.KeyboardButton("⚙️Настройки")
btn_chat = types.KeyboardButton("👧Девушки")
keyboard_markup.add(btn_profile, btn_subscription, btn_referral, btn_settings, btn_chat)

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    args = message.get_args()
    session = SessionLocal()

    telegram_id = message.from_user.id
    username = message.from_user.username

    referrer_id = None
    if args.isdigit():
        referrer_id = int(args)

    user = session.query(User).filter(User.telegram_id == telegram_id).first()

    if not user:
        user = User(telegram_id=telegram_id, username=username, referral_id=referrer_id)
        session.add(user)
        session.commit()
        session.refresh(user)

        if referrer_id:
            referrer_user = session.query(User).filter(User.id == referrer_id).first()
            if referrer_user:
                referrer_user.daily_requests += config.REFERRAL_BONUS
                session.commit()
                await message.reply(f"Вы получили бонус! {referrer_user.username} пригласил вас и получил 5 дополнительных запросов.")

    await message.reply("Добро пожаловать! Выберите действие:", reply_markup=keyboard_markup)

    session.close()

profile.register_handlers_profile(dp)
payment.register_handlers_payment(dp)
referral.register_handlers_referral(dp)
settings.register_handlers_settings(dp)
chat.register_handlers_chat(dp)

init_db()

if __name__ == '__main__':
    start_polling(dp, skip_updates=True)
