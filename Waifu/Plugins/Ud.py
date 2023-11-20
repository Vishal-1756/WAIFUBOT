# Made By @Ikaris0_0
# Join Support:- @botsupportx
# Api By @Ikaris0_0

import requests
from pyrogram import filters
from pyrogram.types import Message
from Waifu import waifu, prefix
from pyrogram.enums import ParseMode

@waifu.on_message(filters.command("ud", prefix))
async def ud(_, message: Message):
    
    text = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None

    if not text:
        await message.reply("Please provide a word to define. Example: /ud <word>")
        return

    response = requests.get(f"https://pervert-api.onrender.com/ud?query={text}&max=2").json()

    try:
        results = response.get("results", [])
        if results:
            first_result = results[0]
            definition = first_result.get("definition", "")
            example = first_result.get("example", "")

            reply_text = f'**Word**: `{text}`\n\n**Definition**: `{definition}`\n\n**Example**: `{example}`'
        else:
            reply_text = f"No Results Found For Word: {text}"
    except (KeyError, IndexError):
        reply_text = "Error processing the API response."

    await message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)
