import os
import requests
import aiohttp
import youtube_dl
import pyrogram
from pyrogram import filters, Client
from youtube_search import YoutubeSearch

bot = Client(
   "Song Downloader",
   api_id = "2192067",
   api_hash = "d2e0ba99f1b9cdb632b43633edb76f11",
   bot_token = "1710612658:AAFLE-PZuJmN8bj4B4YX19peWvY5mjgpx7I"
)

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))
                          
                                 
                                 
@bot.on_message(filters.command('song') & ~filters.private & ~filters.channel)
def song(client, message):
    rq_txt = message.text
    rq_user = message.from_user.mention
    user_name = message.from_user.first_name 

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    rply = message.reply('🔎 𝙎𝙚𝙖𝙧𝙘𝙝𝙞𝙣𝙜 •••')
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
        rply.edit(
            "😕 Found Nothing.\n\nTry another keywork or maybe spell it properly."
        )
        print(str(e))
        return
    rply.edit("Downloading the song by @GalaxyLanka ...")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        cap = f"**Song Name ➠** `{title}` \n**Requested For :** `{rq_text}` \n**Requested By :** {rq_user} \n**Uploaded By :** @Bot"
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=cap, thumb=thumb_name, parse_mode='md', title=title, duration=dur)
        rply.delete()
    except Exception as e:
        rply.edit('❌ Error')
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
