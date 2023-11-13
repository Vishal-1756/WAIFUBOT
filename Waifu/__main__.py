from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Waifu import waifu

markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("OWNER", url="https://t.me/IkariS0_0"),
     InlineKeyboardButton("SUPPORT", url="https://t.me/IkariS0_0")]
])

caption = "WAIFU ADDER STARTED ADD WAIFUS IN DB"
photo = "https://telegra.ph/file/aa68b5d8185a9d5cadf63.jpg"

if __name__ == "__main__":
    waifu.run()
    with waifu:
        waifu.send_photo(chat_id=-1001849819947, photo=photo, caption=caption, reply_markup=markup)
