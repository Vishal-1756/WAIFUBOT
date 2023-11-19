from pyrogram import filters
from Waifu import waifu
from pymongo import MongoClient
from Waifu import DATABASE

db = DATABASE["MAIN"]

async def add_waifu_data_to_db(waifu_data: dict):
    db.insert_one(waifu_data)

async def fetch_all_waifu_data_from_db():
    return list(db.find())

# Example command usage
@waifu.on_message(filters.command("addwaifu"))
async def add_waifu_command(_, message):
    try:
        # Parse waifu details from the command
        args = message.text.split("\n")[1:]
        waifu_name = next((arg.split(":")[1].strip() for arg in args if "Name:" in arg), "")
        image_url = next((arg.split(":")[1].strip() for arg in args if "Image:" in arg), "")
        rarity = next((arg.split(":")[1].strip() for arg in args if "Rarity:" in arg), "")
        special_id = next((arg.split(":")[1].strip() for arg in args if "ID:" in arg), "")
        source = next((arg.split(":")[1].strip() for arg in args if "Source:" in arg), "")

        # Check if all required fields are present
        if not all([waifu_name, image_url, rarity, special_id, source]):
            raise ValueError("Missing required field(s)")

        waifu_data = {
            "name": waifu_name,
            "image_url": image_url,
            "rarity": rarity,
            "special_id": special_id,
            "source": source
        }

        # Add waifu data to the database
        await add_waifu_data_to_db(waifu_data)

        await message.reply("Waifu data added successfully!")

    except Exception as e:
        print(f"Error adding waifu: {str(e)}")
        await message.reply("An error occurred while adding waifu data. Please check the format and try again.")

# Example command usage
@waifu.on_message(filters.command("fetchwaifu"))
async def fetch_waifu_command(_, message):
    try:
        # Fetch all waifu data from the database
        all_waifus = await fetch_all_waifu_data_from_db()

        if all_waifus:
            # Format and send waifu data
            waifu_list = "\n".join(f"Name: {waifu.get('name', 'N/A')}, Image: {waifu.get('image_url', 'N/A')}, Rarity: {waifu.get('rarity', 'N/A')}, ID: {waifu.get('special_id', 'N/A')}, Source: {waifu.get('source', 'N/A')}" for waifu in all_waifus)
            await message.reply(f"All waifus:\n{waifu_list}")
        else:
            await message.reply("No waifus found in the database.")

    except Exception as e:
        print(f"Error fetching waifus: {str(e)}")
        await message.reply("An error occurred while fetching waifu data.")
