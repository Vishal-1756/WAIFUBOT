from Waifu import DATABASE

db = DATABASE["MAIN"]

async def add_users_to_db(user_id: int):
     string = {"user_id": user_id}
     db.insert_one(string)

async def get_users_list():
     user_ids = [x.get("user_id") for x in db.find() if "user_id" in x]
     return user_ids

async def add_waifu_to_db(user_id: int, waifu_name: str, rarity: str, special_id: int, source: str, image_url: str):
    user_data = db.find_one({"user_id": user_id})
    
    if user_data:
        user_waifus = user_data.get("waifu_details", [])
        
        user_waifus.append({
            "name": waifu_name,
            "rarity": rarity,
            "special_id": special_id,
            "source": source,
            "image_url": image_url  # Include image_url
        })

        db.update_one({"user_id": user_id}, {"$set": {"waifu_details": user_waifus}})
    else:
        db.insert_one({"user_id": user_id, "waifu_details": [{
            "name": waifu_name,
            "rarity": rarity,
            "special_id": special_id,
            "source": source,
            "image_url": image_url  # Include image_url
        }]})


async def get_user_waifus(user_id: int):
    user_data = db.find_one({"user_id": user_id})
    if user_data:
        return user_data.get("waifu_details", [])
    else:
        return []
