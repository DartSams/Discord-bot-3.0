import discord
from discord.ext import tasks,commands
from dotenv import load_dotenv
from datetime import timedelta
import os
import random
import json
from MyDB import *


##docs##
#https://discordpy.readthedocs.io/en/latest/api.html
#dev portal (make a bot)

##needs intents to check member status's like when joining/leaving server...
intents = discord.Intents.all()  
intents.members = True
bot = commands.Bot(command_prefix = "/",intents=intents) #sets all bot commands to be required that all commands start with a "."
load_dotenv()

main_table_name = "Discord_DB"
main_table = DiscordTable()
main_table.create_db(main_table_name)

high_level_roles = ["admin"] # list of top level role names to give admin status


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

@bot.command() # decorator basically called when discord message starts with command_prefix 
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
    await ctx.reply("https://i.scdn.co/image/ab6761610000e5eb72c4ca30476ce87954961a10")

@bot.command()
async def bye(ctx): # when ".bye" typed in servers bot replies to that message with "Goodbye"
    print("goodbye")
    await ctx.reply("Goodbye")


@bot.command()
async def showDb(ctx): # returns a list of all useds in db
    await ctx.send(main_table.show_entries())

@bot.command(pass_context=True)
async def giverole(ctx, arg: discord.Member, *, role:discord.Role): # function to create any user admin privilege Ex. ".giverole @Enemy of my Enemy admin"
    for user in main_table.table.find({ "name": ctx.author.name}): #finds message sender in mongodb
        print(user)
        if user["privilege"] == "admin" and ctx.message.author.guild_permissions.administrator: #checks if user has privilege of admin
            main_table.create_admin(arg.discriminator) # function to update privilege in mongodb
            await arg.add_roles(role) # gives role to discord user mentioned in message sent (by mentioned name after @ symbol)
            await ctx.send(f"{ctx.author} is now a {role}")

@bot.command(pass_context=True)
async def takerole(ctx, arg: discord.Member, *, role:discord.Role): # function to create any user admin privilege Ex. ".giverole @Enemy of my Enemy admin"
    for user in main_table.table.find({ "name": ctx.author.name}): #finds message sender in mongodb
        print(user)
        if user["privilege"] == "admin" and ctx.message.author.guild_permissions.administrator: #checks if user has privilege of admin
            main_table.create_admin(arg.discriminator) # function to update privilege in mongodb
            await arg.remove_roles(role) # gives role to discord user mentioned in message sent (by mentioned name after @ symbol)
            await ctx.send(f"{ctx.author} is no longer a {role}")

@bot.command(pass_context=True)
async def createrole(ctx,name:str,color_message:str): # creates a new role Ex. .createrole creator
    for user in main_table.table.find({ "name": ctx.author.name}): #finds message sender in mongodb
        # print(user)
        if user["privilege"] == "admin" and ctx.message.author.guild_permissions.administrator: #checks if user has privilege of admin
            # print(ctx.message.content)
            with open("colors.json","r") as c: # opens the hex color json file
                data_file_color = json.load(c)
                for color in data_file_color:
                    # print(i["name"])
                    if color["name"].lower() == color_message: # when iterating through hex data in json file checks if current iteration has name equal to what was sent in the message
                        # print(color["hex"])
                        color_hex = color["hex"]
                        discord_hex_color_value = discord.Colour.from_str(color_hex).value # calls discord Colour function that takes a str of hex or hsv value that returns the associated color value
                        with open("permission.json","r") as p:
                            data_file_permission = json.load(p)
                            for permission in data_file_permission:
                                if permission["name"].lower() == name: #when iterating through permission data 
                                    if name in high_level_roles:
                                        permission_value = permission["value"] # set the permission value to be a integer which is a combined number based on discords own algorithm
                                    else:
                                        permission_value = 0 # set the default to 0 for all roles if not found in permission.json file

                                    permission_value = discord.Permissions(permissions=permission_value) # calls discord Permission function that takes a integer value that represents the value of privileges to give to a role found on discord dev portal under bot section
                                    await ctx.guild.create_role(name=name,colour=discord_hex_color_value,permissions=permission_value) #creates a role in discord server where message was sent
                                    await ctx.send(f"{name} has been created")

        else: #if message sender isnt a admin in the mongodb
            await ctx.send("Your not a admin cant give roles contact a admin")

