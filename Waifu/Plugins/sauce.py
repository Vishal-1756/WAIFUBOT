from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto
import requests
import time
from Waifu import waifu as app

api_url = "https://api.betabotz.org/api/webzone/whatanime"
telegraph_url = "https://api.telegra.ph/upload"




@app.on_message(filters.command("sauce", prefixes="/") | filters.text)
def sauce_command(client, message):
    if message.reply_to_message and (message.reply_to_message.photo or message.reply_to_message.video):
        # If command is used as a reply to a photo or video
        media = message.reply_to_message.photo[-1] if message.reply_to_message.photo else message.reply_to_message.video
    elif message.text:
        # If command is used with a direct link
        media = message.text.strip()

    if media:
        try:
            # Upload the photo or video to Telegraph
            files = {"file": ("media", open(client.download_media(media), "rb"))}
            telegraph_response = requests.post(telegraph_url, files=files)
            telegraph_data = telegraph_response.json()

            # Make a request to the whatanime API
            api_params = {
                "query": telegraph_data["src"],
                "apikey": "QlyCxRQV"  # Replace with your API key
            }

            # Send "Please wait..." message
            wait_message = message.reply_text("Please wait... Uploading your query to the API.")

            api_response = requests.get(api_url, params=api_params)
            api_data = api_response.json()

            # Delete the "Please wait..." message
            wait_message.delete()

            if api_data["status"] and api_data["code"] == 200:
                result = api_data["result"]["data"]
                caption = f"Anilist: {result['anilist']}\nFile Name: {result['filename']}\nSimilarity: {result['similarity']}\nVideo Link: {result['video']}\nImage Link: {result['image']}"
                message.reply_photo(result['image'], caption=caption)
            else:
                message.reply_text("Error: Unable to fetch data from the whatanime API")

        except Exception as e:
            message.reply_text(f"Error: {str(e)}")
    else:
        message.reply_text("Please reply to a photo or video or provide a direct link when using the /sauce command.")
