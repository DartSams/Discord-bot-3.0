import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv
from datetime import timedelta
import os
import random
import json
import Google_Calendar_API.calendar_test
from MyDB import DiscordTable
import Spotify_API
import Google_Calendar_API
from linkedin import transform, extract
##docs##
#https://discordpy.readthedocs.io/en/latest/api.html
#dev portal (make a bot)

##needs intents to check member status's like when joining/leaving server...
intents = discord.Intents.all()  
intents.members = True
bot = commands.Bot(command_prefix = ".",intents=intents) #sets all bot commands to be required that all commands start with a "."
load_dotenv()

main_table_name = "Discord_DB"
main_table = DiscordTable()
main_table.create_db(main_table_name)

high_level_roles = ["admin"] # list of top level role names to give admin status
channel_ids = {
    "test-server":{},
    "GameDevelopmentServer":{
        "Information": 989899212856623186,
        "welcome-and-rules": 989899212856623187,
        "notes-resources": 989899212856623188,
        "Text Channels": 989899212856623189,
        "general": 989899213422878730,
        "homework-help": 989899213422878731,
        "session-planning": 989899213422878732,
        "off-topic": 989899213422878733,
        "Voice Channels": 989899213422878734,
        "Study Room": 989899213422878735,
        "Study Room 1": 989899213422878736,
        "Voice Chat": 992072925295423619,
        "saturday-of-the-weebs": 1012697333026258974,
        "concept": 1047893711771676702,
        "pixel": 1047899028211384380,
        "3d-drawings": 1047892668719579169,
        "voice-acting": 1050531521729142794,
        "useful-links": 1159294922906677388,
        "levels": 1047897871267139586,
        "interview-questions": 1161018171390701698,
        "memes": 1116809911544844329,
        "paid-studies": 1148441761501413486,
        "Sound design": 1050531461066928158,
        "workshops": 1162096768637485117,
        "Academic Opportunities": 1162068212863733850,
        "idea-generator": 1047892787892322304,
        "postings": 1111115259596517426,
        "leadership-progams": 1148440480233832469,
        "interships": 1125962955595464804,
        "fellowships": 1136003263603425361,
        "externships": 1162064390690971689,
        "background-art": 1047893634063810570,
        "full-time": 1148439830498390036,
        "the rooftop": 1047890947150716928,
        "notifications": 1047911263520440400,
        "Admin Playground": 1047891194157477989,
        "Spitballing": 1047892506127372288,
        "scholarships": 1127703669731762287,
        "test-commands": 1047893027554873395,
        "moderate": 1047892984890392627,
        "tiles": 1047897829584142466,
        "music": 1050531492343840848,
        "Job Postings": 1111114688424583249,
        "Art Showcase": 1047891469316411443,
        "organizations": 1162075922531369061,
        "inspiration": 1053367634420314123,
        "general": 1047890947150716930,
        "friday nights": 1047899859119771809,
        "2d-drawings": 1047892607210106930,
        "Interview Prep": 1162069571960848435,
        "birthday": 1166655376809275422,
        "confess-sins": 1115051583705731162,
        "animation": 1047902387223937114,
        "Friday nights": 1047901188928045076
    }
}

@bot.event
async def on_ready():
    #on startup says (bot name) is here-means code is working
    print(f"{bot.user} is here")

    ##shows every server that the bot is on
    for i in bot.guilds:
    #     print(i.name)
    #     print(i.members)
    #     print(i.id)
        # guildMembers[i.name] = {} #gets all servers bot is in and creates empty dict of that name
        
        ##list all the members in every server that the bot is in
        # for member in i.members:
            # print(member.name,member.discriminator)
            # main_table.insert_user(member.name,member.discriminator)
            # insert_user(f'{member.discriminator}',starting_balance)
            # guildMembers[i.name][member.name] = [member.name,member.discriminator] #gets all users in current server loop and creates new entry

        ##list all the channels
        for channel in i.channels:
            print(f"channel: {channel} - id: {channel.id}") #on start will print every channel and its channel id that the discord is in



    # print(guildMembers)
    auto_send.start() #function to automatically send messages to any channel using the channel id


