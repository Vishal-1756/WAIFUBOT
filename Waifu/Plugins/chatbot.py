# Disign by :- @Team_devsX
# Created by :- @Ikaris0_0
# Api :- @Ikaris0_0

import requests
from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.enums import ChatType
import json
from Waifu import waifu as pbot

@pbot.on_message(filters.text & ~filters.bot & ~filters.me)
async def chatbot(_, message: Message):
    if message.chat.type != ChatType.PRIVATE:
        if not message.reply_to_message:
            return
        if message.reply_to_message.from_user.id != (await pbot.get_me()).id:
            return

    if message.text and message.text[0] in ["/", "!", "?", "."]:
        return

    response = requests.get(f"https://pervert-api.onrender.com/chatbot/{message.text}")

    if response.status_code == 200:
        try:
            results = response.json()
            await message.reply_text(results.get("reply", "No reply from the chatbot."))
        except json.JSONDecodeError:
            await message.reply_text("Failed to decode the chatbot response.")
    elif response.status_code == 429:
        await message.reply_text("ChatBot Error: Too many requests. Please wait a few moments.")
    elif response.status_code >= 500:
        await message.reply_text("ChatBot Error: API server error. Contact us at @Ikaris0_0.")
    else:
        await message.reply_text(f"ChatBot Error: Unknown Error Occurred. Contact us at @Ikaris0_0.")
