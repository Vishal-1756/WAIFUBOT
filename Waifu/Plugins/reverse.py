import requests
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Waifu import waifu as pbot
from Waifu import bot_token as TOKEN

API_URL = "https://gglimg.vercel.app/reverse"

async def get_file_id_from_message(message: Message):
    file_id = None
    message = message.reply_to_message
    if not message:
        return None
    if message.document:
        if int(message.document.file_size) > 3145728:
            return
        mime_type = message.document.mime_type
        if mime_type not in ("image/png", "image/jpeg"):
            return
        file_id = message.document.file_id

    if message.sticker:
        if message.sticker.is_animated:
            if not message.sticker.thumbs:
                return
            file_id = message.sticker.thumbs[0].file_id
        else:
            file_id = message.sticker.file_id

    if message.photo:
        file_id = message.photo.file_id

    if message.animation:
        if not message.animation.thumbs:
            return
        file_id = message.animation.thumbs[0].file_id

    if message.video:
        if not message.video.thumbs:
            return
        file_id = message.video.thumbs[0].file_id
    return file_id

@pbot.on_message(filters.command(["pp", "grs", "reverse"]))
async def reverse(client: Client, message: Message):
    text = await message.reply_text("`Parsing Media...`")  # Simple text
    file_id = await get_file_id_from_message(message)
    if not file_id:
        return await text.edit("`Reply to a Photo or sticker`")  # Simple text
    await text.edit("`Searching...`")  # Simple text

    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}"
    ).json()
    file_path = r["result"]["file_path"]

    data = {
        "imageUrl": f"https://images.google.com/searchbyimage?safe=off&sbisrc=tg&image_url=https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    }

    response = requests.post(API_URL, json=data)

    if response.status_code == 200:
        result = response.json()["data"]
        return await text.edit(
            f'Sauce: {result["output"]}',  # Simple text
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Link", url=result["similar"])]]
            ),
        )
    elif response.status_code == 401:
        return await text.edit("`Couldn't find anything`")  # Simple text
    elif response.status_code == 402:
        return await text.edit("`Failed to reverse image`")  # Simple text
    elif response.status_code <= 500:
        return await text.edit("`Error in API`")  # Simple text
    else:
        return await text.edit("`Unknown Error Occurred`")  # Simple text
