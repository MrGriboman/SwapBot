from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

import database as db
import keyboards as kb
import utils

router = Router()


@router.message(Command("hello"))
async def start_handler(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!')


@router.message(Command("book"))
async def book_handler(msg: Message, bot: Bot):
    if msg.reply_to_message is None:
        await msg.reply("Эта команда должна быть ответом на объявление")
        return
    '''if msg.reply_to_message.from_user.id == msg.from_user.id:
        await msg.reply("Вы не можете забронировать собственное объявление")
        return'''
    con = await db.connect_to_db()
    the_offer = await db.offer_by_id(con, msg.reply_to_message.message_id)
    the_offer = await the_offer.fetchall()
    if not the_offer:
        await msg.reply("Это сообщение не объявление!")
        return
    await db.add_book(con, msg.reply_to_message.message_id, msg.from_user.id, int(msg.date.strftime("%Y%m%d%H%M%S")))
    await msg.reply("Запомнил вашу бронь")
    res = await db.get_first_for_offer(con, msg.reply_to_message.message_id)
    first_in_queue = await res.fetchall()
    if first_in_queue[0][0] == msg.from_user.id:
        await bot.send_message(
            msg.from_user.id,
            f"Вы первый в очереди! Свяжитесь с {await utils.resolve_user_name(msg.reply_to_message.from_user)}!"
        )
        await bot.send_message(
            msg.reply_to_message.from_user.id,
            f"{await utils.resolve_user_name(msg.from_user)} первый в очереди, свяжитесь с ним"
        )


@router.message(Command("start"))
async def register_handler(msg: Message):
    con = await db.connect_to_db()
    username = msg.from_user.username if msg.from_user.username is not None else None
    await db.add_user(con, msg.from_user.id, msg.from_user.first_name, username)
    await msg.answer("Рад вас видеть")


@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(f'I\'m a bot for swapping things. Give me a link to your post in a swap chat and I\'ll help '
                         f'you track potential clients')


@router.message(Command("offer"))
async def offer_handler(msg: Message):
    con = await db.connect_to_db()
    if msg.photo is None:
        await db.add_offer(con, msg.message_id, msg.from_user.id, msg.text.replace("/offer", ''))
    else:
        await db.add_offer(con, msg.message_id, msg.from_user.id, msg.caption.replace("/offer", ''))
    await msg.reply("Добавил ваше объявление в базу данных!")


@router.message(F.text.lower() == 'покажи мои объявления')
async def list_handler(msg: Message, bot: Bot):
    con = await db.connect_to_db()
    res = await db.get_offers_list(con, msg.from_user.id, 0)
    offers = await res.fetchall()
    reply = offers[0][0]
    offers_kb = kb.offers_kb(offers, 0).as_markup()
    await bot.send_message(msg.from_user.id, reply, reply_markup=offers_kb)


@router.message(F.text.lower() == 'покажи мои брони')
async def boklist_handler(msg: Message, bot: Bot):
    con = await db.connect_to_db()
    res = await db.get_books_list(con, msg.from_user.id, 0)
    print(msg.from_user.id)
    books = await res.fetchall()
    reply = books[0][0]
    books_kb = kb.books_kb(books, 0).as_markup()
    await bot.send_message(msg.from_user.id, reply, reply_markup=books_kb)


@router.message(Command("drzj"))
async def dance_handler(msg: Message):
    await msg.answer_sticker(sticker='CAACAgIAAxkBAAELoy1l6p6q6VoUqY5lHx9YgUK0vodpNgACYygAApehcEghrDYNSgAB7Sc0BA')


@router.callback_query(F.data.startswith('booklist'))
async def booklist_callback(callback: CallbackQuery):
    command = callback.data.split('_')
    action = command[1]
    if action == 'goforward':
        value = command[2]
        con = await db.connect_to_db()
        res = await db.get_books_list(con, callback.from_user.id, offset := int(value) + 1)
        books = await res.fetchall()
        print(books)
        books_kb = kb.books_kb(books, offset).as_markup()
        await callback.message.edit_text(books[0][0])
        await callback.message.edit_reply_markup(reply_markup=books_kb)
    if action == 'goback':
        value = command[2]
        con = await db.connect_to_db()
        res = await db.get_books_list(con, callback.from_user.id, offset := int(value) - 1)
        print(callback.from_user.id)
        books = await res.fetchall()
        books_kb = kb.books_kb(books, offset).as_markup()
        await callback.message.edit_text(books[0][0])
        await callback.message.edit_reply_markup(reply_markup=books_kb)
    if action == 'delete':
        offer, booker = command[2], command[3]
        con = await db.connect_to_db()
        await db.delete_book(con, offer, booker)
        res = await db.get_books_list(con, callback.from_user.id, 0)
        books = await res.fetchall()
        books_kb = kb.books_kb(books, 0).as_markup()
        await callback.message.edit_text(books[0][0])
        await callback.message.edit_reply_markup(reply_markup=books_kb)
    await callback.answer()


@router.callback_query(F.data.startswith('offerlist'))
async def offerlist_callback(callback: CallbackQuery):
    command = callback.data.split('_')
    action = command[1]
    if action == 'goforward':
        value = command[2]
        con = await db.connect_to_db()
        res = await db.get_offers_list(con, callback.from_user.id, offset := int(value) + 1)
        offers = await res.fetchall()
        offers_kb = kb.offers_kb(offers, offset).as_markup()
        await callback.message.edit_text(offers[0][0])
        await callback.message.edit_reply_markup(reply_markup=offers_kb)
    if action == 'goback':
        value = command[2]
        con = await db.connect_to_db()
        res = await db.get_offers_list(con, callback.from_user.id, offset := int(value) - 1)
        offers = await res.fetchall()
        offers_kb = kb.offers_kb(offers, offset).as_markup()
        await callback.message.edit_text(offers[0][0])
        await callback.message.edit_reply_markup(reply_markup=offers_kb)
    if action == 'delete':
        offer = command[2]
        con = await db.connect_to_db()
        await db.delete_offer(con, offer)
        res = await db.get_offers_list(con, callback.from_user.id, 0)
        offers = await res.fetchall()
        offers_kb = kb.offers_kb(offers, 0).as_markup()
        await callback.message.edit_text(offers[0][0])
        await callback.message.edit_reply_markup(reply_markup=offers_kb)
    if action == 'books':
        offer = command[2]
        con = await db.connect_to_db()
        res = await db.get_books_by_offer(con, offer, 0)
        books = await res.fetchall()
        books_kb = kb.books_kb(books, 0).as_markup()
        print(books)
        booker = await db.get_user_by_id(con, books[0][2])
        booker = await booker.fetchall()
        booker_name, booker_username = booker[0][1], booker[0][2]
        await callback.message.edit_text(f'Забронировавший:\nИмя: {booker_name}, Username: {booker_username}')
        await callback.message.edit_reply_markup(reply_markup=books_kb)
    await callback.answer()


@router.message()
async def general_handler(msg: Message):
    if msg.chat.type == "private":
        await msg.answer("Чем могу быть полезен?", reply_markup=kb.main_kb)
