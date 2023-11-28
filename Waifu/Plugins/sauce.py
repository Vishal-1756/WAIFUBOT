from pyrogram import Client, filters
import requests
from telegraph import upload_file
from Waifu import waifu as app
from Waifu import bot_token

api_url = "https://api.betabotz.org/api/webzone/whatanime"
tinyurl_api_url = "https://api.erdwpe.com/api/linkshort/tinyurl"


async def shorten_video_url(video_url):
    try:
        response = requests.get(tinyurl_api_url, params={"link": video_url})
        response_data = response.json()

        if response_data["status"] == True:
            return response_data["result"]
        else:
            print("TinyURL API request failed:", response_data)
            return None
    except Exception as error:
        print("Error shortening URL:", error)
        return None


async def get_file_id_from_message(message):
    file_id = None
    if message.reply_to_message and message.reply_to_message.media:
        r = requests.post(f'https://api.telegram.org/bot{bot_token}/getFile?file_id={message.reply_to_message.media.file_id}').json()
        file_id = r['result']['file_path']

    return file_id


async def sauce_command(client, message):
    try:
        # Check if the message has a quoted message
        file_id = await get_file_id_from_message(message)
        if file_id:
            media_path = await client.download_media(file_id)
            telegraph_url = upload_file(media_path)

            if telegraph_url:
                api_params = {"query": telegraph_url, "apikey": "GK5zaGhL"}  # Replace with your API key
                wait_message = await message.reply_text("Please wait... Uploading your query to the API.")

                # Make a request to the whatanime API
                response = requests.get(api_url, params=api_params)
                api_data = response.json()

                # Delete the "Please wait..." message
                wait_message.delete()

                if api_data.get("status") and api_data.get("code") == 200:
                    result_data = api_data["result"]["data"]
                    name = result_data["filename"].replace('.mp4', '')
                    episode = result_data["episode"]
                    image = result_data["image"]
                    video = result_data["video"]

                    # Shorten the video URL
                    tinyurl = await shorten_video_url(video)

                    caption = f"Name: *{name}*\nEpisode: *{episode}*\nVideo: *{tinyurl}*"

                    try:
                        # Send the media with the caption
                        await message.reply_video(video, caption=caption, parse_mode="MarkdownV2")
                    except Exception as send_error:
                        await message.reply_text(f"Error while sending video: {send_error}")
                else:
                    await message.reply_text("Error: Unable to fetch data from the whatanime API")
            else:
                await message.reply_text("Error occurred while creating a direct link.")
        else:
            await message.reply_text("Error: Unable to get file ID from the media.")
    except Exception as command_error:
        await message.reply_text(f"Error: {str(command_error)}")

app.on_message(filters.command("sauce", prefixes="/") | filters.text)(sauce_command)
