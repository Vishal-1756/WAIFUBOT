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

    # Split the message into lines
    lines = message.text.strip().split('\n')

    if len(lines) != 4:
        await message.reply("Invalid format. Please provide Name, Image, Rarity, and Source each on a new line.")
        return

    # Parse the lines
    waifu_name = lines[0].strip().replace("Name:", "")
    image_url = lines[1].strip().replace("Image:", "")
    rarity = lines[2].strip().replace("Rarity:", "")
    source = lines[3].strip().replace("Source:", "")

    insert_waifu_data(waifu_name, rarity, image_url, source)
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
