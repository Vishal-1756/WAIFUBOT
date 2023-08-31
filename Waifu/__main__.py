from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Bot import bot

markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("Oᗯᑎᗴᖇ", url="https://t.me/just_a_bio"),
     InlineKeyboardButton("ՏᑌᑭᑭOᖇT", url="https://t.me/just_a_bio")]
])

caption = "YᗩI ᗰIKO ՏTᗩᖇTᗴᗪ ՏᑌᑕᑕᗴՏՏᖴᑌᒪᒪY"
photo = "https://telegra.ph/file/dc35ba52828e09744b3cc.jpg"
GROUP = "-1001964645198"

if __name__ == "__main__":
    bot.run()
    with bot:
        bot.send_photo(chat_id=-1001964645198, photo=photo, caption=caption, reply_markup=markup)
