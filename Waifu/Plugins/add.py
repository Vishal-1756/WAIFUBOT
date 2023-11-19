from pyrogram import filters
from Waifu import waifu
from pymongo import MongoClient
from Waifu import DATABASE

# Assuming DATABASE is properly configured
db = DATABASE["MAIN"]
collection = db["waifus"]

@waifu.on_message(filters.command("addwaifu"))
async def add_waifu_detail(_, message):
    try:
        # Ensure that the command has arguments
        if len(message.command) >= 6:
            # Extract waifu details from command arguments
            waifu_data = {
                "waifu_name": message.command[1].split(":")[1].strip(),
                "image_url": message.command[2].split(":")[1].strip(),
                "rarity": message.command[3].split(":")[1].strip(),
                "source": message.command[4].split(":")[1].strip(),
                "special_id": message.command[5].split(":")[1].strip() if len(message.command) > 5 else None
            }

            # Check if the special ID is already used for another waifu
            if waifu_data["special_id"] and collection.find_one({"special_id": waifu_data["special_id"]}):
                await message.reply(f"Special ID '{waifu_data['special_id']}' is already in use for another waifu. Please provide a different ID.")
                return

            # Save the waifu data to the database
            collection.insert_one(waifu_data)
            await message.reply("Waifu data added successfully!")

        else:
            await message.reply("Please use the /addwaifu command with the following format:\n\n/addwaifu Name: [waifu name]\nImage: [image URL]\nRarity: [rarity]\nSource: [source text]\nID: [special ID]")

    except Exception as e:
        print(f"Error adding waifu: {str(e)}")
        await message.reply("An error occurred while adding waifu data. Please check the format and try again.")

@waifu.on_message(filters.command("fetchwaifu"))
async def fetch_waifu_data(_, message):
    try:
        waifus = collection.find()

        for waifu in waifus:
            special_id = waifu.get("special_id", "N/A")
            waifu_name = waifu.get("waifu_name", "No Name")
            rarity = waifu.get("rarity", "No Rarity")
            image_url = waifu.get("image_url", "")
            source = waifu.get("source", "No Source")

            # Send the image along with the caption
            caption = f"ID: {special_id}\nName: {waifu_name}\nRarity: {rarity}\nSource: {source}"
            await message.reply_photo(
                photo=image_url,
                caption=caption
            )

    except Exception as e:
        print(f"Error fetching waifus: {str(e)}")
        await message.reply("An error occurred while fetching waifu data.")
