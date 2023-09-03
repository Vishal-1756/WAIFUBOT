import random
import json
from pyrogram import Client, filters
from pyrogram.types import Message
from Waifu.Database.main import get_user_waifus, add_waifu_to_db
from Waifu import waifu


# Load waifu data from the "waifu.json" file
with open("waifu.json", "r") as file:
    waifus = json.load(file)

message_count = 0

@waifu.on_message(filters.text & filters.group)
async def on_text_message(_, message: Message):
    global message_count
    message_count += 1
    
    if message_count == 5:
        # Reset the message count
        message_count = 0
        
        # Send a random waifu from your data when 5 messages are reached
        random_waifu = random.choice(waifus.get("waifus", []))
        
        if random_waifu:
            image_url = random_waifu.get("image")
            rank = random_waifu.get("rank")
            
            if image_url and rank:
                # Update the caption to include the rank and the new text
                caption = f"UwU {rank} Just appeared in group! Catch it by /catch (name)"
                await waifu.send_photo(chat_id=message.chat.id, photo=image_url, caption=caption)
            else:
                await waifu.send_message(chat_id=message.chat.id, text="Incomplete waifu data. Unable to send.")
        else:
            await waifu.send_message(chat_id=message.chat.id, text="No random waifu found.")


@waifu.on_message(filters.command("catch", prefixes="/") & filters.regex(r"/catch [a-zA-Z]+"))
async def catch_waifu(_, message):
    # Check if there are waifus available in the data
    if waifus.get("waifus"):
        # Get the name provided in the /catch command
        query = message.text.split("/catch ", 1)[-1].strip()

        # Search for the waifu by name in your data
        found_waifu = None
        for waifu_data in waifus["waifus"]:
            if "name" in waifu_data and query.lower() in waifu_data["name"].lower():
                found_waifu = waifu_data
                break

        if found_waifu:
            image_url = found_waifu.get("image")
            rank = found_waifu.get("rank")
            id = found_waifu.get("id")  # Assuming you have an 'id' field in your waifu data

            if image_url and rank and id:
                user_id = message.from_user.id
                await add_waifu_to_db(user_id, found_waifu['name'])
                # Update the caption to include the rank, name, and image ID
                caption = f"Gotcha! You caught a {rank} {found_waifu['name']} with image ID {id}"
                await waifu.send_photo(chat_id=message.chat.id, photo=image_url, caption=caption)
            else:
                await waifu.send_message(chat_id=message.chat.id, text="Incomplete waifu data. Unable to send.")
        else:
            await waifu.send_message(chat_id=message.chat.id, text="Waifu not found.")
    else:
        await waifu.send_message(chat_id=message.chat.id, text="No waifus available at the moment.")


@waifu.on_message(filters.command("harem", prefixes="/"))
async def harem_command(_, message):
    user_id = message.from_user.id
    user_waifus = await get_user_waifus(user_id)
    
    if user_waifus:
        waifu_list = "\n".join(user_waifus)
        reply_text = f"Your harem:\n{waifu_list}"
    else:
        reply_text = "Your harem is empty!"
    
    await waifu.send_message(chat_id=message.chat.id, text=reply_text)


