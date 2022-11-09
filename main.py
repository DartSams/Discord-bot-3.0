import discord
from discord.ext import tasks,commands
from discord.utils import get
# from discord.ext.commands import Bot
from dotenv import load_dotenv
import os
import random
import json
# from games.slots import *
from MyDB import *


##needs intents to check member status's like when joining/leaving server...
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix = ".",intents=intents) #sets all bot commands to be required that all commands start with a "."
load_dotenv()

main_table_name = "Discord_DB"
# main_table = create_db(main_table_name)
# admin_table = create_db("discord_admins")

main_table = DiscordTable()
main_table.create_db(main_table_name)

admin_table = DiscordTable()
admin_table.create_db("discord_admins")

@bot.event
async def on_ready():
    #on startup says (bot name) is here-means code is working
    print(f"{bot.user} is here")

    ##shows every server that the bot is on
    # for i in bot.guilds:
    #     print(i.name)
        # print(i.members)
        # print(i.id)
        # guildMembers[i.name] = {} #gets all servers bot is in and creates empty dict of that name
        
        ##list all the members in every server that the bot is in
        # for member in i.members:
            # print(member.name,member.discriminator)
            # main_table.insert_user(member.name,member.discriminator)
            # insert_user(f'{member.discriminator}',starting_balance)
            # guildMembers[i.name][member.name] = [member.name,member.discriminator] #gets all users in current server loop and creates new entry

        ##list all the channels
        # for channel in i.channels:
        #     print(f"channel: {channel} - id: {channel.id}")


    # print(guildMembers)
    auto_send.start() #function to automatically send messages to any channel using the channel id

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

@bot.command()
async def hello(ctx): # when ".hello" typed in servers bot replies to that message with "Hello World"
    print(ctx.message.content)
    print("\nmessage details:")
    print(ctx)
    print("\nmessage content:")
    print(f"{ctx.message} \n")
    my_message=ctx.message.content.lower().split(' ')
    print("message after split:")
    print(my_message)
    await ctx.reply("Hello world") #sends a reply to that message

@bot.command()
async def bye(ctx): # when ".bye" typed in servers bot replies to that message with "Goodbye"
    print("goodbye")
    await ctx.reply("Goodbye")

# @bot.command()
# async def createAdmin(ctx): # function to create any user admin privilege Ex. ".createAdmin 3977"
#     split_message = ctx.message.content.lower().split(' ')
#     for user in main_table.table.find({ "name": ctx.author.name}):
#         print(user)
#         if user["privilege"] == "admin":
#             main_table.create_admin(split_message[1])



@bot.command()
async def showDb(ctx): # returns a list of all useds in db
    await ctx.send(main_table.show_entries())

@bot.command(pass_context=True)
async def giverole(ctx, arg: discord.Member, *, role:discord.Role): # function to create any user admin privilege Ex. ".giverole @Enemy of my Enemy admin"
    for user in main_table.table.find({ "name": ctx.author.name}):
        print(user)
        if user["privilege"] == "admin":
            main_table.create_admin(arg.discriminator)
            await arg.add_roles(role) ###ERROR says bot is missing permissions



@bot.command()
async def addAll(ctx): # adds all members in all discord servers to the db
    for i in bot.guilds:
        # print(i.name)
        # print(i.members)
        # print(i.id)
        # guildMembers[i.name] = {} #gets all servers bot is in and creates empty dict of that name
        
        ##list all the members in every server that the bot is in
        for member in i.members:
            print(member.name,member.discriminator)
            main_table.insert_user(member.name,member.discriminator)


@bot.command()
async def massDestroy(ctx): # deletes all users in db
    main_table.mass_destry()


bot.run(os.getenv('discord_token'))
 

##TODO
#in createAdmin function add functionality to give admin role
