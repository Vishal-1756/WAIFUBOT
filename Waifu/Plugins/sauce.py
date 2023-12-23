from pyrogram import Client, filters, types
from telegraph import upload_file
from json import JSONDecodeError
import requests
from Waifu import waifu as app
from telegraph import Telegraph

API_URL = "https://api.qewertyy.me/image-reverse/google?img_url={url}"
API_URL_BING = "https://api.qewertyy.me/image-reverse/bing?img_url={url}"

telegraph = Telegraph()
telegraph.create_account(short_name='TeamX')

def upload_text_to_telegraph(text_content):
    try:
        response = telegraph.create_page(
            title='Bing Image Search',
            content=[('p', text_content)]
        )
        telegraph_url = 'https://telegra.ph/{}'.format(response['path'])
        return telegraph_url
    except Exception as e:
        print(f"Error uploading text to Telegraph: {str(e)}")
        return None

async def telegraph(path):
    try:
        telegraph_file = upload_file(path)
    except JSONDecodeError:        
        print("Failed To Upload 🚫.")
        url = False
        return url
    try:
        for file_id in telegraph_file:
            telegraph_url = "https://graph.org/" + file_id
    except:
        pass
    return telegraph_url

def create_buttons(request_url, similar_url, more_results_text_url):
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
        m = await message.reply_text("`Parsing Your Media Wait`")
        photo_path = await reply_message.download()
        telegraph_url = telegraph(photo_path)
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
        results = result.get("bestResults", [])      
        
        results2 = result2.get("bestResults", [])
        image_descriptions2 = [res["name"] for res in results2[:10]]
        urls2 = [res["url"] for res in results2[:10]]
        more_results_text = "\n".join([f"{i + 1}. {desc}: {url}" for i, (desc, url) in enumerate(zip(image_descriptions2, urls2))])

        if telegraph_url:
            more_results_text_url = upload_text_to_telegraph(more_results_text)
            buttons = create_buttons(request_url, similar_url, more_results_text_url)
            text = f"From Google Search Engine: {image_description}\n\nFrom Bing Search Engine:\n"
            text += "\n".join([f"{i + 1}. {desc}" for i, desc in enumerate(image_descriptions2)])
        else:
            buttons = create_buttons(request_url, similar_url, None)
            text = f"From Google Search Engine: {image_description}\n\nFrom Bing Search Engine:\n"
            text += "\n".join([f"{i + 1}. {desc}" for i, desc in enumerate(image_descriptions2)])

        await message.reply_text(text, reply_markup=buttons)
        m.delete()
    except Exception as e:
        await message.reply_text(f"Error fetching information: {str(e)}")
