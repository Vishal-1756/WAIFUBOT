from pyrogram import Client, filters, types
from telegraph import upload_file
from json import JSONDecodeError
import requests
from Waifu import waifu as app

API_URL = "https://reverse-pbq1.onrender.com/reverse?url={url}"
API_URL_BING = "https://api.qewertyy.me/image-reverse/bing?img_url={url}"

async def telegraph(message, path):
    try:
        telegraph_file = upload_file(path)
    except JSONDecodeError:
        await message.reply_text("Failed To Upload.")
        url = False
        return url

    try:
        url = "https://telegra.ph/" + telegraph_file[0]
    except:
        pass

    return url

def create_buttons(request_url, similar_urls, more_results_text):
    keyboard = [
        [
            types.InlineKeyboardButton("Request URL", url=request_url),
            types.InlineKeyboardButton("Similar URLs", url=similar_url)
        ],
        [
            types.InlineKeyboardButton("More Results", callback_data=f"more_results:{more_results_text}")
        ]
    ]
    return types.InlineKeyboardMarkup(keyboard)
    

@app.on_message(filters.command("kela") & filters.reply)
async def reverse_search(client, message):
    reply_message = message.reply_to_message

    if reply_message.photo:
        photo_path = await reply_message.download()
        telegraph_url = await telegraph(message, photo_path)
        url = API_URL.format(url=telegraph_url)
        url2 = API_URL_BING.format(url=telegraph_url)
    elif reply_message.text:
        url = API_URL.format(url=telegraph_url)
        url2 = API_URL_BING.format(url=telegraph_url)
    else:
        await message.reply_text("Unsupported message type. Reply to an image or provide a URL.")
        return

    try:
        response = requests.get(url)
        response2 = requests.get(url2)
        result = response.json()
        result2 = response2.json()
        image_description = result["result"]["image"]
        request_url = result["result"]["requestUrl"]
        similar_url = result.get("similarUrl", [])
        results2 = result2.get("bestResults", [])
        image_descriptions2 = [res["name"] for res in results2[:10]]
        urls2 = [res["url"] for res in results2[:10]]
        more_results_text = "\n".join([f"{i + 1}. {desc}: {url}" for i, (desc, url) in enumerate(zip(image_descriptions2, urls2))])

        buttons = create_buttons(request_url, similar_urls, more_results_text)
        text = f"From Google Search Engine: {image_description}\n\nFrom Bing Search Engine:\n"
        text += "\n".join([f"{i + 1}. {desc}" for i, desc in enumerate(image_descriptions2)])

        await message.reply_text(text, reply_markup=buttons)
    except Exception as e:
        await message.reply_text(f"Error fetching information: {str(e)}")


