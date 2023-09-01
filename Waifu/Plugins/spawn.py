import random
import json
from pyrogram import Client, filters
from pyrogram.types import Message
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
                await message.reply_photo(photo=image_url, caption=caption)
            else:
                await message.reply_text("Incomplete waifu data. Unable to send.")
        else:
            await message.reply_text("No random waifu found.")


@waifu.on_message(filters.command("catch", prefixes="/"))
async def catch_waifu(_, message: Message):
    # Get the name provided in the /catch command
    query = message.text.split("/catch ", 1)[-1].strip()
    
    # Search for the waifu by name in your data
    found_waifu = None
    for waifu_data in waifus.get("waifus", []):
        if "name" in waifu_data and query.lower() in waifu_data["name"].lower():
            found_waifu = waifu_data
            break
    
    if found_waifu:
        image_url = found_waifu.get("image")
        rank = found_waifu.get("rank")
        id = found_waifu.get("id")  # Assuming you have an 'id' field in your waifu data
        
        if image_url and rank and id:
            # Update the caption to include the rank, name, and image ID
            caption = f"Gotcha! You caught a {rank} {found_waifu['name']} with image ID {id}"
            await message.reply_photo(photo=image_url, caption=caption)
        else:
            await message.reply_text("Incomplete waifu data. Unable to send.")
    else:
        await message.reply_text("Waifu not found!")

