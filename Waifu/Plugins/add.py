from Waifu import DATABASE
from pyrogram import filters
from Waifu import waifu
from pymongo import MongoClient

db = DATABASE["MAIN"]
collection = db["waifus"]

@waifu.on_message(filters.command("addwaifu"))
async def start_add_waifu(_, message):
    await message.reply("Please reply to this message with the waifu details in the following format:\n\nName: [waifu name]\nImage: [image URL]\nRarity: [rarity]\nSource: [source text]\nID: [special ID]")

@waifu.on_message(filters.reply & filters.regex(r"Name: (.+)\nImage: (.+)\nRarity: (.+)\nSource: (.+)(?:\nID: (.+))?$"))
async def add_waifu_detail(_, message):
    match = message.matches[0]
    special_id = match.group(5) if match.group(5) else None

    # Check if the special ID is already used for another waifu
    if special_id and collection.find_one({"special_id": special_id}):
        await message.reply(f"Special ID '{special_id}' is already in use for another waifu. Please provide a different ID.")
        return

    waifu_data = {
        "special_id": special_id,
        "waifu_name": match.group(1),
        "rarity": match.group(3),
        "image_url": match.group(2),
        "source": match.group(4)
    }
    collection.insert_one(waifu_data)
    await message.reply("Waifu data added successfully!")

@waifu.on_message(filters.command("fetchwaifu"))
async def fetch_waifu_data(_, message):
    waifus = collection.find()

    for waifu in waifus:
        if "waifu_name" in waifu and "rarity" in waifu and "image_url" in waifu and "source" in waifu:
            special_id = waifu.get("special_id", "N/A")
            waifu_name = waifu["waifu_name"]
            rarity = waifu["rarity"]
            image_url = waifu["image_url"]
            source = waifu["source"]

            caption = f"ID: {special_id}\nName: {waifu_name}\nImage: {image_url}\nRarity: {rarity}\nSource: {source}"
            await message.reply_photo(photo=image_url, caption=caption)
        else:
            await message.reply("Waifu data is missing some fields and cannot be displayed.")
