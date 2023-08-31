from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Waifu import waifu

markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("OWNER", url="https://t.me/just_a_bio"),
     InlineKeyboardButton("SUPPORT", url="https://t.me/just_a_bio")]
])

caption = "TEAM-X WAIFU GRABBER STARTED"
photo = "https://telegra.ph/file/dc35ba52828e09744b3cc.jpg"

if __name__ == "__main__":
    waifu.run()
    with waifu:
        waifu.send_photo(chat_id=-1001849819947, photo=photo, caption=caption, reply_markup=markup)
