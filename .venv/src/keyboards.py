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


def offers_kb(offers):
    builder = InlineKeyboardBuilder()
    for offer in offers:
        builder.row(InlineKeyboardButton(
            text=offer[0],
            callback_data=str(offer[1]))
        )
    builder.row(
        InlineKeyboardButton(text='Назад', callback_data='go_back'),
        InlineKeyboardButton(text='Вперёд', callback_data='go_forward')
    )
    return builder
