import discord
from bs4 import BeautifulSoup
import requests
import io

client = discord.Client()

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(message.author.name)

    #Botch for mantaro bot playlists from youtube
    if message.content.find('Now playing'):


        time = message.content.find(') on ') - 8 #botched but should work about half the time - TO IMPROVE
        song = message.content[16:time]

        print(song)


        try:

            url = 'https://www.google.es/search?q=' + song.replace(' ','+')
            response = requests.get(url, headers=headers)
            soup_pre_js = BeautifulSoup(response.text, "html.parser")
            soup = BeautifulSoup(soup_pre_js.prettify(), "html.parser")
            lyrics = soup.select('div[data-lyricid]')[0]
            clean_lyrics = lyrics.text.replace('                                 ', '')
            clean_lyrics = clean_lyrics.replace("\n\n\n", "")
            print(clean_lyrics[0:200])

            with io.open('test.txt', "w", encoding="utf-8") as f:
                f.write(clean_lyrics)

            await message.channel.send(file=discord.File('test.txt'))
        
        except (Exception, ArithmeticError) as e:
            template = "Exception type {0}.\n{1!r}"
            await message.channel.send(template.format(type(e).__name__, e.args))
            print (message)

            #Logging song failed
            content = ""
            with io.open('failed.txt', "r", encoding="utf-8") as f:
                content = f.read()

            with io.open('failed.txt', "w", encoding="utf-8") as f:
                f.write(content + song + "\n")

client.run('YourKey')