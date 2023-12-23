from pyrogram import Client, filters, types
from telegraph import upload_file
from json import JSONDecodeError
import requests
from telegraph import Telegraph
from Waifu import waifu as app

API_URL = "https://api.qewertyy.me/image-reverse/google?img_url={url}"
API_URL_BING = "https://api.qewertyy.me/image-reverse/bing?img_url={url}"

telegraph = Telegraph()
telegraph.create_account(short_name="The Team X")

def upload_text_to_telegraph(text_content):
    try:
        response = telegraph.create_page(
            title='Bing Image Search',
            html_content=text_content,
            author_name='TeamX',
            author_url='https://telegram.dog/team_devsX'
        )
        telegraph_url = 'https://telegra.ph/{}'.format(response['path'])
        return telegraph_url
    except Exception as e:
        print(f"Error uploading text to Telegraph: {str(e)}")
        return None

async def telegraph_upload(path):
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

def create_buttons(more_results_text_url_google, more_results_text_url_bing):
    keyboard = [
        [
            types.InlineKeyboardButton("Similar Image Google", url=more_results_text_url_google),
            types.InlineKeyboardButton("More Bing Results", url=more_results_text_url_bing)
        ]
    ]
    return types.InlineKeyboardMarkup(keyboard)

@app.on_message(filters.command("kela") & filters.reply)
async def reverse_search(client, message):
    reply_message = message.reply_to_message
    
    if reply_message.photo:
        m = await message.reply_text("`Parsing Your Media Wait`")
        photo_path = await reply_message.download()
        telegraph_url = await telegraph_upload(photo_path)
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
        results = result.get("content", {}).get("bestResults", {}).get("names", [])      
        
        results2 = result2.get("content", {}).get("bestResults", {}).get("names", [])
        urls2 = result2.get("content", {}).get("bestResults", {}).get("urls", [])
        more_results_text = "\n".join([f"{i + 1}. {desc}: {url}" for i, (desc, url) in enumerate(zip(results2, urls2))])
        more_results_texts = str(more_results_text)
        
        if telegraph_url:
            print(f"more_results_texts: {more_results_texts}")
            more_results_text_url_bing = upload_text_to_telegraph(more_results_texts)
            more_results_text_url_google = f"https://images.google.com/searchbyimage?safe=off&sbisrc=tg&image_url={telegraph_url}"
            buttons = create_buttons(more_results_text_url_google, more_results_text_url_bing)
            text = f"From Google Search Engine:\n"
            text += "\n".join([f"{i + 1}. {desc}" for i, desc in enumerate(results)])
            text += "\n\nFrom Bing Search Engine:\n"
            text += "\n".join([f"{i + 1}. {desc}" for i, desc in enumerate(results2)])
        else:
            buttons = create_buttons(None, None)
            text = f"From Google Search Engine:\n"
            text += "\n".join([f"{i + 1}. {desc}" for i, desc in enumerate(results)])
            text += "\n\nFrom Bing Search Engine:\n"
            text += "\n".join([f"{i + 1}. {desc}" for i, desc in enumerate(results2)])

        await message.reply_text(text, reply_markup=buttons)
        m.delete()
    except Exception as e:
        await message.reply_text(f"Error fetching information: {str(e)}")
