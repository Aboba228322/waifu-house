# handlers/chat.py

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils import load_prompt, get_chatgpt_response
from sqlalchemy.orm import Session
from datetime import datetime
from database import SessionLocal, User


class ChatStates(StatesGroup):
    choosing_girl = State()
    chatting = State()


user_conversations = {}

async def choose_girl_handler(message: types.Message):
    keyboard_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_anna = KeyboardButton("Анна")
    btn_ekaterina = KeyboardButton("Екатерина")
    btn_maria = KeyboardButton("Мария")
    btn_back = KeyboardButton("Назад в меню")
    keyboard_markup.add(btn_anna, btn_ekaterina, btn_maria)
    keyboard_markup.add(btn_back)

    response_text = "Выберите девушку для общения:"
    await message.reply(response_text, reply_markup=keyboard_markup)
    await ChatStates.choosing_girl.set()

async def start_chat_handler(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    user_choice = message.text.lower()

    if user_choice in ["анна", "екатерина", "мария"]:
        async with state.proxy() as data:
            data['prompt_file'] = f"{user_choice}.txt"

        user_conversations[telegram_id] = [{"role": "system", "content": load_prompt(f"{user_choice}.txt")}]
        await message.reply(f"Вы начали общение с {user_choice.capitalize()}! Напишите ей что-нибудь.")
        await ChatStates.chatting.set()
    elif user_choice == "назад в меню":
        await exit_to_menu(message, state)
    else:
        await message.reply("Пожалуйста, выберите девушку для общения или нажмите 'Назад в меню'.")

async def chat_handler(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад в меню":
        await exit_to_menu(message, state)
        return

    telegram_id = message.from_user.id

    session: Session = SessionLocal()
    user = session.query(User).filter(User.telegram_id == telegram_id).first()

    if not user:
        user = User(telegram_id=telegram_id, username=message.from_user.username)
        session.add(user)
        session.commit()
        session.refresh(user)

    if user.daily_requests <= 0:
        await message.reply("Извините, вы исчерпали дневной лимит запросов.")
        await exit_to_menu(message, state)
        return

    async with state.proxy() as data:
        if 'prompt_file' not in data:
            await message.reply("Пожалуйста, выберите девушку для общения.")
            await ChatStates.choosing_girl.set()
            return


        user_conversations[telegram_id].append({"role": "user", "content": message.text})


        response_text = get_chatgpt_response(user_conversations[telegram_id])


        user_conversations[telegram_id].append({"role": "assistant", "content": response_text})


        user.daily_requests -= 1
        user.last_request_date = datetime.utcnow()
        session.add(user)
        session.commit()

        await message.reply(response_text)

async def exit_to_menu(message: types.Message, state: FSMContext):
    await state.finish()

    keyboard_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_profile = KeyboardButton("Профиль")
    btn_subscription = KeyboardButton("Оплатить подписку")
    btn_referral = KeyboardButton("Пригласить друга")
    btn_settings = KeyboardButton("Настройки")
    btn_chat = KeyboardButton("Девушки")
    keyboard_markup.add(btn_profile, btn_subscription, btn_referral, btn_settings, btn_chat)


    telegram_id = message.from_user.id
    if telegram_id in user_conversations:
        del user_conversations[telegram_id]

    await message.reply("Вы вернулись в главное меню. Выберите действие:", reply_markup=keyboard_markup)

def register_handlers_chat(dp: Dispatcher):
    dp.register_message_handler(choose_girl_handler, Text(equals="Девушки", ignore_case=True), state="*")
    dp.register_message_handler(start_chat_handler, state=ChatStates.choosing_girl)
    dp.register_message_handler(chat_handler, state=ChatStates.chatting)
    dp.register_message_handler(exit_to_menu, Text(equals="Назад в меню", ignore_case=True), state="*")
