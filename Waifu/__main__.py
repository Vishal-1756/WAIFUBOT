import pyrogram

from Waifu import waifu , app 

async def run_clients():
      await app.start()
      await waifu.start()
      await pyrogram.idle()
      

if __name__ == "__main__":
    waifu.loop.run_until_complete(run_clients())
