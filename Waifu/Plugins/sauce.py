from pyrogram import Client, filters
import time
import requests
from Waifu import app

api_url = "https://pervert-api.onrender.com/nudes"


async def send_photo_periodically(message):
    try:
        while True:
            # Fetch photo URL from the API
            response = requests.get(api_url)
            data = response.json()
            photo_url = data["url"]

            # Send the photo
            await message.reply_photo(photo=photo_url, caption="Enjoy!")

            # Wait for 45 seconds before sending the next photo
            time.sleep(45)

    except Exception as e:
        print(f"Error: {e}")
        # Handle exceptions as needed

@app.on_message(filters.command("send_photos"))
async def send_photos_command(_, message):
    # Trigger the function when the command is received
    await send_photo_periodically(message)
