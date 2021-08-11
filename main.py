import os
import requests
import aiohttp
import youtube_dl
import pyrogram
import json
from pyrogram import filters, Client
from youtube_search import YoutubeSearch
from youtubesearchpython import SearchVideos
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InlineQuery, InputTextMessageContent
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)
bot = Client(
   "Song Downloader",
   api_id = "2192067",
   api_hash = "d2e0ba99f1b9cdb632b43633edb76f11",
   bot_token = "1710612658:AAFLE-PZuJmN8bj4B4YX19peWvY5mjgpx7I"
)

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))
                          
                                 
@bot.on_message(filters.command("start"))
async def start(client, message):
   if message.chat.type == 'private':
       await bot.send_message(
               chat_id=message.chat.id,
               text="""<b>Hey There, I'm a Song Downloader Bot. A bot by @FuckMeSoon.

Hit help button to find out more about how to use me</b>""",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "Help", callback_data="help"),
                                        InlineKeyboardButton(
                                            "Channel", url="https://t.me/sindupotha")
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html",
            reply_to_message_id=message.message_id
        )
   else:
       await bot.send_message(
               chat_id=message.chat.id,
               text="""<b>Song Downloader Is Online.\n\n</b>""",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "Help", callback_data="help")
                                        
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html",
            reply_to_message_id=message.message_id
        )
@bot.on_message(filters.command("help"))
async def help(client, message):
    if message.chat.type == 'private':   
        await bot.send_message(
               chat_id=message.chat.id,
               text="""<b>Send a Song Name to Download Song </b>""",
            reply_to_message_id=message.message_id
        )
    else:
        await bot.send_message(
               chat_id=message.chat.id,
               text="<b>Song Downloader Help.\n\nSyntax: /song `Song Name`</b>",
            reply_to_message_id=message.message_id
        ) 

         
@bot.on_message(filters.private & ~filters.bot & ~filters.command("help") & ~filters.command("start") & ~filters.command("s"))
async def song(client, message):
    url = message.text
    user = message.from_user.mention
    rkp = await message.reply("Processing...")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    capz = q[0]["title"]
    cap = f"**Song Name ➠** `{capz}` \n**Requested For :** `{url}` \n**Requested By :** {user} \n**Uploaded By :** @Bot"
    try:
        url = q[0]["link"]
    except BaseException:
        return await rkp.edit("Failed to find that song.")
    type = "audio"
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        song = True
    try:
        await rkp.edit("Downloading...")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await rkp.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await rkp.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await rkp.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await rkp.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await rkp.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await rkp.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await rkp.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await rkp.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await rkp.edit(f"{str(type(e)): {str(e)}}")
        return
    time.time()
    if song:
        await rkp.edit("Uploading...") 
        lol = "./SinduPotha.png"
        lel = await message.reply_audio(
                 f"{rip_data['id']}.mp3",
                 duration=int(rip_data["duration"]),
                 title=str(rip_data["title"]),
                 performer=str(rip_data["uploader"]),
                 thumb=lol,
                 caption=cap)  
        await rkp.delete()
         
@bot.on_message(filters.command('song') & ~filters.private & ~filters.channel)
def song(client, message):
    rq_text = message.text.split(None, 1)[1]
    rq_user = message.from_user.mention
    user_name = message.from_user.first_name 
    user_id = message.from_user.id 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"  
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('🔎 𝙎𝙚𝙖𝙧𝙘𝙝𝙞𝙣𝙜 •••')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)


        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        m.edit(
            "😕 Found Nothing.\n\nTry another keywork or maybe spell it properly."
        )
        print(str(e))
        return
    m.edit("Downloading the song  ...")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
            rep = f"**Song Name ➠** `{title}` \n**Requested For :** `{rq_text}` \n**Requested By :** {rq_user} \n**Uploaded By :** @Bot"
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, thumb=thumb_name, title=title, duration=dur)
        m.delete()
    except Exception as e:
        m.edit('❌ Error')
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
print(
    """
Bot Started!
Join @FuckMeSoon
"""
)
bot.run()
