from pyrogram import Client, filters, types
from telegraph import upload_file
from json import JSONDecodeError
import requests
from Waifu import waifu as app

API_URL = "https://reverse-pbq1.onrender.com/reverse?url={url}"
API_URL_BING = "https://api.qewertyy.me/image-reverse/bing?img_url={url}"
API_URL_GOOGLE = "https://api.qewertyy.me/image-reverse/bing?img_url={url}"

async def telegraph(message, path):
    try:
        telegraph_file = upload_file(path)
    except JSONDecodeError:
        await message.reply_text("Failed To Upload.")
        url = False
        return url

    try:
        url = "https://telegra.ph/" + telegraph_file[0]
    except:
        pass

    return url

def create_buttons(request_url, similar_url):
    keyboard = [
        [
            types.InlineKeyboardButton("Request URL", url=request_url),
            types.InlineKeyboardButton("Similar URL", url=similar_url)
        ]
    ]
    return types.InlineKeyboardMarkup(keyboard)

@app.on_message(filters.command("pp") & filters.reply)
async def reverse_search(client, message):
    reply_message = message.reply_to_message

    if reply_message.photo:
        photo_path = await reply_message.download()
        telegraph_url = await telegraph(message, photo_path)
        url = API_URL.format(url=telegraph_url)
    elif reply_message.text:
        url = API_URL.format(url=reply_message.text)
    else:
        await message.reply_text("Unsupported message type. Reply to an image or provide a URL.")
        return

    try:
        response = requests.get(url)
        result = response.json()
        image_description = result["result"]["image"]
        request_url = result["result"]["requestUrl"]
        similar_url = result["similarUrl"]
        buttons = create_buttons(request_url, similar_url)
        await message.reply_text(f"Image: {image_description}", reply_markup=buttons)
    except Exception as e:
        await message.reply_text(f"Error fetching information: {str(e)}")
