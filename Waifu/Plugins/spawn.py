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

# Global variable to store the spawned waifu
spawned_waifu = None

# Counter to track the number of messages in the group
message_count = 0

# Your message handler for text messages in groups
@waifu.on_message(filters.text & filters.group)
async def on_text_message(_, message: Message):
    global message_count, spawned_waifu_name, spawned_waifu

    message_count += 1

    if message_count == 5:
        message_count = 0

        # Retrieve a random waifu from the database
        random_waifu = collection.aggregate([{ "$sample": { "size": 1 } }])
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

@waifu.on_message(filters.command("catch", prefix) & filters.group)
async def catch_waifu(_, message):
    global spawned_waifu_name, spawned_waifu
    
    if spawned_waifu_name and spawned_waifu:
        query = message.text.split(maxsplit=1)[1]
        
        # Check if the provided name matches the spawned waifu's name
        if query.lower() == spawned_waifu_name.lower():
            image_url = spawned_waifu.get("image_url")
            rarity = spawned_waifu.get("rarity")

            if image_url and rarity:
                user_id = message.from_user.id
                await add_waifu_to_db(user_id, spawned_waifu_name)
                caption = f"Congratulations! You caught a {rarity} {spawned_waifu_name}."
                await waifu.send_photo(chat_id=message.chat.id, photo=image_url, caption=caption)
                spawned_waifu_name = None  # Reset the spawned waifu name after catching
                spawned_waifu = None  # Reset the spawned waifu
            else:
                await waifu.send_message(chat_id=message.chat.id, text="Incomplete waifu data. Unable to send.")
        else:
            await waifu.send_message(chat_id=message.chat.id, text=f"You missed! The spawned waifu's name is {spawned_waifu_name}. Try again.")
    else:
        await waifu.send_message(chat_id=message.chat.id, text="No waifu to catch. Wait for a spawned waifu.")
