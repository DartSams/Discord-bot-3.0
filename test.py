import discord
from discord.ext import tasks,commands
# from discord.ext.commands import Bot
from dotenv import load_dotenv
import os
import random
import json
# from games.slots import *
from MyDB import *
# from games.blackjack import *
# from test_table import *
# from webscrape.scrape_anime_characters import *
# from webscrape.nyia_scrape import *



##docs##
#https://discordpy.readthedocs.io/en/latest/api.html
#dev portal (make a bot)

##needs intents to check member status's like when joining/leaving server...
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = '.',intents=intents)
load_dotenv()

guildMembers = {}
sauce_channels = ["marinara","test-games"]
game_channels = ["marinara","test-games"]
starting_balance = 1000
playerDict={}

@bot.event
async def on_ready():
    #on startup says (bot name) is here-means code is working
    print(f"{bot.user} is here")

    ##shows every server that the bot is on
    for i in bot.guilds:
        # print(i.name)
        # print(i.members)
        # print(i.id)
        guildMembers[i.name] = {} #gets all servers bot is in and creates empty dict of that name
        
        ##list all the members in every server that the bot is in
        for member in i.members:
            # print(member.name,member.discriminator)
            # insert_user(f'{member.discriminator}',starting_balance)
            guildMembers[i.name][member.name] = [member.name,member.discriminator] #gets all users in current server loop and creates new entry

        ##list all the channels
        # for channel in i.channels:
        #     print(f"channel: {channel} - id: {channel.id}")


    # print(guildMembers)
    auto_send.start() #function to automatically send messages to any channel using the channel id


@bot.command
async def on_message(message):
    global dealer_draw_count,game_on
    print(message.content)
    my_message=message.content.lower().split(' ')
    # print(message) (prints dict of all the properties of a message)
    # print(message.content) (prints what the message said)
    # print(message.author) (prints who said the message)
    # print(message.channel.name) (prints what channel the message came from)

    if my_message[0] == ".search":
        # my_message.pop(0)
        # character = "_".join(my_message[1:])
        character = my_message[1]
        print(character)
        with open(r"nyia.json","r") as f:
            images_list = json.load(f)
            images_sent = 0
            c = len(images_list[character])

            if len(my_message) > 2:
                for i in range(int(my_message[2])):
                    image = images_list[character][str(random.randrange(0,c))]
                    await message.channel.send(image)
                    images_sent += 1
                await message.channel.send(f"{images_sent} images sent")
            
            else: #if there is no my_message[2] then automatically send 50 images
                for i in range(50):
                    image = images_list[character][str(i)]
                    await message.channel.send(image)
                    images_sent += 1
                await message.channel.send(f"{images_sent} images sent")
            

    #detect if someone says (.hello) in any channel
    if message.content=='.hello':
        # print(f"Message from {message.channel}") #testing what is returned during direct message
        await message.channel.send(f'hello {message.author}')
        
    
    #differentiate between channels
    # if message.channel.name=='general':
    #     print('message in general')

    #ignore this person messages
    if message.author.name=='SecondAccount':
        pass

    ##for setting up personal commands
    if message.author.name=='Enemy of my Enemy' and message.author.discriminator=='3977':
        # print("\nmessage details:")
        # print(message)
        print("\nmessage content:")
        print(f"{message.content} \n")
        # my_message=message.content.lower().split(' ')
        print("message after split:")
        print(my_message)


@tasks.loop(hours=1.0)
async def auto_send():
    """
    channel: Text Channels - id: 795114714560069692
    channel: Voice Channels - id: 795114714560069693
    channel: the-rooftop - id: 795114714560069694
    channel: General - id: 795114714560069695
    channel: 18+ - id: 829488433642733578
    channel: nudes - id: 829488509067853904
    channel: hentai - id: 829488639783993345
    channel: marinara - id: 829488855686053938
    channel: clips - id: 829488935909589073
    channel: memes - id: 829489020127936544
    channel: ps4 - id: 829489726020911156
    channel: xbox - id: 829489749776400494
    channel: pc - id: 829489777745199164
    channel: switch - id: 829489802079371294
    channel: test-games - id: 830504789241757806
    channel: music - id: 830554770435473508
    channel: weeb-world - id: 830555229862494239
    """ #all channel names and channel id
    tag_str = {
        "0":"media",
        "1":"nsfw",
        "2":"furry",
        "3":"futa",
        "4":"yaoi",
        "5":"yuri",
        "6":"traps",
        "7":"irl"
    }
    #sends random image irl image to nude channel
    channel_nude = await bot.fetch_channel('829488509067853904')
    with open(r"images.json") as f:
        images_list = json.load(f)
        
        image = images_list["irl"][str(random.randint(0,4607))]
        await channel_nude.send(image["link"])

    # #sends random image nsfw or media image to hentai channel
    channel_hentai = await bot.fetch_channel('829488639783993345')
    with open(r"images.json") as f: 
        images_list = json.load(f)
        
        image = images_list[tag_str[str(random.randrange(0,2))]][str(random.randint(0,4607))]
        await channel_hentai.send(image["link"])

    #sends random image meme image to meme channel
    channel_meme = await bot.fetch_channel('829489020127936544')
    with open(r"memes.json") as f: 
        meme_list = json.load(f)
        
        for i in range(1):
            meme = meme_list["meme"][str(random.randint(0,759))]
            await channel_meme.send(meme)

@bot.event
async def on_member_join(member):
    print(member)
    print(f"{member} joins the frey")
    insert_user(f'{member.discriminator}',starting_balance)
    await member.send(f"Welcome to the Server")

@bot.event
async def on_member_remove(member):
    print(member)
    print(f"{member} has left the server")
     
    delete_user(f"{member.discriminator}")



bot.run(os.getenv('discord_token'))
