import random
import json
from pyrogram import Client, filters
from pyrogram.types import Message
from Waifu.Database.main import get_user_waifus, add_waifu_to_db
from Waifu import waifu, prefix

# Variable to store the currently spawned waifu
spawned_waifu = None

# Load waifu data from the "waifu.json" file
with open("waifu.json", "r") as file:
    waifus = json.load(file)

# Counter to track the number of messages in the group
message_count = 0

@waifu.on_message(filters.text & filters.group)
async def on_text_message(_, message: Message):
    global spawned_waifu, message_count
    
    message_count += 1
    
    if message_count == 5:
        # Reset the message count
        message_count = 0
        
        # Send a random waifu from your data when 5 messages are reached
        spawned_waifu = random.choice(waifus.get("waifus", []))
        
        if spawned_waifu:
            image_url = spawned_waifu.get("image")
            rank = spawned_waifu.get("rank")
            
            if image_url and rank:
                # Update the caption to include the rank and the new text
                caption = f"UwU {rank} Just appeared in the group! Catch it by /catch {spawned_waifu['name']}"
                await waifu.send_photo(chat_id=message.chat.id, photo=image_url, caption=caption)

            else:
                await message.send_message(chat_id=message.chat.id, text="Incomplete waifu data. Unable to send.")
        else:
            await message.send_message(chat_id=message.chat.id, text="No random waifu found.")

@waifu.on_message(filters.command("catch", prefix))
async def catch_waifu(_, message):
    global spawned_waifu
    
    if spawned_waifu:
        # Get the name provided in the /catch command
        query = message.text.split(maxsplit=1)[1]
        
        # Check if the provided name matches the spawned waifu's name
        if query.lower() == spawned_waifu["name"].lower():
            image_url = spawned_waifu.get("image")
            rank = spawned_waifu.get("rank")
            id = spawned_waifu.get("id")  # Assuming you have an 'id' field in your waifu data
            
            if image_url and rank and id:
                user_id = message.from_user.id
                await add_waifu_to_db(user_id, spawned_waifu['name'])
                # Update the caption to include the rank, name, and image ID
                caption = f"Gotcha! You caught a {rank} {spawned_waifu['name']} with image ID {id}"
                await message.send_photo(chat_id=message.chat.id, photo=image_url, caption=caption)
                spawned_waifu = None  # Reset the spawned waifu after catching
            else:
                await message.send_message(chat_id=message.chat.id, text="Incomplete waifu data. Unable to send.")
        else:
            await message.send_message(chat_id=message.chat.id, text="Invalid waifu name. Try again.")
    else:
        await message.send_message(chat_id=message.chat.id, text="No waifu to catch. Wait for a spawned waifu.")

@waifu.on_message(filters.command("harem", prefix))
async def harem_command(_, message):
    user_id = message.from_user.id
    user_waifus = await get_user_waifus(user_id)
    
    if user_waifus:
        waifu_list = "\n".join(user_waifus)
        reply_text = f"Your harem:\n{waifu_list}"
    else:
        reply_text = "Your harem is empty!"
    
    # Use the message object to reply
    await message.reply_text(reply_text)

# Additional code for /h and other commands not shown, but you can keep it as you had before.
