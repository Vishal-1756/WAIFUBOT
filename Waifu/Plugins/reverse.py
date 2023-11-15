from Waifu import waifu as app
from Waifu import bot_token
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from unidecode import unidecode

async def Sauce(bot_token, file_id):
    r = requests.post(f'https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}').json()
    file_path = r['result']['file_path']
    headers = {
        'User-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'
    }
    to_parse = f"https://images.google.com/searchbyimage?safe=off&sbisrc=tg&image_url=https://api.telegram.org/file/bot{bot_token}/{file_path}"
    r = requests.get(to_parse, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    result = {
        "similar": '',
        'output': ''
    }

    # Extract the similar image link
    similar_link_tag = soup.find('a', {'class': 'irc_mimg irc_but_r'})
    if similar_link_tag:
        result['similar'] = similar_link_tag['href']

    # Extract the best guess text
    best_guess_tag = soup.find('div', {'class': 'BNeawe iBp4i AP7Wnd'})
    if best_guess_tag:
        result["output"] = unidecode(best_guess_tag.get_text())

    return result


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
    text = await msg.reply("** wait a sec...**")
    file_id = await get_file_id_from_message(msg)
    if not file_id:
        return await text.edit("**reply to media!**")
    await text.edit("** Searching in Google....**")
    result = await Sauce(bot_token, file_id)
    if not result["output"]:
        return await text.edit("Couldn't find anything")
    
    reply_text = f'[{result["output"]}]({result["similar"]})' if result["similar"] else f'[{result["output"]}]'
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Visit Site", url=result["similar"])]]) if result["similar"] else None
    await text.edit(reply_text, reply_markup=reply_markup)


@app.on_message(filters.command(["pp", "grs", "reverse", "r"]) & filters.private)
async def ppsearch(_, msg):
    text = await msg.reply("** wait a sec...**")
    file_id = await get_file_id_from_message(msg)
    if not file_id:
        return await text.edit("**reply to media!**")
    await text.edit("** Searching in Google....**")
    result = await Sauce(bot_token, file_id)
    if not result["output"]:
        return await text.edit("Couldn't find anything")

    reply_text = f'[{result["output"]}]({result["similar"]})' if result["similar"] else f'[{result["output"]}]'
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Visit Site", url=result["similar"])]]) if result["similar"] else None
    await text.edit(reply_text, reply_markup=reply_markup)
