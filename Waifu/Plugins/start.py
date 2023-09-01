import asyncio
from Waifu.Database.main import add_users_to_db, get_users_list
from pyrogram import filters, enums 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from Waifu import waifu
from Waifu import prefix

@waifu.on_message(filters.command("start", prefix) | filters.private)
async def start(_, message):
    user_id = int(message.from_user.id)
    mention = message.from_user.mention

    if message.chat.type == enums.ChatType.PRIVATE:
        # Check if the user is already in the database
        if user_id not in await get_users_list():
            await add_users_to_db(user_id)


