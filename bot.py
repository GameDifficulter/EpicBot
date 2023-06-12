import os
import random
import datetime

import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.members = True
intents.messages = True

allowed_mentions = discord.AllowedMentions.all()


activity = discord.Activity(
application_id = 945360,
type = discord.ActivityType.playing)

bot = commands.Bot(activity = activity, command_prefix = ['epic ', 'Epic '], help_command = None,intents = intents, allowed_mentions = allowed_mentions)


### EVENTS ###
@bot.event
async def on_ready():
    # friend_server = discord.utils.get(bot.guilds, id = 759059172414586900)
    # human_dm = await discord.utils.get(friend_server.members, id = 521702691508846593).create_dm()
    # await human_dm.send("You're not hot.")
    # me_dm = await discord.utils.get(friend_server.members, id = 335579816382300179).create_dm()
    # await me_dm.send("test test ha")

    # await bot.change_presence(activity = activity)

    print(
        f'{bot.user.name} is ready.'
    )

@bot.event
async def on_connect():
    # await bot.load_extension("tictactoe")
    await bot.load_extension("normal_commands")
    await bot.load_extension("silly_commands")
    await bot.load_extension("voice_commands")
    await bot.load_extension("owner")

    print(f'{bot.user.name} is connected to Discord.')\

@bot.event
async def on_disconnect():
    print(f'{bot.user.name} has disconnected. Attempting to reconnect...')


@bot.event
async def on_message(message):
    friend_server = discord.utils.get(bot.guilds, id = 759059172414586900)
    friend_voice = discord.utils.get(friend_server.voice_channels, id = 786982807880335364)
    test_server = discord.utils.get(bot.guilds, id = 848568976430596107)
    voice = discord.utils.get(test_server.voice_channels, id = 848568976430596111)
    connected = None
    friend_connected = None
    # servers = [friend_server, test_server]
    # human_dm = await discord.utils.get(friend_server.members, id = 343094362105839618).create_dm()

    me_dm = await discord.utils.get(friend_server.members, id = 335579816382300179).create_dm()

    # if message.guild == friend_server or message.guild == test_server:
    #     camPog = bot.get_emoji(797130209848852500)
    #     fiona_pog = bot.get_emoji(789468149765373992)
    #     the_forbidden_pog = bot.get_emoji(759067762735186020)
    #     virgin_pog = bot.get_emoji(808523933308813323)
    #     wes_pog = bot.get_emoji(785891522620424233)
    #     cat = bot.get_emoji(802335831464345650)
    #
    #     emotes = [camPog, fiona_pog, the_forbidden_pog, virgin_pog, wes_pog, cat]
    #
    #     if 'pog' in message.content.lower():
    #         for emote in emotes:
    #             await message.add_reaction(emote)
    #
    #     if 'duck' in message.content.lower():
    #         await message.add_reaction('🦆')

    if message.content == 'CALL THE BOT':
        await message.channel.send('d!wotd')

    if message.channel.type == discord.ChannelType.private and message.author != bot.user and message.channel != me_dm:
        await me_dm.send(f'Message from {message.author.name}:\n{message.content}')
        for image in message.attachments:
            await me_dm.send(image.url)
        await message.add_reaction('✅')

    if message.channel == me_dm and message.author != bot.user:
        first_bracket = message.content.find('<')
        second_bracket = message.content.find('>')
        user_id = message.content[first_bracket + 1:second_bracket]
        bot_channel = discord.utils.get(friend_server.channels, id = 776148490093854741)
        gen_chat = discord.utils.get(friend_server.channels, id = 759059172863246408)

        if user_id == 'bot chat':
            human_dm = bot_channel
        elif user_id == 'general':
            human_dm = gen_chat
        else:
            human_dm = await discord.utils.get(friend_server.members, id = int(user_id)).create_dm()

        await human_dm.send(message.content[second_bracket + 1:])

    if message.channel.id == 776148490093854741 and message.author != bot.user:
        await me_dm.send(f"Message from {message.author.name} in bot chat:\n{message.content}")

    await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction, member):
    friend_server = discord.utils.get(bot.guilds, id = 759059172414586900)
    if reaction.message.guild == discord.utils.get(bot.guilds, id = 759059172414586900):

        me_dm = await discord.utils.get(friend_server.members, id = 335579816382300179).create_dm()
        camPog = bot.get_emoji(797130209848852500)
        # he_him = discord.utils.get(reaction.message.guild.roles, name = 'he/him')
        # she_her = discord.utils.get(reaction.message.guild.roles, name = 'she/her')
        # they_them = discord.utils.get(reaction.message.guild.roles, name = 'they/them')

        if reaction.emoji == camPog:
            await reaction.message.add_reaction(camPog)

    if reaction.message.channel.type == discord.ChannelType.private:
        await me_dm.send(f'{member.name} reacted to "{reaction.message.content}" with {reaction.emoji}')


