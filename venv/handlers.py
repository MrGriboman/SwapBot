from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
import datetime

import database as db

router = Router()


@router.message(Command("hello"))
async def start_handler(message: Message):
    await message.answer(f'Hi there, {message.from_user.first_name}!')


@router.message(Command("book"))
async def book_handler(msg: Message, bot: Bot):
    con = await db.connect_to_db()
    await db.add_book(con, msg.reply_to_message.message_id, msg.from_user.id, int(msg.date.strftime("%Y%m%d%H%M%S")))
    await msg.reply("Remembered your booking!")
    res = await db.get_first_for_offer(con, msg.reply_to_message.message_id)
    first_in_queue = await res.fetchall()
    if first_in_queue[0][0] == msg.from_user.id:
        await bot.send_message(
            msg.from_user.id,
            f"You're the first in the queue, contact {msg.reply_to_message.from_user.first_name}!"
        )
        await bot.send_message(
            msg.reply_to_message.from_user.id,
            f"{msg.from_user.first_name} is the first in the queue, contact them!"
        )


@router.message(F.text.lower() == "да")
async def da_handler(msg: Message):
    await msg.reply("Пизда")


@router.message(Command("start"))
async def register_handler(msg: Message):
    con = await db.connect_to_db()
    await db.add_user(con, msg.from_user.id, msg.from_user.first_name)
    await msg.answer("Glad to see you!")


@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(f'I\'m a bot for swapping things. Give me a link to your post in a swap chat and I\'ll help '
                         f'you track potential clients')


@router.message(Command("offer"))
async def offer_handler(msg: Message):
    con = await db.connect_to_db()
    await db.add_offer(con, msg.message_id, msg.from_user.id, msg.text.replace("/offer", ''))
    await msg.reply("Added your offer to my database!")


@router.message(Command("mylist"))
async def list_handler(msg: Message, bot: Bot):
    con = await db.connect_to_db()
    res = await db.get_offers_list(con, msg.from_user.id)
    offers = await res.fetchall()
    reply = "Here's the list of your offers!\n"
    for i, offer in enumerate(offers):
        reply += f"{i+1}) {offer[0][0]}\n"
    await bot.send_message(msg.from_user.id, reply)


@router.message(Command("drzj"))
async def dance_handler(msg: Message):
    await msg.answer_sticker(sticker='CAACAgIAAxkBAAELoy1l6p6q6VoUqY5lHx9YgUK0vodpNgACYygAApehcEghrDYNSgAB7Sc0BA')


