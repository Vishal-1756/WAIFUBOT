import pyrogram

from Waifu import waifu

async def run_clients():
      await waifu.start()
      await pyrogram.idle()
      

if __name__ == "__main__":
    waifu.loop.run_until_complete(run_clients())
