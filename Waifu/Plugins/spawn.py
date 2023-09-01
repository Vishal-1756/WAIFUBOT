import random
import json
from pyrogram import filters
from pyrogram.types import Message
from Waifu import waifu

# Load waifu data from the "waifu.json" file
with open("waifu.json", "r") as file:
    waifus = json.load(file)

# Counter to track the number of messages in the group
message_count = 0

@waifu.on_message(filters.text & filters.group)
def on_text_message(_, message: Message):
    global message_count
    message_count += 1
    
    if message_count == 5:
        # Reset the message count
        message_count = 0
        
        # Send a random waifu from your data when 5 messages are reached
        random_waifu = random.choice(waifus.get("waifus", []))
        
        if random_waifu:
            image_url = random_waifu.get("image")
            name = random_waifu.get("name")
            rank = random_waifu.get("rank")
            
            if image_url and name and rank:
                message.reply_photo(photo=image_url, caption=f"{name} - {rank}")
            else:
                message.reply_text("Incomplete waifu data. Unable to send.")
        else:
            message.reply_text("No random waifu found.")

@waifu.on_message(filters.command("catch", prefixes="/"))
def catch_waifu(_, message: Message):
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
        name = found_waifu.get("name")
        rank = found_waifu.get("rank")
        
        if image_url and name and rank:
            message.reply_photo(photo=image_url, caption=f"{name} - {rank}")
        else:
            message.reply_text("Incomplete waifu data. Unable to send.")
    else:
        message.reply_text("Waifu not found!")

# Add additional logging to track the flow of your code for debugging
print("Bot started successfully. Listening for messages...")
