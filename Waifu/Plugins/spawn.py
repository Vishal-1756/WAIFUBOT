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
        random_waifu = random.choice(waifus["waifus"])
        
        # Check if random_waifu is not None before replying
        if random_waifu:
            message.reply_photo(photo=random_waifu.get("image", ""), caption=f"{random_waifu.get('name', '')} - {random_waifu.get('rank', '')}")
        else:
            message.reply_text("No random waifu found!")

@waifu.on_message(filters.command("catch", prefixes="/"))
def catch_waifu(_, message: Message):
    # Get the name provided in the /catch command
    query = message.text.split("/catch ", 1)[-1].strip()
    
    # Search for the waifu by name in your data
    found_waifu = None
    for waifu_data in waifus["waifus"]:
        if query.lower() in waifu_data.get("name", "").lower():
            found_waifu = waifu_data
            break
    
    if found_waifu:
        message.reply_photo(photo=found_waifu.get("image", ""), caption=f"{found_waifu.get('name', '')} - {found_waifu.get('rank', '')}")
    else:
        message.reply_text("Waifu not found!")
