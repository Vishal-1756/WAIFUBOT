import requests
from urllib.parse import quote_plus, unquote
from bs4 import BeautifulSoup
from unidecode import unidecode
from Waifu import waifu as app
from Waifu import bot_token
from pyrogram import filters

async def Sauce(bot_token, file_id):
    r = requests.post(f'https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}').json()
    file_path = r['result']['file_path']
    headers = {'User-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'}
    to_parse = f"https://images.google.com/searchbyimage?safe=off&sbisrc=tg&image_url=https://api.telegram.org/file/bot{bot_token}/{file_path}"
    r = requests.get(to_parse, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    result = {
        "similar_google": [],
        'output_google': '',
        "similar_saucenao": '',
        'output_saucenao': ''
    }

    # Google Search
    similar_images_div = soup.find('div', {'class': 'RAyV4b'})
    if similar_images_div:
        for similar_images_link in similar_images_div.find_all('a'):
            url = f"https://www.google.com{similar_images_link['href']}"
            result['similar_google'].append(url)

    for best in soup.find_all('div', {'class': 'r5a77d'}):
        output = best.get_text()
        decoded_text = unidecode(output)
        result["output_google"] = decoded_text

    # SauceNAO Search
    saucenao_result = await SauceNAO(file_id)
    result['similar_saucenao'] = saucenao_result.get('similar', '')
    result['output_saucenao'] = saucenao_result.get('output', '')

    return result

async def SauceNAO(file_id):
    file_url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
    r = requests.post(file_url).json()
    file_path = r['result']['file_path']
    image_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"

    saucenao_url = "https://saucenao.com/search.php"
    params = {
        'output_type': 2,
        'numres': 1,
        'url': image_url
    }

    response = requests.post(saucenao_url, data=params)
    if response.status_code == 200:
        result = response.json()
        if 'results' in result and result['results']:
            best_match = result['results'][0]
            return {
                'similar': best_match['data']['ext_urls'][0] if 'ext_urls' in best_match['data'] else '',
                'output': best_match['data']['title'] if 'title' in best_match['data'] else ''
            }

    return {'similar': '', 'output': ''}

async def get_file_id_from_message(msg):
    file_id = None
    message = msg.reply_to_message
    if not message:
        return
    if message.document:
        if int(message.document.file_size) > 3145728:
            return
        mime_type = message.document.mime_type
        if mime_type not in ("image/png", "image/jpeg"):
            return
        file_id = message.document.file_id

    if message.sticker:
        if message.sticker.is_animated:
            if not message.sticker.thumbs:
                return
            file_id = message.sticker.thumbs[0].file_id
        else:
            file_id = message.sticker.file_id

    if message.photo:
        file_id = message.photo.file_id

    if message.animation:
        if not message.animation.thumbs:
            return
        file_id = message.animation.thumbs[0].file_id

    if message.video:
        if not message.video.thumbs:
            return
        file_id = message.video.thumbs[0].file_id
    return file_id

@app.on_message(filters.command(["pp", "grs", "reverse", "r"]) & filters.group)
async def _reverse(_, msg):
    text = await msg.reply("** wait a sec...**")
    file_id = await get_file_id_from_message(msg)
    if not file_id:
        return await text.edit("**reply to media!**")
    
    await text.edit("** Searching in Google and SauceNAO....**")
    result = await Sauce(bot_token, file_id)

    if not result["output_google"] and not result["output_saucenao"]:
        return await text.edit("Couldn't find anything")

    reply_text = (
        f'Google: {result["output_google"]}\n[Similar Images]({result["similar_google"]})\n\n'
        f'SauceNAO: {result["output_saucenao"]}\n[Similar Images]({result["similar_saucenao"]})'
    )

    await text.edit(reply_text)
