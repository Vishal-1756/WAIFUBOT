from Waifu import DATABASE
from pyrogram import filters
from pymongo import MongoClient
from Waifu import waifu

db = DATABASE["MAIN"]

def insert_waifu_data(name, rarity, image_url, source):
    waifu_data = {
        "waifu_name": name,
        "rarity": rarity,
        "image_url": image_url,
        "source": source
    }
    db.insert_one(waifu_data)

@waifu.on_message(filters.command("addwaifu"))
async def handle_waifu_data(client, message):
    user_id = message.from_user.id

    if len(message.command) != 1:
        await message.reply("Invalid format. Please provide only one command, and include the details as separate text in the following format:\n\nName: [waifu name]\nImage: [image URL]\nRarity: [rarity]\nSource: [source text]")
        return

    text = message.text
    name = text.split("Name:")[1].split("Image:")[0].strip()
    image = text.split("Image:")[1].split("Rarity:")[0].strip()
    rarity = text.split("Rarity:")[1].split("Source:")[0].strip()
    source = text.split("Source:")[1].strip()

    insert_waifu_data(name, rarity, image, source)
    await message.reply("Waifu data added successfully!")

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
