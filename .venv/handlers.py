from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

import database as db
import keyboards as kb

router = Router()


@router.message(Command("hello"))
async def start_handler(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!')


@router.message(Command("book"))
async def book_handler(msg: Message, bot: Bot):
    if msg.reply_to_message is None:
        await msg.reply("Эта команда должна быть ответом на объявление")
        return
    if msg.reply_to_message.from_user.id == msg.from_user.id:
        await msg.reply("Вы не можете забронировать собственное объявление")
        return
    con = await db.connect_to_db()
    await db.add_book(con, msg.reply_to_message.message_id, msg.from_user.id, int(msg.date.strftime("%Y%m%d%H%M%S")))
    await msg.reply("Запомнил вашу бронь")
    res = await db.get_first_for_offer(con, msg.reply_to_message.message_id)
    first_in_queue = await res.fetchall()
    if first_in_queue[0][0] == msg.from_user.id:
        await bot.send_message(
            msg.from_user.id,
            f"Вы первый в очереди! Свяжитесь с {msg.reply_to_message.from_user.first_name}!"
        )
        await bot.send_message(
            msg.reply_to_message.from_user.id,
            f"{msg.from_user.first_name} первый в очереди, свяжитесь с ним"
        )


@router.message(F.text.lower() == "да")
async def da_handler(msg: Message):
    await msg.reply("Пизда")


@router.message(Command("start"))
async def register_handler(msg: Message):
    con = await db.connect_to_db()
    await db.add_user(con, msg.from_user.id, msg.from_user.first_name)
    await msg.answer("Рад вас видеть")


@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(f'I\'m a bot for swapping things. Give me a link to your post in a swap chat and I\'ll help '
                         f'you track potential clients')


@router.message(Command("offer"))
async def offer_handler(msg: Message):
    con = await db.connect_to_db()
    await db.add_offer(con, msg.message_id, msg.from_user.id, msg.text.replace("/offer", ''))
    await msg.reply("Добавил ваше объявление в базу данных!")


@router.message(Command("mylist"))
async def list_handler(msg: Message, bot: Bot):
    con = await db.connect_to_db()
    res = await db.get_offers_list(con, msg.from_user.id)
    offers = await res.fetchall()
    reply = "Вот список ваших объявлений!\n"
    for i, offer in enumerate(offers):
        reply += f"{i+1}) {offer[0]}, id={offer[1]}\n"
    await bot.send_message(msg.from_user.id, reply)


@router.message(Command("drzj"))
async def dance_handler(msg: Message):
    await msg.answer_sticker(sticker='CAACAgIAAxkBAAELoy1l6p6q6VoUqY5lHx9YgUK0vodpNgACYygAApehcEghrDYNSgAB7Sc0BA')


@router.message()
async def general_handler(msg: Message):
    if msg.chat.type == "private":
        await msg.answer("What do you want?", reply_markup=kb.main_kb)


