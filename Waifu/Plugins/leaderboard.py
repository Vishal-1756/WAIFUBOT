from pyrogram import enum, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Database.main import get_top_harem_groups, get_chat_top_harem_users
from Waifu import waifu



@waifu.on_message(filters.command("globaltop", prefixes="/"))
async def global_top(_, message):
    limit = 5  # You can adjust the limit as needed
    top_groups = await get_top_harem_groups(limit)

    if top_groups:
        text = "<b>Global Top Waifu Groups:</b>\n"
        for i, group in enumerate(top_groups, start=1):
            text += f"{i}. <b>Chat ID:</b> {group['chat_id']} | <b>Waifu Count:</b> {group['waifu_count']}\n"

        await message.reply_text(text, parse_mode="html")
    else:
        await message.reply_text("No data available for global top waifu groups.")

@waifu.on_message(filters.command("top", prefixes="/"))
async def chat_top(_, message):
    limit = 5  # You can adjust the limit as needed
    chat_id = message.chat.id
    top_users = await get_chat_top_harem_users(chat_id, limit)

    if top_users:
        text = "<b>Top Waifu Users in this Chat:</b>\n"
        for i, user in enumerate(top_users, start=1):
            user_id = user["user_id"]
            waifu_count = user["waifu_count"]
            mention = f"<a href='tg://user?id={user_id}'>User</a>"
            text += f"{i}. {mention} | <b>Waifu Count:</b> {waifu_count}\n"

        await message.reply_text(text, parse_mode="html")
    else:
        await message.reply_text("No data available for top waifu users in this chat.")
      
