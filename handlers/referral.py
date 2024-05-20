from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

async def referral_handler(message: types.Message):
    referral_link = f"https://t.me/Waifu_Town_AI_Bot?start={message.from_user.id}"
    response_text = f"Ваша реферальная ссылка: {referral_link}\nПригласите друга и получите бонус!"
    await message.reply(response_text)

def register_handlers_referral(dp: Dispatcher):
    dp.register_message_handler(referral_handler, Text(equals="Пригласить друга", ignore_case=True))
