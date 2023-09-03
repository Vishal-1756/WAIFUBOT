from Waifu import DATABASE

db = DATABASE["MAIN"]

async def add_users_to_db(user_id: int):
     string = {"user_id": user_id}
     db.insert_one(string)

async def get_users_list():
     list = [x["user_id"] for x in db.find()]
     return lis

async def add_waifu_to_db(user_id: int, waifu_name: str):
    user_data = db.find_one({"user_id": user_id})
    if user_data:
        user_waifus = user_data.get("waifus", [])
        user_waifus.append(waifu_name)
        db.update_one({"user_id": user_id}, {"$set": {"waifus": user_waifus}})
    else:
        collection.insert_one({"user_id": user_id, "waifus": [waifu_name]})

async def get_user_waifus(user_id: int):
    user_data = db.find_one({"user_id": user_id})
    if user_data:
        return user_data.get("waifus", [])
    else:
        return []
