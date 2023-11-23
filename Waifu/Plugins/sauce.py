from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InputMediaVideo
from pyrogram.file_id import FileId
from io import BytesIO
import base64
import mimetypes
import requests
import aiohttp
from Waifu import waifu as app

async def telegraph(attachment_data):
    form = FormData()
    form.add_file("file", BytesIO(base64.b64decode(attachment_data['data'])),
                  filename=f"telegraph.{mimetypes.guess_extension(attachment_data['mimetype'])}")

    async with aiohttp.ClientSession() as session:
        async with session.post("https://te.legra.ph/upload", data=form) as resp:
            response_data = await resp.json()
            return "https://te.legra.ph" + response_data[0]['src']

async def shorten_video_url(video_url):
    try:
        response = await requests.get('https://api.erdwpe.com/api/linkshort/tinyurl', params={'link': video_url})
        data = response.json()
        if data['status']:
            return data['result']
        else:
            print('TinyURL API request failed:', data)
            return None
    except Exception as e:
        print('Error shortening URL:', e)
        return None

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

@app.on_message(filters.command("sauce"))
async def sauce_command(_, message):
    try:
        await message.delete(True)
        if message.reply_to_message:
            quoted_msg = message.reply_to_message
            attachment_data = await app.download_media(quoted_msg)
            tdata = await telegraph(attachment_data)

            if tdata == "error":
                await quoted_msg.reply("Error occurred while creating a direct link.")
            else:
                response = await requests.get(f'https://api.betabotz.org/api/webzone/whatanime?query={tdata}&apikey=GK5zaGhL')
                jdata = response.json()
                name = jdata['result']['data']['filename'].replace('.mp4', '')
                episode = jdata['result']['data']['episode']
                image = jdata['result']['data']['image']
                video = jdata['result']['data']['video']

                tinyurl = await shorten_video_url(video)
                caption = f"Name: **{name}**\nEpisode: **{episode}**\nVideo: **{tinyurl}**"


                try:
                    media = InputMediaVideo(FileId(video))
                    await app.send_message(message.chat.id, media, caption=caption, parse_mode=ParseMode.MARKDOWN)
                except Exception as e:
                    await message.reply("Error while sending video")
        else:
            await message.reply("*Error*\n```Please reply to a media file```")
    except Exception as e:
        await message.reply("*Error*\n```Can't support text!```")
