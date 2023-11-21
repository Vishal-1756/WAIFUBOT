import asyncio
import random
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Waifu.Database.main import add_users_to_db, get_users_list, add_chat_to_db, get_chats_list
from Waifu import waifu
from Waifu import prefix

start_message = "Mᴏsʜɪ Mᴏsʜɪ {mention}\ɴTʜɪs ɪs ᴡᴀɪғᴜ ɢʀᴀʙʙᴇʀ/ᴄᴏʟʟᴇᴄᴛᴏʀ ʙᴏᴛ. Iᴛ's ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴄᴀᴛᴄʜ/ɢʀᴀʙ ʀᴀɴᴅᴏᴍ ᴡᴀɪғᴜs sᴘᴀᴡɴᴇᴅ ɪɴ ɢʀᴏᴜᴘ ᴄʜᴀᴛ.Fᴏʀ ᴍᴏʀᴇ Jᴏɪɴ: [Sᴜᴘᴘᴏʀᴛ](https://t.me/botsupportx)"
photo_links = [
    "https://telegra.ph/file/31544ca877fde042275ff.jpg",
    "https://telegra.ph/file/2e60670798b5b70458c67.jpg",
    "https://telegra.ph/file/95f92cefb8ec53ee0c625.jpg",
    "https://telegra.ph/file/3b5ebeeb66bdef64b87fd.jpg"
]

reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⤜ Sᴜᴘᴘᴏʀᴛ ⤛", url="https://t.me/botsupportx"),
                InlineKeyboardButton("⇜ Uᴘᴅᴀᴛᴇs ⇝", url="https://t.me/botupdatex")
            ],
            [
                InlineKeyboardButton("☊ Oᴡɴᴇʀ ☋", url="https://t.me/Ikaris0_0"),
                InlineKeyboardButton("☌ Cʀᴇᴅɪᴛs ☌", url="https://telegra.ph/𓆩Ꭰᥲʀκ𓆪-𖤍-11-20-2")
            ],
            [
                InlineKeyboardButton("+ Aᴅᴅ Mᴇ Iɴ Gʀᴏᴜᴘ +", url="https://t.me/Chat_Rank_Roobot?startgroup=true")
            ]
        ]
)


@waifu.on_message(filters.command("start", prefix))
async def start_command(_, message):
    chat_id = int(message.chat.id)
    mention = f"@{message.from_user.username}" if message.from_user.username else message.from_user.mention

    if message.chat.type == enums.ChatType.PRIVATE:
        user_id = int(message.from_user.id)
        photo_link = random.choice(photo_links)
        await message.reply_photo(photo=photo_link, caption=start_message.format(mention=mention), reply_markup=reply_markup)
        if user_id not in await get_users_list():
            await add_users_to_db(user_id)
    else:
        message.chat.type != enums.ChatType.PRIVATE:
        photo_link = random.choice(photo_links)
        await message.reply_photo(photo=photo_link, caption=start_message.format(mention=mention), reply_markup=reply_markup)
        if chat_id not in await get_chats_list():
            await add_chat_to_db(message.chat)
