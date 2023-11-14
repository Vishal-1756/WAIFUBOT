import random
from pyrogram import filters, Client
from pyrogram.types import Message
from Waifu.Database.main import add_waifu_to_db
from Waifu import waifu, prefix
from Waifu import DATABASE

db = DATABASE["MAIN"]
collection = db["waifus"]

# Variable to store the name of the spawned waifu
spawned_waifu_name = None

# Counter to track the number of messages in the group
message_count = 0

# Your message handler for text messages in groups
@waifu.on_message(filters.text & filters.group)
async def on_text_message(_, message: Message):
    global message_count, spawned_waifu_name

    message_count += 1

    if message_count == 5:
        message_count = 0

        # Retrieve a random waifu from the database
        random_waifu = collection.aggregate([{ "$sample": { "size": 1 } } ])
        spawned_waifu = next(random_waifu, None)

        if spawned_waifu:
            spawned_waifu_name = spawned_waifu.get("waifu_name")
            image_url = spawned_waifu.get("image_url")
            rarity = spawned_waifu.get("rarity")

            if image_url and rarity:
                caption = f"UwU {rarity} just appeared in the group! Catch it by using /catch {spawned_waifu_name}"
                await waifu.send_photo(chat_id=message.chat.id, photo=image_url, caption=caption)
            else:
                await waifu.send_message(chat_id=message.chat.id, text="Incomplete waifu data. Unable to send.")
        else:
            await waifu.send_message(chat_id=message.chat.id, text="No waifus found in the database.")
