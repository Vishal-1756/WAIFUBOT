# Disign by :- @Team_devsX
# Created by :- @Ikaris0_0
# Api :- @Ikaris0_0

import requests
from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.enums import ChatType
from Waifu import waifu as pbot

@pbot.on_message(~filters.bot & ~filters.me & filters.text)
async def chatbot(_:Client,message:Message):
    if message.chat.type!= ChatType.PRIVATE:
        if not message.reply_to_message:
            return
        if message.reply_to_message.from_user.id != (await pbot.get_me()).id:
            return
    if message.text and message.text[0] in ["/", "!", "?", "."]:
        return
    response = requests.get("https://pervert-api.onrender.com/chatbot/{message.text}")
    if response.status_code == 200:
        data = response.json()['response']
        return await message.reply_text(data)
    elif response.status_code == 429:
        return await message.reply_text("ChatBot Error: Too many requests. Please wait a few moments.")
    elif response.status_code >= 500:
        return await message.reply_text("ChatBot Error: API server error. Contact us at @Ikaris0_0.")
    else:
        return await message.reply_text("ChatBot Error: Unknown Error Occurred. Contact us at @Ikaris0_0.")
