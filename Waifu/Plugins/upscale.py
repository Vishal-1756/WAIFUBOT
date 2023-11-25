import requests
from PIL import Image
from io import BytesIO
import os
import base64
from pyrogram import *
from Waifu import waifu as app
import asyncio
from lexica import AsyncClient
from lexica.constants import languageModels

async def getFile(message):
    if not message.reply_to_message:
        return None
    if message.reply_to_message.document is False or message.reply_to_message.photo is False:
        return None
    if message.reply_to_message.document and message.reply_to_message.document.mime_type in ['image/png','image/jpg','image/jpeg'] or message.reply_to_message.photo:
        image = await message.reply_to_message.download()
        return image
    else:
        return None


async def UpscaleImages(image: bytes) -> str:
    """
    Upscales an image and return with upscaled image path.
    """
    try:
        client = AsyncClient()
        content = await client.upscale(image)
        await client.close()
        upscaled_file_path = "upscaled.png"
        with open(upscaled_file_path, "wb") as output_file:
            output_file.write(content)
        return upscaled_file_path
    except Exception as e:
        raise Exception(f"Failed to upscale the image: {e}")

@app.on_message(filters.command("upscale"))
async def upscale(client,message):
    try:
        image = await message.reply_to_message.download()
    except:
        return await message.reply_text("reply to an image to upscale images.")
    temp = await message.reply_text("**wait a moment upscaling your image....**")
    with open(image, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())
    img = encoded_image.decode('utf-8')
    response = requests.post("https://alphacoder-api.vercel.app/v2/upscale",json={"image": img})
    try:
        link = response.json()["image_url"]
        resp = requests.get(link)
        data = resp.content
        Img = Image.open(BytesIO(data))
        Img.save("upscale.png")
        await message.reply_document("upscale.png")
        await temp.delete()
        os.remove("upscale.png")
    except:
        return await temp.edit_text("**Try again after 10 seconds.**")

@app.on_message(filters.command(["up"]))
async def upscaleImages(_, message):
    file = await getFile(message)
    if file is None:
        return await message.reply_text("`Dear Pro Ppls Reply To a Media File 🗃️`")
    msg = await message.reply("`Requesting to api wait...`")
    imageBytes = open(file,"rb").read()
    os.remove(file)
    upscaledImage = await UpscaleImages(imageBytes)
    try:
      await message.reply_document(open(upscaledImage,"rb"))
      await msg.delete()
      os.remove(upscaledImage)
    except Exception as e:
       await msg.edit(f"{e}").save("upscale.png")
        await message.reply_document("upscale.png")
        await temp.delete()
        os.remove("upscale.png")
    except:
        return await temp.edit_text("**Try again after 10 seconds.**")


