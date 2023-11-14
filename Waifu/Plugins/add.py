from Waifu import DATABASE
from pyrogram import filters
from pymongo import MongoClient
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

@waifu.on_message(filters.command("addwaifu"))
async def handle_waifu_data(client, message):
    user_id = message.from_user.id
    text = message.text.strip()

    if not text.startswith("Name: ") or not text.count(": ") == 3:
        await message.reply("Invalid format. Please use the format: Name: Image: Rarity: Source")
        return

    data = text.split(": ")
    if len(data) == 4:
        waifu_name, image_url, rarity, source = map(str.strip, data)
        insert_waifu_data(waifu_name, rarity, image_url, source)
        await message.reply("Waifu data added successfully!")
    else:
        await message.reply("Invalid format. Please use the format: Name: Image: Rarity: Source")

@waifu.on_message(filters.command("fetchwaifu"))
async def fetch_waifu_data(_, message):
    waifus = db.find()

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
