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

# Define a function to send a spawned waifu
async def send_spawned_waifu(chat_id):
    global spawned_waifu
    if spawned_waifu:
        image_url = spawned_waifu.get("image")
        rank = spawned_waifu.get("rank")

        if image_url and rank:
            caption = f"UwU {rank} just appeared in the group! Catch it by using /catch {spawned_waifu['name']}"
            await waifu.send_photo(chat_id=chat_id, photo=image_url, caption=caption)
        else:
            await waifu.send_message(chat_id=chat_id, text="Incomplete waifu data. Unable to send.")
    else:
        await waifu.send_message(chat_id=chat_id, text="No random waifu found.")

# Your message handler for text messages in groups
@waifu.on_message(filters.text & filters.group)
async def on_text_message(_, message: Message):
    global message_count, spawned_waifu
    
    message_count += 1
    
    if message_count == 5:
        message_count = 0
        
        # Send a random waifu from your data when 5 messages are reached
        spawned_waifu = random.choice(waifus.get("waifus", []))
        await send_spawned_waifu(message.chat.id)

@waifu.on_message(filters.command("catch", prefix) & filters.group)
async def catch_waifu(_, message):
    global spawned_waifu
    
    if spawned_waifu:
        spawned_waifu_name = spawned_waifu.get("name")
        query = message.text.split(maxsplit=1)[1]
        
        # Check if the provided name matches the spawned waifu's name
        if query.lower() == spawned_waifu_name.lower():
            image_url = spawned_waifu.get("image")
            rank = spawned_waifu.get("rank")
            id = spawned_waifu.get("id")
            
            if image_url and rank and id:
                user_id = message.from_user.id
                await add_waifu_to_db(user_id, spawned_waifu_name)
                caption = f"Gotcha! You caught a {rank} {spawned_waifu_name} with image ID {id}"
                await waifu.send_photo(chat_id=message.chat.id, photo=image_url, caption=caption)
                spawned_waifu = None  # Reset the spawned waifu after catching
            else:
                await waifu.send_message(chat_id=message.chat.id, text="Incomplete waifu data. Unable to send.")
        else:
            await waifu.send_message(chat_id=message.chat.id, text=f"You missed! The spawned waifu's name is {spawned_waifu_name}. Try again.")
    else:
        await waifu.send_message(chat_id=message.chat.id, text="No waifu to catch. Wait for a spawned waifu.")

# Your message handler for the /harem command
@waifu.on_message(filters.command("harem", prefix) & filters.group)
async def harem_command(_, message):
    user_id = message.from_user.id
    user_waifus = await get_user_waifus(user_id)
    
    if user_waifus:
        waifu_list = "\n".join(user_waifus)
        reply_text = f"Your harem:\n{waifu_list}"
    else:
        reply_text = "Your harem is empty!"
    
    await waifu.send_message(chat_id=message.chat.id, text=reply_text)
