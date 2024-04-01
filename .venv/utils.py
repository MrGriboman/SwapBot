from aiogram import types


async def resolve_user_name(user):
    return user.first_name if user.username is None else '@'+user.username


async def in_group(message):
    return message.chat.type in (
        types.ChatType.GROUP,
        types.ChatType.SUPER_GROUP,
    )
