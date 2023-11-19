from pyrogram import filters
from Waifu import waifu
from pymongo import MongoClient

# Assuming DATABASE is properly configured
db = DATABASE["MAIN"]
collection = db["waifus"]

@waifu.on_message(filters.command("addwaifu"))
async def add_waifu_detail(_, message):
    try:
        # Ensure that the message is a reply
        if message.reply_to_message and message.reply_to_message.text:
            # Parse the waifu details from the user's reply
            waifu_name = message.reply_to_message.text.split("\n")[1].split(":")[1].strip()
            image_url = message.reply_to_message.text.split("\n")[2].split(":")[1].strip()
            rarity = message.reply_to_message.text.split("\n")[3].split(":")[1].strip()
            source = message.reply_to_message.text.split("\n")[4].split(":")[1].strip()
            special_id = message.reply_to_message.text.split("\n")[5].split(":")[1].strip() if len(message.reply_to_message.text.split("\n")) > 5 else None

            # Check if the special ID is already used for another waifu
            if special_id and collection.find_one({"special_id": special_id}):
                await message.reply(f"Special ID '{special_id}' is already in use for another waifu. Please provide a different ID.")
                return

            waifu_data = {
                "special_id": special_id,
                "waifu_name": waifu_name,
                "rarity": rarity,
                "image_url": image_url,
                "source": source
            }

            collection.insert_one(waifu_data)
            await message.reply("Waifu data added successfully!")

        else:
            await message.reply("Please reply to this message with the waifu details in the specified format.")

    except Exception as e:
        print(f"Error adding waifu: {str(e)}")
        await message.reply("An error occurred while adding waifu data. Please check the format and try again.")

@waifu.on_message(filters.command("fetchwaifu"))
async def fetch_waifu_data(_, message):
    try:
        waifus = collection.find()

        for waifu in waifus:
            if all(key in waifu for key in ["waifu_name", "rarity", "image_url", "source"]):
                special_id = waifu.get("special_id", "N/A")
                waifu_name = waifu["waifu_name"]
                rarity = waifu["rarity"]
                image_url = waifu["image_url"]
                source = waifu["source"]

                caption = f"ID: {special_id}\nName: {waifu_name}\nImage: {image_url}\nRarity: {rarity}\nSource: {source}"
                await message.reply_photo(photo=image_url, caption=caption)
            else:
                await message.reply("Waifu data is missing some fields and cannot be displayed.")

    except Exception as e:
        print(f"Error fetching waifus: {str(e)}")
        await message.reply("An error occurred while fetching waifu data.")
