from pyrogram import filters
from Waifu.Database.main import get_chats_list, get_users_list
from Waifu import waifu

@waifu.on_message(filters.command("stats", prefixes="/"))
async def bot_stats(_, message):
    total_users = await get_users_count()
    total_chats = await get_chats_count()

    text = f"<b>Bot Statistics:</b>\n\n"
    text += f"**Total Users:** `{total_users}`\n"
    text += f"**Total Chats:** `{total_chats}`\n"

    await message.reply_text(text)

async def get_users_count():
    user_ids = await get_users_list()
    return len(user_ids)

async def get_chats_count():
    chats = await get_chats_list()
    return len(chats)
  
