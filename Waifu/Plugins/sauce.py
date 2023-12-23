from pyrogram import Client, filters, types
from telegraph import upload_file
from json import JSONDecodeError
import requests
from Waifu import waifu as app
from telegraph import Telegraph, upload_file

API_URL = "https://reverse-pbq1.onrender.com/reverse?url={url}"
API_URL_BING = "https://api.qewertyy.me/image-reverse/bing?img_url={url}"

telegraph = Telegraph()
telegraph.create_account(short_name='BingImageSearchResults')

def upload_to_telegraph(file_path, text_content=None):
    try:
        if text_content:
            response = telegraph.create_page(
                f"Caption: {text_content}",
                content=[("p", text_content)]
            )
            telegraph_url = 'https://telegra.ph/{}'.format(response['path'])
        else:
            telegraph_file = upload_file(file_path)
            telegraph_url = "https://telegra.ph/" + telegraph_file[0]

        return telegraph_url
    except Exception as e:
        print(f"Error uploading to Telegraph: {str(e)}")
        return None

def create_buttons(request_url, similar_urls, more_results_text_url):
    keyboard = [
        [
            types.InlineKeyboardButton("Request URL", url=request_url),
            types.InlineKeyboardButton("Similar URLs", url=similar_url)
        ],
        [
            types.InlineKeyboardButton("More Results", url=more_results_text_url)
        ]
    ]
    return types.InlineKeyboardMarkup(keyboard)

@app.on_message(filters.command("kela") & filters.reply)
async def reverse_search(client, message):
    reply_message = message.reply_to_message
     
    if reply_message.photo:
        await message.reply_text("`Parsing Your Media Wait`")
        photo_path = await reply_message.download()
        telegraph_url = upload_to_telegraph(photo_path)
        url = API_URL.format(url=telegraph_url)
        url2 = API_URL_BING.format(url=telegraph_url)            
    else:
        await message.reply_text("Unsupported type. Reply to an image")
        return

    try:
        response = requests.get(url)
        response2 = requests.get(url2)
        result = response.json()
        result2 = response2.json()
        image_description = result["result"]["image"]
        request_url = result["result"]["requestUrl"]
        similar_urls = result.get("similarUrl", [])
        results2 = result2.get("bestResults", [])
        image_descriptions2 = [res["name"] for res in results2[:10]]
        urls2 = [res["url"] for res in results2[:10]]
        more_results_text = "\n".join([f"{i + 1}. {desc}: {url}" for i, (desc, url) in enumerate(zip(image_descriptions2, urls2))])

        more_results_text_url = await upload_to_telegraph(None, more_results_text)
        buttons = create_buttons(request_url, similar_urls, more_results_text_url)
        text = f"From Google Search Engine: {image_description}\n\nFrom Bing Search Engine:\n"
        text += "\n".join([f"{i + 1}. {desc}" for i, desc in enumerate(image_descriptions2)])

        await message.reply_text(text, reply_markup=buttons)
    except Exception as e:
        await message.reply_text(f"Error fetching information: {str(e)}")
