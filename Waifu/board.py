from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Waifu import waifu



# Define a handler for the /top or /leader command
@waifu.on_message(filters.command(["top", "leader"], prefixes="/"))
async def top_command(_, message):
    # Get the top users with the most waifus from your database
    top_users = await get_top_users(limit=10)  # Adjust the limit as needed

    if not top_users:
        await message.reply("The leaderboard is empty!")
        return

    # Prepare a message with the top users and chat name (if available)
    chat_name = message.chat.title
    chat_username = message.chat.username
    chat_photo = message.chat.photo.big_file_id if message.chat.photo else None

    leaderboard_message = f"Top Users in {chat_name}:\n" if chat_name else "Top Users:\n"

    for rank, user in enumerate(top_users, start=1):
        leaderboard_message += f"{rank}. {user['username']} - {user['waifu_count']} waifus\n"

    # Send the leaderboard message with chat name and/or chat photo
    await message.reply_photo(
        photo=chat_photo,
        caption=leaderboard_message,
        reply_markup=None if chat_username else InlineKeyboardMarkup(
            [[InlineKeyboardButton("Join Chat", url=f"https://t.me/{chat_username}")]]
        )
    )
  
