from aiogram.types import(
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Покажи мои объявления"),
            KeyboardButton(text="Покажи мои брони")
        ]
    ],
    resize_keyboard=True
)