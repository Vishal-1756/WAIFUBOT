from Waifu import DATABASE

db = DATABASE["MAIN"]

async def add_users_to_db(user_id: int):
     string = {"user_id": user_id}
     db.insert_one(string)

async def get_users_list():
     list = [x["user_id"] for x in db.find()]
     return lis
