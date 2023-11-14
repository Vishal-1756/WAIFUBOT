from Waifu import DATABASE
from pyrogram import filters
from Waifu import waifu
from pymongo import MongoClient

db = DATABASE["MAIN"]
collection = db["waifus"]  # Replace "waifus" with your actual collection name

@waifu.on_message(filters.command("addwaifu"))
async def start_add_waifu(_, message):
    await message.reply("Please provide the waifu details in the following format:\n\nName: [waifu name]\nImage: [image URL]\nRarity: [rarity]\nSource: [source text]")

@waifu.on_message(filters.regex(r"Name: (.+)\nImage: (.+)\nRarity: (.+)\nSource: (.+)"))
async def add_waifu_detail(_, message):
    match = message.matches[0]
    waifu_data = {
        "waifu_name": match.group(1),
        "rarity": match.group(3),
        "image_url": match.group(2),
        "source": match.group(4)
    }
    collection.insert_one(waifu_data)  # Use insert_one on the collection
    await message.reply("Waifu data added successfully!")

@waifu.on_message(filters.command("fetchwaifu"))
async def fetch_waifu_data(_, message):
    waifus = collection.find()

    for waifu in waifus:
        if "waifu_name" in waifu and "rarity" in waifu and "image_url" in waifu and "source" in waifu:
            waifu_name = waifu["waifu_name"]
            rarity = waifu["rarity"]
            image_url = waifu["image_url"]
            source = waifu["source"]

            caption = f"Name: {waifu_name}\nImage: {image_url}\nRarity: {rarity}\nSource: {source}"
            await message.reply_photo(photo=image_url, caption=caption)
        else:
            await message.reply("Waifu data is missing some fields and cannot be displayed.")
