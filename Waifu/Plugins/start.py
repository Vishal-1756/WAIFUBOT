import asyncio
from Waifu.Database.main import add_users_to_db, get_users_list
from pyrogram import filters, enums 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from Waifu import waifu
from Waifu import prefix

# Define your custom start message and extra text
start_message = "Welcome to the Waifu Bot! I can help you catch and collect waifus. Use /help to see available commands."
extra_text = "Feel free to explore the available commands and have fun!"

@waifu.on_message(filters.command("start", prefix) | filters.private)
async def start(_, message):
    user_id = int(message.from_user.id)
    mention = message.from_user.mention

    if message.chat.type == enums.ChatType.PRIVATE:
        # Check if the user is already in the database
        if user_id not in await get_users_list():
            await add_users_to_db(user_id)
        
        # Send the custom start message and extra text
        await message.reply_text(start_message + "\n\n" + extra_text)

# Additional code for other commands not shown, but you can keep it as you had before.
