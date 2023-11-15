import requests
from urllib.parse import quote_plus, unquote
from bs4 import BeautifulSoup
from unidecode import unidecode
from Waifu import waifu as app
from Waifu import bot_token
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ParseMode

BASE_URL = "https://api.telegram.org/bot{}"

async def Sauce(bot_token, file_id):
    file_url = f"{BASE_URL}/getFile?file_id={file_id}"
    r = requests.post(file_url).json()
    file_path = r['result']['file_path']
    headers = {'User-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'}
    to_parse = f"https://images.google.com/searchbyimage?safe=off&sbisrc=tg&image_url={BASE_URL}/file/{bot_token}/{file_path}"
    r = requests.get(to_parse, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    result = {
        "similar_google": [],
        'output_google': '',
    }

    # Google Search
    similar_images_div = soup.find('div', {'class': 'RAyV4b'})
    if similar_images_div:
        for similar_images_link in similar_images_div.find_all('a'):
            url = f"https://www.google.com{similar_images_link['href']}"
            result['similar_google'].append(url)

    best_guess_div = soup.find('div', {'class': 'r5a77d'})
    if best_guess_div:
        output = best_guess_div.get_text()
        decoded_text = unidecode(output)
        result["output_google"] = f"[{decoded_text} - Google Image Search]({to_parse})"
        
    return result, to_parse

async def get_file_id_from_message(msg):
    file_id = None
    message = msg.reply_to_message
    if not message:
        return
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

@app.on_message(filters.command(["pp", "grs", "reverse", "r"]) & filters.group)
async def _reverse(_, msg):
    text = await msg.reply("`⏫ Uploading To Google Search Engine`")
    file_id = await get_file_id_from_message(msg)
    if not file_id:
        return await text.edit("`Dear Pro People's Please Reply To A Media File 🗃️`")
    
    await text.edit("`🌐 Wait For >1 Min Searching Your Prompt`")
    result, to_parse = await Sauce(bot_token, file_id)

    if not result["output_google"]:
        return await text.edit("`😅 Ntg Found On Google Buddy`")

    reply_text = (
        f'Google: {result["output_google"]}\n'
        f'Made by @ikaris0_0 distributed by @team_devx'
    )

    keyboard = [
        [
            InlineKeyboardButton("📌 More Results Here", url=to_parse),
            InlineKeyboardButton("👾 Support 📈", url="https://t.me/team_devsX"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await text.edit_text(reply_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
