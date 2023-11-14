from Waifu import DATABASE
from pyrogram import filters
from pymongo import MongoClient
import asyncio
from Waifu import waifu

db = DATABASE["MAIN"]

def insert_waifu_data(waifu_name, rarity, image_url, source):
    waifu_data = {
        "waifu_name": waifu_name,
        "rarity": rarity,
        "image_url": image_url,
        "source": source
    }
    db.insert_one(waifu_data)

# Command to add waifu data in one go
@waifu.on_message(filters.command(["addwaifu"]))
async def add_new_waifu_command(_, message):
    user_id = message.from_user.id

    await message.reply("Please enter waifu data in the format: Name: Image: Rarity: Source")

# Filter to handle the user's response
@waifu.on_message(filters.user & filters.reply(message))
async def handle_waifu_data(_, message):
    user_id = message.from_user.id
    text = message.text.strip()
    
    if not text.startswith("Name: Image: Rarity: Source: "):
        await message.reply("Invalid format. Please use the format: Name: Image: Rarity: Source")
        return

    # Parse waifu data
    data = text.split(": ")
    if len(data) == 4:
        waifu_name, image_url, rarity, source = map(str.strip, data)

        # Insert waifu data into the database
        insert_waifu_data(waifu_name, rarity, image_url, source)
        await message.reply("Waifu data added successfully!")
    else:
        await message.reply("Invalid format. Please use the format: Name: Image: Rarity: Source")

# Command to fetch waifu data
@waifu.on_message(filters.command(["fetchwaifu"]))
async def fetch_waifu_data(_, message):
    waifus = db.find()  # Retrieve all waifu data from the database

    for waifu in waifus:
        if "waifu_name" in waifu and "rarity" in waifu and "image_url" in waifu and "source" in waifu:
            waifu_name = waifu["waifu_name"]
            rarity = waifu["rarity"]
            image_url = waifu["image_url"]
            source = waifu["source"]

            caption = f"Name: {waifu_name}\nRarity: {rarity}\nSource: {source}"
            await message.reply_photo(photo=image_url, caption=caption)
        else:
            await message.reply("Waifu data is missing some fields and cannot be displayed.")
