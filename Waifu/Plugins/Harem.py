from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultPhoto
from Waifu import waifu, prefix
from Waifu.Database.main import get_users_list, add_users_to_db, get_user_waifus

@waifu.on_message(filters.command("harem", prefix))
async def harem_command(_, message):
    user_id = message.from_user.id

    # Check if the user is in the database and add them if not
    if user_id not in await get_users_list():
        await add_users_to_db(user_id)

    # Create an inline keyboard with a button to view waifus
    inline_keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("View My Waifus", switch_inline_query_current_chat="view_waifus"),
            ]
        ]
    )

    # Send a message with the inline keyboard
    await message.reply(
        "Manage your harem:",
        reply_markup=inline_keyboard
    )

# Handle inline queries for viewing waifus
@waifu.on_inline_query(filters.regex("^view_waifus$"))
async def view_waifus_inline_query(_, inline_query):
    user_id = inline_query.from_user.id

    # Fetch waifus for the specific user from the database
    user_waifus = await get_user_waifus(user_id)
    
    print(f"DEBUG: User {user_id} waifus: {user_waifus}")

    results = []

    for waifu in user_waifus:
        if isinstance(waifu, dict):  # Check if waifu is a dictionary
            title = waifu.get('name', 'No Name')
            photo_url = waifu.get('image', '')
            caption = f"Name: {title}\nRank: {waifu.get('rank', 'No Rank')}\nId: {waifu.get('id', 'No Id')}\nSource: {waifu.get('source', 'No Source')}"
            
            results.append(
                InlineQueryResultPhoto(
                    title=title,
                    photo_url=photo_url,
                    thumb_url=photo_url,
                    caption=caption
                )
            )
        else:
            print(f"DEBUG: Invalid waifu data for user {user_id}: {waifu}")

    await inline_query.answer(results, cache_time=0)
