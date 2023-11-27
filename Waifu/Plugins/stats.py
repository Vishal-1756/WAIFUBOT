from Waifu import waifu as api
from pyrogram import Client, filters
import requests

@api.on_message(filters.command("hentai", prefixes="/"))
async def hentai_command(client, message):
    api_url = "https://hentaibar.onrender.com/random"

    try:
        await message.reply("Please wait patiently. Fetching your request...")

        response = requests.get(api_url)
        response.raise_for_status()  # Check for errors

        hentai_data = response.json()

        thumb_url = hentai_data.get('thum')
        file_url = hentai_data.get('file')
        name = hentai_data.get('name')
        upload_date = hentai_data.get('upload_date')
        duration = hentai_data.get('duration')

        if thumb_url and file_url and name and upload_date and duration:
            # Send thumbnail as a photo and other data in the caption
            await message.reply_photo(thumb_url, caption=f"Name: {name}\nUpload Date: {upload_date}\nDuration: {duration}\n\n{file_url}")
        else:
            await message.reply_text("Error: Incomplete data received from the API.")

    except requests.exceptions.RequestException as err:
        await message.reply_text(f"Error fetching data: {err}")


