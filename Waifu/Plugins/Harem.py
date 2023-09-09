from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Waifu.Database.main import get_user_waifus, get_waifu_by_id
from Waifu import waifu, prefix 


# Define a handler for the /harem command
@waifu.on_message(filters.command("harem", prefix))
async def harem_command(_, message):
    user_id = message.from_user.id
    user_waifus = await get_user_waifus(user_id)

    if not user_waifus:
        await message.reply("Your harem is empty!")
        return

    # Create inline buttons for each waifu
    inline_buttons = [
        [
            InlineKeyboardButton(waifu['name'], callback_data=f"view_waifu_{waifu['id']}")
        ]
        for waifu in user_waifus
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
    waifu = await get_waifu_by_id(waifu_id)

    if waifu:
        # Send the photo and waifu data
        await callback_query.message.reply_photo(
            photo=waifu['image_url'],
            caption=waifu['data']
        )


