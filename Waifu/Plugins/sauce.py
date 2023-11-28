from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto
import requests
import time
from Waifu import waifu as app

api_url = "https://api.betabotz.org/api/webzone/whatanime"
telegraph_url = "https://api.telegra.ph/upload"


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


@app.on_message(filters.command("sauce", prefixes="/") | filters.text)
async def sauce_command(client, message):
    file_id = await get_file_id_from_message(message)

    if file_id:
        try:
            # Download the media using file_id
            media_path = await client.download_media(file_id)

            # Upload the media to Telegraph
            files = {"file": ("media", open(media_path, "rb"))}
            telegraph_response = requests.post(telegraph_url, files=files)
            telegraph_data = telegraph_response.json()

            # Make a request to the whatanime API
            api_params = {
                "query": telegraph_data["src"],
                "apikey": "QlyCxRQV"  # Replace with your API key
            }

            # Send "Please wait..." message
            wait_message = await message.reply_text("Please wait... Uploading your query to the API.")

            api_response = requests.get(api_url, params=api_params)
            api_data = api_response.json()

            # Delete the "Please wait..." message
            wait_message.delete()

            if api_data["status"] and api_data["code"] == 200:
                result = api_data["result"]["data"]
                caption = f"Anilist: {result['anilist']}\nFile Name: {result['filename']}\nSimilarity: {result['similarity']}\nVideo Link: {result['video']}\nImage Link: {result['image']}"
                await message.reply_photo(result['image'], caption=caption)
            else:
                await message.reply_text("Error: Unable to fetch data from the whatanime API")

        except Exception as e:
            await message.reply_text(f"Error: {str(e)}")
    else:
        await message.reply_text("Please reply to a photo or video or provide a direct link when using the /sauce command.")

app.run()
