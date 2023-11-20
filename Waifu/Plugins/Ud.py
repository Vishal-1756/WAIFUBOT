import requests
from pyrogram import filters, enums
from pyrogram.types import Message
from Waifu import waifu, prefix

@waifu.on_message(filters.command("ud", prefix))
async def ud(_, message: Message):
    # Extract the word to define from the user's message
    text = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None

    if not text:
        await message.reply("Please provide a word to define. Example: /ud ")
        return

    # Get the definition and examples for the provided word
    results = requests.get(f"https://pervert-api.onrender.com/ud?query={text}&max=2").json()

    try:
        reply_text = f'*{text}*\n\n{results["definition"]}\n\n_{results["example"]}_'
    except (KeyError, IndexError):
        reply_text = "No results found."

    await message.reply_text(reply_text, parse_mode=enums.Parsemode.MARKDOWN)
