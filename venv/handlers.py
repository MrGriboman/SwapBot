from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command

import database as db

router = Router()


@router.message(Command("hello"))
async def start_handler(message: Message):
    await message.answer(f'Hi there, {message.from_user.first_name}!')


@router.message(F.text.lower() == "да")
async def da_handler(msg: Message):
    await msg.reply("Пизда")


@router.message(Command("register"))
async def register_handler(msg: Message):
    con = await db.connect_to_db()
    await db.add_user(con, msg.from_user.id, msg.from_user.first_name)


@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(f'I\'m a bot for swapping things. Give me a link to your post in a swap chat and I\'ll help '
                         f'you track potential clients')


@router.message(Command("offer"))
async def offer_handler(msg: Message):
    con = await db.connect_to_db()
    await db.add_offer(con, msg.message_id, msg.from_user.id)
    await msg.reply("Added your offer to my database!")


@router.message(Command("drzj"))
async def dance_handler(msg: Message):
    await msg.answer_sticker(sticker='CAACAgIAAxkBAAELoy1l6p6q6VoUqY5lHx9YgUK0vodpNgACYygAApehcEghrDYNSgAB7Sc0BA')


