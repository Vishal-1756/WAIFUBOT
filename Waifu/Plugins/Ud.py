import requests
from pyrogram import filters
from pyrogram.types import Message
from Waifu import waifu, prefix
from pyrogram.enums import ParseMode

@waifu.on_message(filters.command("ud", prefix))
async def ud(_, message: Message):
    # Extract the word to define from the user's message
    text = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None

    if not text:
        await message.reply("Please provide a word to define. Example: /ud <word>")
        return

    # Get the definition and examples for the provided word
    response = requests.get(f"https://pervert-api.onrender.com/ud?query={text}&max=2").json()

    try:
        results = response.get("results", [])
        if results:
            # Extracting the first result
            first_result = results[0]
            definition = first_result.get("definition", "")
            example = first_result.get("example", "")

            reply_text = f'*{text}*\n\n{definition}\n\n_{example}_'
        else:
            reply_text = "No results found."
    except (KeyError, IndexError):
        reply_text = "Error processing the API response."

    await message.reply_text(reply_text, parse_mode=Parsemode.MARKDOWN)
