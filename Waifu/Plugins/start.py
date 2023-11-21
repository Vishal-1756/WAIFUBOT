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

@waifu.on_message(filters.command("start", prefix) & filters.private)
async def start_private(_, message):
    user_id = int(message.from_user.id)
    mention = message.from_user.mention

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

    photo_link = random.choice(photo_links)

    # Check if the user is already in the database
    if user_id not in await get_users_list():
        await add_users_to_db(user_id)

    await waifu.send_photo(chat_id=message.chat.id, photo=photo_link, caption=start_message.format(mention=mention), reply_markup=reply_markup)


@waifu.on_message(filters.command("start", prefix) & filters.group)
async def start_group(_, message):
    chat_id = int(message.chat.id)
    mention = message.from_user.mention

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⤜ Sᴜᴘᴘᴏʀᴛ ⤛", url="https://t.me/botsupportx"),
                InlineKeyboardButton("⇜ UᴘᴅᴀᴛᴇS ⇝", url="https://t.me/botupdatex")
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

    photo_link = random.choice(photo_links)

    # Check if the chat is already in the database
    if chat_id not in await get_chats_list():
        await add_chat_to_db(message.chat)

    await waifu.send_photo(chat_id=message.chat.id, photo=photo_link, caption=start_message.format(mention=mention), reply_markup=reply_markup)
