import httpx
from pyrogram import filters, Client
from pyrogram.types import Message
from Waifu import waifu as app

api_url = "https://pervert-api.onrender.com/chatgpt5"

@app.on_message(filters.command("chatgpt"))
async def chatgpt5(_: Client, message: Message):
    # Check if there is a query provided
    if len(message.command) < 2:
        return await message.reply_text("**Please provide a query.**")

    query = " ".join(message.command[1:])
    txt = await message.reply_text("**Wait patiently, requesting to API...**")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{api_url}?query={query}")
            response.raise_for_status()
            data = response.json()
            api_response = data.get("ChatGpt5", "No response from the API.")
            await txt.edit(api_response)
        except httpx.HTTPError as e:
            await txt.edit(f"HTTP error: {e}")
        except Exception as e:
            await txt.edit(f"An error occurred: {str(e)}")
