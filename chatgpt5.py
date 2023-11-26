from pyrogram import filters
from pyrogram.types import Message
import requests
from Waifu import waifu as waifu

api_url = "https://pervert-api.onrender.com/chatgpt5"

@app.on_message(filters.command("chat5"))
async def chatgpt5(_, message: Message):
   
    if len(message.command) < 2:
        await message.reply_text("`Please provide a query.`")
        return

    
    query = " ".join(message.command[1:])
    
    await message.reply_text("`Wait patiently, requesting to API...`")

    try:
        response = requests.get(f"{api_url}?query={query}")
        data = response.json()
        api_response = data.get("data", "No response from the API.")
        await message.edit_text(api_response)
    except Exception as e:
        await message.edit_text(f"Failed to fetch data: {str(e)}")
