from Waifu import DATABASE
from pyrogram import filters
from pymongo import MongoClient
import asyncio
from Waifu import waifu

db = DATABASE["MAIN"]


def insert_waifu_data(waifu_name, rank, image_url):
    waifu_data = {
        "waifu_name": waifu_name,
        "rank": rank,
        "image_url": image_url
    }
    db.insert_one(waifu_data)

# Command to add waifu data
@waifu.on_message(filters.command(["addwaifu"]))
async def add_new_waifu_command(_, message):
    user_id = message.from_user.id
    input_text = message.text.split(" ", 1)[1]  # Remove the '/addwaifu' part

    # Parse the input for waifu data
    try:
        waifu_name, rank, image_url = input_text.split("-", 2)
    except ValueError:
        await message.reply("Invalid format. Use /addwaifu waifuname-rank-imageurl")
        return

    # Insert waifu data into the database
    insert_waifu_data(waifu_name, rank, image_url)
    await message.reply("Waifu data added successfully!")

# Command to fetch waifu data
@waifu.on_message(filters.command(["fetchwaifu"]))
async def fetch_waifu_data(_, message):
    waifus = db.find()  # Retrieve all waifu data from the database

    for waifu in waifus:
        waifu_name = waifu["waifu_name"]
        rank = waifu["rank"]
        image_url = waifu["image_url"]

        caption = f"Name: {waifu_name}\nRank: {rank}"
        await message.reply_photo(photo=image_url, caption=caption)