@bot.command()
async def addAll(ctx): # adds all members in all discord servers to the db
    for i in bot.guilds:
        # print(i.name) #return iterated server names
        # print(i.members) #returns list of all members in iterated server
        # print(i.id) # returns iterated id of server
        # guildMembers[i.name] = {} #gets all servers bot is in and creates empty dict of that name
        
        ##list all the members in every server that the bot is in
        for member in i.members:
            print(member.name,member.discriminator)
            main_table.insert_user(member.name,member.discriminator)


@bot.command()
async def massDestroy(ctx): # deletes all users in db
    main_table.mass_destry()


@bot.command()
async def ban(ctx,member:discord.Member,reason=None): # kicks someone from server and bans them so they can rejoin Ex. .ban @Enemy of my Enemy was being rude
    for user in main_table.table.find({ "name": ctx.author.name}): #finds message sender in mongodb
        # print(user)
        if user["privilege"] == "admin" and ctx.message.author.guild_permissions.administrator: #checks if user has privilege of admin in mongodb and checks in discord roles
            print(ctx.message.content)
            print(member,reason)
            await member.ban()
            await ctx.reply(f"{member} has now been banned")

        else: # if message author isnt a admin
            print("User is not admin")
            await ctx.reply(f"{ctx.author.name} is not a admin")

@bot.command()
async def unban(ctx,member:discord.Member,reason=None): # unbans someone from server Ex. .unban @Enemy of my Enemy has earned a free pass
    for user in main_table.table.find({ "name": ctx.author.name}): #finds message sender in mongodb
        # print(user)
        if user["privilege"] == "admin" and ctx.message.author.guild_permissions.administrator: #checks if user has privilege of admin in mongodb and checks in discord roles
            print(ctx.message.content)
            print(member,reason)
            await member.unban()
            await ctx.reply(f"{member} has now been unbanned")

        else: # if message author isnt a admin
            print("User is not admin")
            await ctx.reply(f"{ctx.author.name} is not a admin")

@bot.command()
async def kick(ctx,member:discord.Member,reason=None): # kicks server member from server that message was sent in Ex. .kick @Enemy of my Enemy was being rude
    for user in main_table.table.find({ "name": ctx.author.name}): #finds message sender in mongodb
        # print(user)
        if user["privilege"] == "admin" and ctx.message.author.guild_permissions.administrator: #checks if user has privilege of admin in mongodb and checks in discord roles
            print(ctx.message.content)
            print(member,reason)
            await member.kick()
            await ctx.reply(f"{member} has now been kicked")

        else: # if message author isnt a admin
            print("User is not admin")
            await ctx.reply(f"{ctx.author.name} is not a admin")

@bot.command()
async def mute(ctx,member:discord.Member, time: int, how_long:str): # function that timeouts server members (member cant type/text in any channel in server for amount of time) Ex. .mute @Enemy of my Enemy 2 min
    print(member,time,how_long)
    for user in main_table.table.find({ "name": ctx.author.name}): #finds message sender in mongodb
        # print(user)
        if user["privilege"] == "admin" and ctx.message.author.guild_permissions.administrator: #checks if user has privilege of admin in mongodb and checks in discord roles
            print(ctx.message.content)
            print(member)
            if how_long == "day" or how_long == "days":
                member_timeout = timedelta(days=time) #timedelta returns the difference of current time and the amount passed
            elif how_long == "hour" or how_long == "hours":
                member_timeout = timedelta(hours=time) #timedelta returns the difference of current time and the amount passed
            elif how_long == "min" or how_long == "minuts":
                member_timeout = timedelta(minutes=time) #timedelta returns the difference of current time and the amount passed
            else:
                await ctx.send("Please enter a valid time in days,hours,minutes")

            await member.timeout(member_timeout)
            await ctx.reply(f"{member} has now been muted for {time} {how_long}")

        else: # if message author isnt a admin
            print("User is not admin")
            await ctx.reply(f"{ctx.author.name} is not a admin")



@bot.command()
async def sp(ctx,spotify_artist:str):
    pass


bot.run(os.getenv('discord_token'))