### COMMANDS ###
# @bot.command()
# async def hello(ctx, times = 1):
#     if times > 100:
#         times = 100
#
#     if times == 0:
#         await ctx.send("‎")
#     else:
#         await ctx.send('hello '*times)
#
#     with open("members_and_roles.txt", "w") as file:
#
#         friend_server = ctx.guild
#
#         async for member in friend_server.fetch_members():
#             try:
#
#                 file.writelines(f"Member: {member.name}\n")
#
#                 file.writelines(f"Roles: ")
#                 for role in member.roles:
#                     file.writelines(f"{role}\n")
#
#                 file.writelines(f"\n")
#             except UnicodeEncodeError:
#                 file.writelines(f"\n\n")
#                 continue
#
# @bot.command()
# async def howepic(ctx, *, thing = None):
#     content = ''
#     if thing == None:
#         thing = ctx.author.name
#
#     embed = discord.Embed(title = f"How epic is {thing}?", color = discord.Colour.teal())
#
#     epic_level = random.randint(0,100)
#
#     if epic_level < 10:
#         content = 'That is the unepic-est.'
#     elif epic_level >= 10 and epic_level < 20:
#         content = 'That is quite unepic.'
#     elif epic_level >= 20 and epic_level < 35:
#         content = 'That is pretty unepic.'
#     elif epic_level >= 35 and epic_level < 45:
#         content = 'That is kinda unepic.'
#     elif epic_level >= 45 and epic_level < 55:
#         content = "That's not too bad."
#     elif epic_level >= 55 and epic_level < 65:
#         content = 'That is kinda epic.'
#     elif epic_level >= 65 and epic_level < 80:
#         content = 'That is pretty epic.'
#     elif epic_level >= 80 and epic_level < 90:
#         content = 'That is quite epic.'
#     elif epic_level >= 90:
#         content = 'That is the epic-est.'
#
#     if thing.lower() == 'cora':
#         epic_level = '`OVERFLOW ERROR`'
#         content = '❤️❤️😍😍❤️❤️❤️😍😍😍😍🥰❤️🥰🥰❤️❤️❤️❤️❤️'
#
#     embed.add_field(name = 'Result:', value = f'{thing} is {epic_level}% epic.\n{content}', inline = False)
#
#     await ctx.send(embed = embed)
#
# @bot.command()
# async def pissandshit(ctx):
#     for i in range(random.randint(1,20)):
#         await ctx.send("OH FUCK I'M PISSING AND SHITTING EVERYWHERE")
#
#     dm = await ctx.member.createdm()
#
#     await dm.send("Well you've made a mess.")
#
# @bot.command()
# async def say(ctx, *, stuff):
#     await ctx.send(stuff)
#
# @bot.command(name = "8ball")
# async def eight_ball(ctx, *, question):
#
#     decision = random.randint(1,25)
#     die_roll = random.randint(1,100)
#     gun_roll = random.randint(1,1000)
#
#     gun = "I have a gun in my mouth."
#     rant = "If you put me in a room with Hitler, my worst enemy, and someone who says yes to this, and you gave me 100 bullets and a gun, I would shoot the third person 99 times, then I'd shoot myself because I don't want to live on this planet knowing that people like them exist."
#
#     answers = {
#         1: "Definitely",
#         2: "Probably",
#         3: "I mean, I don't see why not",
#         4: "Yeah",
#         5: "Only a dumbass would say no to that",
#         6: "Literally everybody I know thinks the answer's yes",
#         7: "Of course, yes",
#         8: "Obviously!",
#         9: "I can't see any way that this wouldn't be true",
#         10: "Normally I'd say no, but in this case, I'm gonna say yeah",
#         11: "What the fuck did you just ask?",
#         12: f"Someone needs to put {ctx.message.author.name} behind bars for asking this",
#         13: "I'm gonna pretend you didn't just say those words",
#         14: "Who cares?",
#         15: "Idfk",
#         16: "Hell no",
#         17: "You are an idiot if you think I'm gonna say yes",
#         18: "Nah",
#         19: "Fuck off, that's a no",
#         20: "Yeah, I can't see this being a yes in any scenario",
#         21: "100% no",
#         22: "I'm sorry, but that's gonna be a no from me",
#         23: "Probably not",
#         24: "It's not lookin' good, chief",
#         25: "No, obviously not"
#     }
#
#     answer = discord.Embed(title = "Epic 8 Ball", color = discord.Colour.teal())
#
#     if die_roll == 1:
#         answer.add_field(name = f"{ctx.message.author.name} asks: {question}", value = rant)
#     elif gun_roll == 1:
#         answer.add_field(name = f"{ctx.message.author.name} asks: {question}", value = gun)
#     else:
#         answer.add_field(name = f"{ctx.message.author.name} asks: {question}", value = answers[decision])
#
#     await ctx.send(embed = answer)

# @bot.command()
# async def join(ctx):
#     user_voice = ctx.author.voice.channel
#     await user_voice.connect(timeout = 1.0, reconnect = True)
#     for x in bot.voice_clients:
#         if x.guild == ctx.guild:
#             await x.connect(reconnect = True, timeout = 60.0)
#             await x.guild.change_voice_state(user_voice)
#
#     await ctx.send("Joining " + user_voice.name)
#
# @bot.command()
# async def fuckoff(ctx):
#     for v in bot.voice_clients:
#         if v.guild == ctx.guild:
#             await ctx.send("Fucking off from " + ctx.author.voice.channel.name)
#             await v.disconnect(force = True)
#
# @bot.command()
# async def bruh(ctx):
#     bruhh = open('bruh.wav','rb',buffering=0)
#     for v in bot.voice_clients:
#         if v.guild == ctx.guild:
#             v.play(discord.PCMAudio(bruhh))


# @bot.command()
# async def test(ctx):
#     await ctx.send("haha yes I am alive")

@bot.command()
async def reload(ctx, module):
    if ctx.author.id == 335579816382300179:
        try:
            await bot.reload_extension(module)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('❎')
            
    else:
        await ctx.message.add_reaction('❎')



# @bot.command()
# async def destroy(ctx, user, *, reason = None):
#     user = discord.utils.get(ctx.guild.members, name = user)
#     await user.ban()
#     await ctx.send("boom.")

bot.run(TOKEN)
