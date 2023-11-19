from Waifu import DATABASE

db = DATABASE["MAIN"]

async def add_users_to_db(user_id: int):
     string = {"user_id": user_id}
     db.insert_one(string)

async def get_users_list():
     user_ids = [x.get("user_id") for x in db.find() if "user_id" in x]
     return user_ids

async def add_waifu_to_db(user_id: int, waifu_name: str, rarity: str, special_id: str, source: str):
    user_data = db.find_one({"user_id": user_id})
    
    if user_data:
        user_waifus = user_data.get("waifus", [])
        user_waifu_details = user_data.get("waifu_details", [])

        user_waifus.append(waifu_name)
        user_waifu_details.append({
            "name": waifu_name,
            "rarity": rarity,
            "special_id": special_id,
            "source": source
        })

        db.update_one({"user_id": user_id}, {"$set": {"waifus": user_waifus, "waifu_details": user_waifu_details}})
    else:
        db.insert_one({"user_id": user_id, "waifus": [waifu_name], "waifu_details": [{
            "name": waifu_name,
            "rarity": rarity,
            "special_id": special_id,
            "source": source
        }]})


async def get_user_waifus(user_id: int):
    user_data = db.find_one({"user_id": user_id})
    if user_data:
        return [
            {"name": waifu.get("name", "N/A"),
             "rarity": waifu.get("rarity", "N/A"),
             "id": waifu.get("id", "N/A"),
             "source": waifu.get("source", "N/A")} for waifu in user_data.get("waifus", []) if isinstance(waifu, dict)
        ]
    else:
        return []
