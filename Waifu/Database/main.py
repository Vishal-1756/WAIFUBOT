from Waifu import DATABASE
from pyrogram.types import Chat

db = DATABASE["MAIN"]
collection = db["users"]

async def add_users_to_db(user_id: int):
    string = {"user_id": user_id}
    collection.insert_one(string)

async def get_users_list():
    user_ids = [x.get("user_id") for x in collection.find() if "user_id" in x]
    return user_ids

async def add_waifu_to_db(user_id: int, waifu_name: str, rarity: str, special_id: int, source: str, image_url: str):
    user_data = collection.find_one({"user_id": user_id})
    
    if user_data:
        user_waifus = user_data.get("waifu_details", [])
        
        user_waifus.append({
            "name": waifu_name,
            "rarity": rarity,
            "special_id": special_id,
            "source": source,
            "image_url": image_url  # Add image_url to the user's waifu details
        })

        collection.update_one({"user_id": user_id}, {"$set": {"waifu_details": user_waifus}})
    else:
        collection.insert_one({"user_id": user_id, "waifu_details": [{
            "name": waifu_name,
            "rarity": rarity,
            "special_id": special_id,
            "source": source,
            "image_url": image_url  # Add image_url to the user's waifu details
        }]})

async def get_user_waifus(user_id: int):
    user_data = collection.find_one({"user_id": user_id})
    if user_data:
        return user_data.get("waifu_details", [])
    else:
        return []

async def add_chat_to_db(chat: Chat):
    chat_id = chat.id
    chat_data = {"chat_id": chat_id, "type": chat.type}
    collection.insert_one(chat_data)

async def get_chats_list():
    chats = [x.get("chat_id") for x in collection.find() if "chat_id" in x]
    return chats

async def get_top_harem_groups(limit: int):
    top_groups = collection.aggregate([
        {"$match": {"type": "group"}},
        {"$unwind": "$waifu_details"},
        {"$group": {"_id": "$chat_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ])

    return [{"chat_id": group["_id"], "waifu_count": group["count"]} for group in top_groups]

async def get_chat_top_harem_users(chat_id: int, limit: int):
    top_users = collection.aggregate([
        {"$match": {"chat_id": chat_id}},
        {"$unwind": "$waifu_details"},
        {"$group": {"_id": "$user_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ])

    return [{"user_id": user["_id"], "waifu_count": user["count"]} for user in top_users]
    
