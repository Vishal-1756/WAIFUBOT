from Waifu import DATABASE
from pyrogram import filters
from pymongo import MongoClient
import asyncio
from Waifu import waifu

db = DATABASE["MAIN"]

waifu_data = {}  # Store waifu data temporarily

def insert_waifu_data(waifu_name, rarity, image_url, source):
    waifu_data = {
        "waifu_name": waifu_name,
        "rarity": rarity,
        "image_url": image_url,
        "source": source
    }
    db.insert_one(waifu_data)

# Command to add waifu data step by step
@waifu.on_message(filters.command(["addwaifu"]))
async def add_new_waifu_command_1(_, message):
    await message.reply("Please enter the waifu's Name:")
    waifu_data["user_id"] = message.from_user.id
    waifu_data["message_id"] = message.message_id
    waifu_data["step"] = 1

# Filter to handle the next user message
@waifu.on_message(filters.user(waifu_data["user_id"]) & filters.reply(waifu_data["message_id"]) & filters.text)
async def add_new_waifu_command_2(_, message):
    user_id = waifu_data["user_id"]
    step = waifu_data["step"]

    if step == 1:
        waifu_data["waifu_name"] = message.text
        await message.reply("Please enter the Rarity:")
        waifu_data["step"] = 2
    elif step == 2:
        waifu_data["rarity"] = message.text
        await message.reply("Please enter the Image URL:")
        waifu_data["step"] = 3
    elif step == 3:
        waifu_data["image_url"] = message.text
        await message.reply("Please enter the Source:")
        waifu_data["step"] = 4
    elif step == 4:
        waifu_data["source"] = message.text
        insert_waifu_data(waifu_data["waifu_name"], waifu_data["rarity"], waifu_data["image_url"], waifu_data["source"])
        await message.reply("Waifu data added successfully!")

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
