from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Waifu.Database.main import get_top_harem_groups, get_chat_top_harem_users
from Waifu import waifu

# Define a constant for the number of users per page
USERS_PER_PAGE = 5

@waifu.on_message(filters.command("globaltop", prefixes="/"))
async def global_top(_, message):
    limit = USERS_PER_PAGE  # Adjust the limit as needed
    top_groups = await get_top_harem_groups(limit)

    if top_groups:
        await send_groups_page(_, message, top_groups, 1)  # Display the first page
    else:
        await message.reply_text("No data available for global top waifu groups.")

async def send_groups_page(_, message, group_list, page_number):
    start_index = (page_number - 1) * USERS_PER_PAGE
    end_index = start_index + USERS_PER_PAGE
    current_page_groups = group_list[start_index:end_index]

    text = f"<b>Global Top Waifu Groups - Page {page_number}:</b>\n"
    for i, group in enumerate(current_page_groups, start=start_index + 1):
        chat_id = group["chat_id"]
        waifu_count = group["waifu_count"]
        text += f"{i}. <b>Chat ID:</b> {chat_id} | <b>Waifu Count:</b> {waifu_count}\n"

    keyboard = build_pagination_keyboard(page_number, len(group_list), "groups")
    await message.reply_text(text, parse_mode="html", reply_markup=keyboard)

# Handle button clicks for pagination
@waifu.on_callback_query(filters.regex(r"^page_(\d+)"))
async def callback_handler(_, callback_query):
    page_data = callback_query.data.split("_")
    page_type = page_data[1]
    page_number = int(page_data[2])

    if page_type == "groups":
        await handle_groups_pagination(_, callback_query.message, callback_query.from_user.id, page_number)
    elif page_type == "users":
        await handle_users_pagination(_, callback_query.message, callback_query.from_user.id, page_number)

async def handle_groups_pagination(_, message, user_id, page_number):
    limit = USERS_PER_PAGE  # Adjust the limit as needed
    top_groups = await get_top_harem_groups(limit)

    if top_groups:
        await send_groups_page(_, message, top_groups, page_number)
    else:
        await message.reply_text("No data available for global top waifu groups.")

@waifu.on_message(filters.command("top", prefixes="/"))
async def chat_top(_, message):
    limit = USERS_PER_PAGE  # You can adjust the limit as needed
    chat_id = message.chat.id
    top_users = await get_chat_top_harem_users(chat_id, limit)

    if top_users:
        await send_users_page(_, message, top_users, 1)  # Display the first page
    else:
        await message.reply_text("No data available for top waifu users in this chat.")

async def send_users_page(_, message, user_list, page_number):
    start_index = (page_number - 1) * USERS_PER_PAGE
    end_index = start_index + USERS_PER_PAGE
    current_page_users = user_list[start_index:end_index]

    text = f"<b>Top Waifu Users in this Chat - Page {page_number}:</b>\n"
    for i, user in enumerate(current_page_users, start=start_index + 1):
        user_id = user["user_id"]
        waifu_count = user["waifu_count"]
        mention = f"<a href='tg://user?id={user_id}'>User</a>"
        text += f"{i}. {mention} | <b>Waifu Count:</b> {waifu_count}\n"

    keyboard = build_pagination_keyboard(page_number, len(user_list), "users")
    await message.reply_text(text, parse_mode="html", reply_markup=keyboard)

async def handle_users_pagination(_, message, user_id, page_number):
    limit = USERS_PER_PAGE  # You can adjust the limit as needed
    chat_id = message.chat.id
    top_users = await get_chat_top_harem_users(chat_id, limit)

    if top_users:
        await send_users_page(_, message, top_users, page_number)
    else:
        await message.reply_text("No data available for top waifu users in this chat.")

def build_pagination_keyboard(current_page, total_pages, page_type):
    keyboard = [
        InlineKeyboardButton("◀️ Previous", callback_data=f"page_{page_type}_{current_page - 1}") if current_page > 1 else None,
        InlineKeyboardButton(f"Page {current_page}/{total_pages}", callback_data="ignore"),
        InlineKeyboardButton("Next ▶️", callback_data=f"page_{page_type}_{current_page + 1}") if current_page < total_pages else None,
    ]

    return InlineKeyboardMarkup([button for button in keyboard if button])
