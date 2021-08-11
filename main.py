import os
import requests
import aiohttp
import youtube_dl
import pyrogram
from pyrogram import filters, Client
from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InlineQuery, InputTextMessageContent

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
    rq_text = message.text
    rq_user = message.from_user.mention
    user_name = message.from_user.first_name 
    user_id = message.from_user.id 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"  
    query = ''
    for i in message
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
