from Waifu import DATABASE
from pyrogram import filters
from pymongo import MongoClient
import asyncio
from Waifu import waifu

db = DATABASE["MAIN"]

def insert_waifu_data(user_id, waifu_name, rank, images):
    waifu_data = {
        "user_id": user_id,
        "waifu_name": waifu_name,
        "rank": rank,
        "images": images
    }
    db.insert_one(waifu_data)

# Command to add waifu data
@waifu.on_message(filters.command(["addwaifu"]))
async def add_new_waifu_command(_, message):
    user_id = message.from_user.id

    # Ask for the waifu's name
    await message.reply("Please reply with the name of the waifu:")
    waifu_name = (await waifu.listen(user=user_id)).text

    # Ask for the waifu's rank
    await message.reply("Please reply with the rank of the waifu (text or number):")
    rank = (await waifu.listen(user=user_id)).text

    images = []

    # Ask for image URLs
    await message.reply("Now, please reply with image URLs one by one. Send 'done' when you're finished.")

    while True:
        image_url = (await waifu.listen(user=user_id)).text
        if image_url.lower() == "done":
            break
        images.append(image_url)

    # Insert waifu data into the database
    insert_waifu_data(user_id, waifu_name, rank, images)
    await message.reply("Waifu data added successfully!")