@tasks.loop(hours=1.0)
async def auto_send():
    """
    Old test server
    channel: Text Channels - id: 795114714560069692
    channel: Voice Channels - id: 795114714560069693
    channel: the-rooftop - id: 795114714560069694
    channel: General - id: 795114714560069695
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
    # channel_ids = {
    #     "the-rooftop":"795114714560069694",
    # }
    
    # channel = await bot.fetch_channel(channel_ids["GameDevelopmentServer"]["the-rooftop"])
    # await channel.send('GOOD MORNING!')

    """
    Game Development Server
    GameDevs
    <discord.utils.SequenceProxy object at 0x000001AAC3777820>
    1047890946110521354
    """
    channel = await bot.fetch_channel(str(channel_ids["GameDevelopmentServer"]["memes"]))
    # await channel.send(
    #     
    # )
    jobs = [
        "Computer Science", "IT", "Software Engineer", "Software Developer",
        "Game Programmer", "Game Developer", "Fellowship", "Cybersecurity"
    ]
    for i in transform(extract(random.choice(jobs))):
        channel = await bot.fetch_channel(str(channel_ids["GameDevelopmentServer"]["postings"]))
        #await channel.send(i["link"])

    gc = Google_Calendar_API.calendar_test
    gc_events = gc.show_upcoming_events()
    
    channel = await bot.fetch_channel(channel_ids["GameDevelopmentServer"]["birthday"])
    for i in gc_events:
        await channel.send(i)

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
    await ctx.reply("Konicha Wassupp") #sends a reply to that message

@bot.command()
async def newmessage(ctx):
    print(ctx.message.content)
    my_message=ctx.message.content.lower().split('->')
    print(my_message)
    # await ctx.send(my_message[1])
    #channel = await bot.fetch_channel(channel_ids["GameDevelopmentServer"][my_message[1]]) #send a message to the channel the user wants (.newmessage -> {channel name}->web developer) Ex. .newmessage -> postings->web developer
    channel = await bot.fetch_channel(str(channel_ids["GameDevelopmentServer"][my_message[1]]))
    
    await channel.send(my_message[2]) #makes the bot send the message that is withing the 3 index of the message send (.newmessage -> {channel name}->{message})
    
@bot.command()
async def scrape(ctx):
    my_message=ctx.message.content.lower().split('->')
    # posting = my_message[1].split("-")
    print(ctx.guild)
    print(my_message)
    # await ctx.send(my_message[1])
    channel = await bot.fetch_channel(channel_ids["GameDevelopmentServer"][my_message[1]]) #send a message to the channel the user wants (.scrape -> {channel name}->web developer) Ex. .scrape -> postings->web developer
    # await channel.send(my_message[2])
    if len(my_message) == 3: #searches only job type
        for i in transform(extract(my_message[2])): #calls bs4 functions in file to return a list of job objects
            channel = await bot.fetch_channel(str(channel_ids["GameDevelopmentServer"]["postings"]))
            await channel.send(i["link"]) 
    elif len(my_message) == 4: #searches job type and location
        for i in transform(extract(my_message[2],my_message[3])): #calls bs4 functions in file to return a list of job objects
            channel = await bot.fetch_channel(str(channel_ids["GameDevelopmentServer"]["postings"]))
            await channel.send(i["link"]) 
    elif len(my_message) == 5: #searches job type and location
        for i in transform(extract(my_message[2],my_message[3],my_message[4])): #calls bs4 functions in file to return a list of job objects
            channel = await bot.fetch_channel(str(channel_ids["GameDevelopmentServer"]["postings"]))
            await channel.send(i["link"]) 

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
async def takerole(ctx, arg: discord.Member, *, role:discord.Role): # function to create any user admin privilege Ex. ".takerole @Enemy of my Enemy admin"
    for user in main_table.table.find({ "name": ctx.author.name}): #finds message sender in mongodb
        print(user)
        if user["privilege"] == "admin" and ctx.message.author.guild_permissions.administrator: #checks if user has privilege of admin
            main_table.create_admin(arg.discriminator) # function to update privilege in mongodb
            await arg.remove_roles(role) # removes role to discord user mentioned in message sent (by mentioned name after @ symbol)
            await ctx.send(f"{ctx.author} is no longer a {role}")

@bot.command(pass_context=True)
async def createrole(ctx,name:str,color_message:str): # creates a new role Ex. .createrole creator red
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
async def addAll(ctx): # adds all members in all discord servers to the db (Ex. .addAll)
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
        if ctx.message.author.guild_permissions.administrator: #checks if user has privilege of admin in mongodb and checks in discord roles
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
async def sp(ctx): #function to query spotify artist and/or album Ex. .sp -kota the friend- -> return spotify artist #Ex. .sp -kota the friend- everything
    message = ctx.message.content.split('-')
    spotify_artist = message[1]
    album_name = message[2].replace(" ","")
    # print(message)
    print(spotify_artist,album_name)
    s = Spotify_API.Spotify()
    # print(s.get_artist_album(spotify_artist,album_name))
    artist = s.search(spotify_artist)
    # # print(spotify_data)

    if album_name:
        # artist = s.search(spotify_artist)
        data = {}
        for i in s.album_list:
            # print(i["name"])
            if album_name.lower() == i["name"].lower():
                # print(i["id"])
                album = s.get_album(i["id"])
                data["artist"] = artist
                data["album"] = album
                # await ctx.send(data)
                await ctx.send(data["artist"]["pic"])
                await ctx.send(data["artist"]["name"])
                await ctx.send(data["album"]["album_url"])
            
            elif album_name.lower() == "albums":
                all_albums = s.get_all_albums()
                await ctx.send(all_albums)
    # await ctx.send(s.search(spotify_artist))
    else:
        await ctx.send(artist["pic"])
        await ctx.send(artist["name"])


@bot.command()
async def helpList(ctx):
    help_text = """
        Below are the commands I am capable of...

        # (Ex. .hello) typed in servers bot replies to that message with "Hello World"
        # (Ex. .newmessage ->{channel name}->{message}) makes the bot send the message that is withing the 3 index of the message send 
        # (Ex. .scrape ->postings->web developer) send a message to the channel the user wants (.scrape -> {channel name}->web developer) 
        # (Ex. .bye) typed in servers bot replies to that message with "Goodbye"
        # (Ex. .showdb) returns a list of all useds in db 
        # (Ex. .giverole @Enemy of my Enemy admin) gives any user privilege 
        # (Ex. .takerole @Enemy of my Enemy admin) remove any user privilege 
        # (Ex. .createrole creator red) creates a new role with a color
        # (Ex. .addAll) adds all members in all discord servers to the db 
        # (Ex. .massDestroy) deletes all users in db 
        # (Ex. .ban @Enemy of my Enemy was being rude) kicks someone from server and bans them so they can rejoin 
        # (Ex. .unban @Enemy of my Enemy has earned a free pass) unbans someone from server 
        # (Ex. .kick @Enemy of my Enemy was being rude) kick  s server member from server that message was sent in 
        # (Ex. .mute @Enemy of my Enemy 2 min) timeouts server members (member cant type/text in any channel in server for amount of time) 
        # (Ex. .sp -kota the friend- everything) function to query spotify artist and/or album (Ex. .sp -kota the friend)- -> return spotify artist 
    """

    await ctx.send(help_text)

# bot.run(os.environ.get('discord_token'))
my_secret = "MTAzOTc0NzQzMjc2Mzg5MTc1Mg.GvJjcm.tWc9Ns_7rqzVKcps2SN_5THzkNPFVVyYgENiIM"
bot.run(my_secret)
