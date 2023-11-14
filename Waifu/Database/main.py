from Waifu import DATABASE

db = DATABASE["MAIN"]

async def add_users_to_db(user_id: int):
     string = {"user_id": user_id}
     db.insert_one(string)

async def get_users_list():
     user_ids = [x.get("user_id") for x in db.find() if "user_id" in x]
     return user_ids

async def add_waifu_to_db(user_id: int, waifu_name: str):
    user_data = db.find_one({"user_id": user_id})
    if user_data:
        user_waifus = user_data.get("waifus", [])
        user_waifus.append(waifu_name)
        db.update_one({"user_id": user_id}, {"$set": {"waifus": user_waifus}})
    else:
        db.insert_one({"user_id": user_id, "waifus": [waifu_name]})

async def get_user_waifus(user_id: int):
    user_data = db.find_one({"user_id": user_id})
    if user_data:
        return [{"name": waifu_name, "rarity": rarity, "id": special_id, "source": source} for waifu_name in user_data.get("waifus", [])]
    else:
        return []
