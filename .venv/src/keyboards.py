from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Покажи мои объявления"),
            KeyboardButton(text="Покажи мои брони")
        ]
    ],
    resize_keyboard=True
)


def books_kb(books, offset):
    builder = InlineKeyboardBuilder()
    for book in books:
        builder.row(InlineKeyboardButton(
            text='Удалить',
            callback_data='booklist_delete_' + str(book[1]) + '_' + str(book[2])
            )
        )
    builder.row(
        InlineKeyboardButton(text='Назад', callback_data='booklist_goback_' + str(offset)),
        InlineKeyboardButton(text='Вперёд', callback_data='booklist_goforward_' + str(offset))
    )
    return builder


def offers_kb(offers, offset):
    builder = InlineKeyboardBuilder()
    for offer in offers:
        builder.row(
            InlineKeyboardButton(
                text='Список броней',
                callback_data='offerlist_books_' + str(offer[1])
            ),
            InlineKeyboardButton(
                text='Удалить',
                callback_data='offerlist_delete_' + str(offer[1])
            )
        )
    builder.row(
        InlineKeyboardButton(text='Назад', callback_data='offerlist_goback_' + str(offset)),
        InlineKeyboardButton(text='Вперёд', callback_data='offerlist_goforward_' + str(offset))
    )
    return builder
