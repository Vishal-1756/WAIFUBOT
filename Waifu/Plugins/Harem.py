from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Waifu.Database.main import get_users_list, add_waifu_to_db, get_user_waifus
from Waifu import waifu, prefix 
import json

with open("waifu.json", "r") as file:
    waifus_data = json.load(file)

@waifu.on_message(filters.command("harem", prefix))
async def harem_command(_, message):
    user_id = message.from_user.id

    # Check if the user is in the database
    if user_id not in await get_users_list():
        await add_users_to_db(user_id)

    user_waifus = await get_user_waifus(user_id)

    if not user_waifus:
        await message.reply("Your harem is empty!")
        return

    # Debug: Print the content and type of waifu_data
    for waifu_data in user_waifus:
        print(f"waifu_data: {waifu_data}, type: {type(waifu_data)}")

    # Create inline buttons for each waifu
    inline_buttons = [
        [
            InlineKeyboardButton(waifu_data['name'], callback_data=f"view_waifu_{waifu_data['id']}")
        ]
        for waifu_data in user_waifus
    ]

    # Send the inline keyboard with waifu names
    await message.reply(
        "Your harem:",
        reply_markup=InlineKeyboardMarkup(inline_buttons)
    )


# Define a callback handler for viewing a specific waifu
@waifu.on_callback_query(filters.regex(r'^view_waifu_(\d+)$'))
async def view_waifu_callback(_, callback_query):
    waifu_id = int(callback_query.matches[0].group(1))
    waifu = None

    # Try to find the waifu in the JSON data
    for waifu_data in waifus_data.get("waifus", []):
        if waifu_data['id'] == waifu_id:
            waifu = waifu_data
            break

    if waifu:
        # Send the photo and waifu data
        await callback_query.message.reply_photo(
            photo=waifu['image_url'],
            caption=waifu['data']
        )
