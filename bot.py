import os
import random
import datetime

import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True

allowed_mentions = discord.AllowedMentions.all()


activity = discord.Activity(
name = "my fucking life fall apart",
type = discord.ActivityType.watching)

bot = commands.Bot(command_prefix = ['epic ', 'Epic '], intents = intents, allowed_mentions = allowed_mentions)

#tic tac Toe
game_on = False


### EVENTS ###
@bot.event
async def on_ready():
    # friend_server = discord.utils.get(bot.guilds, id = 759059172414586900)
    # human_dm = await discord.utils.get(friend_server.members, id = 521702691508846593).create_dm()
    # await human_dm.send("You're not hot.")
    # me_dm = await discord.utils.get(friend_server.members, id = 335579816382300179).create_dm()
    # await me_dm.send("test test ha")

    await bot.change_presence(activity = activity)

    print(
        f'{bot.user.name} is ready.'
    )

@bot.event
async def on_connect():
    print(f'{bot.user.name} is connected to Discord.')

@bot.event
async def on_disconnect():
    print('Epic Bot has disconnected. Attempting to reconnect...')


@bot.event
async def on_message(message):
    friend_server = discord.utils.get(bot.guilds, id = 759059172414586900)
    test_server = discord.utils.get(bot.guilds, id = 848568976430596107)
    # servers = [friend_server, test_server]
    # human_dm = await discord.utils.get(friend_server.members, id = 343094362105839618).create_dm()
    me_dm = await discord.utils.get(friend_server.members, id = 335579816382300179).create_dm()
    if message.guild == friend_server or message.guild == test_server:
        camPog = discord.utils.get(message.guild.emojis, name = 'camPog')
        fiona_pog = discord.utils.get(message.guild.emojis, name = 'fiona_pog')
        sad_pog_jack = discord.utils.get(message.guild.emojis, name = 'sadpogjack')
        the_forbidden_pog = discord.utils.get(message.guild.emojis, name = 'theforbiddenpog')
        virgin_pog = discord.utils.get(message.guild.emojis, name = 'virginpog')
        wes_pog = discord.utils.get(message.guild.emojis, name = 'wesley')

        emotes = [camPog, fiona_pog, sad_pog_jack, the_forbidden_pog, virgin_pog, wes_pog]

        if 'pog' in message.content.lower():
            for emote in emotes:
                await message.add_reaction(emote)

        if 'duck' in message.content.lower():
            await message.add_reaction('🦆')

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

    #tic tac Toe
    for embed in message.embeds:
        if embed.fields[0].name == 'Your Turn':
            await message.add_reaction('1️⃣')
            await message.add_reaction('2️⃣')
            await message.add_reaction('3️⃣')
            await message.add_reaction('4️⃣')
            await message.add_reaction('5️⃣')
            await message.add_reaction('6️⃣')
            await message.add_reaction('7️⃣')
            await message.add_reaction('8️⃣')
            await message.add_reaction('9️⃣')

    # if message.channel.name == 'welcome':
    #     await message.add_reaction('☀️')
    #     await message.add_reaction('🌑')
    #     await message.add_reaction('✨')
    #     await message.add_reaction('🪐')

    await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction, member):
    me_dm = await discord.utils.get(friend_server.members, id = 335579816382300179).create_dm()
    camPog = discord.utils.get(reaction.message.guild.emojis, name = 'camPog')
    he_him = discord.utils.get(reaction.message.guild.roles, name = 'he/him')
    she_her = discord.utils.get(reaction.message.guild.roles, name = 'she/her')
    they_them = discord.utils.get(reaction.message.guild.roles, name = 'they/them')

    if reaction.emoji == camPog:
        await reaction.message.add_reaction(camPog)

    if reaction.message.channel.type == discord.ChannelType.private:
        await me_dm.send(f'{member.name} reacted to "{reaction.message.content}" with {reaction.emoji}')

    #tic tac toe
    # for embed in reaction.message.embeds:
    #     if embed.fields[0].name == 'Your Turn':
    #         if reaction.emoji == '':


    # if reaction.message.channel.name == 'welcome' and f'<@{member.id}>' in reaction.message:
    #     if reaction.emoji == '☀️':
    #         await member.add_roles(he_him)
    #     elif reaction.emoji == '🌑':
    #         await member.add_roles(she_her)
    #     elif reaction.emoji == '✨':
    #         await member.add_roles(they_them)
    #     elif reaction.emoji == '🪐':
    #         pass

# @bot.event
# async def on_reaction_remove(reaction, member):
#     he_him = discord.utils.get(reaction.message.guild.roles, name = 'he/him')
#     she_her = discord.utils.get(reaction.message.guild.roles, name = 'she/her')
#     they_them = discord.utils.get(reaction.message.guild.roles, name = 'they/them')
#
#     if member.guild.name == 'Bot Test Server':
#         if reaction.message.channel.name == 'welcome' and f'<@{member.id}>' in reaction.message:
#             if reaction.emoji == '☀️':
#                 await member.remove_roles(he_him)
#             elif reaction.emoji == '🌑':
#                 await member.remove_roles(she_her)
#             elif reaction.emoji == '✨':
#                 await member.remove_roles(they_them)
#             elif reaction.emoji == '🪐':
#                 pass

# @bot.event
# async def on_member_join(member):
#     if discord.utils.get(bot.guilds, name = 'Bot Test Server') and member.id == 410965506858942464:
#         await member.add_roles(discord.utils.get(member.guild.roles, name = 'admin'))
#
#     welcome_channel = discord.utils.get(member.guild.text_channels, name = 'welcome')
#     names_channel = discord.utils.get(member.guild.text_channels, name = 'names')
#
#     if member.guild.name == 'Bot Test Server':
#         await welcome_channel.send(
#             f"Hello, <@{member.id}>! Please put your name in <#{names_channel.id}>, and react to this message with your preferred pronouns!\nHe/Him ☀️\nShe/Her 🌑\nThey/Them ✨\nOther 🪐"
#             )

# @bot.event
# async def on_error(event):
#     print(f"")

### COMMANDS ###
@bot.command()
async def hello(ctx, times = 1):
    if times > 100:
        times = 100

    if times == 0:
        await ctx.send("‎")
    else:
        await ctx.send('hello '*times)

    with open("members_and_roles.txt", "w") as file:

        friend_server = ctx.guild

        async for member in friend_server.fetch_members():
            try:

                file.writelines(f"Member: {member.name}\n")

                file.writelines(f"Roles: ")
                for role in member.roles:
                    file.writelines(f"{role}\n")

                file.writelines(f"\n")
            except UnicodeEncodeError:
                file.writelines(f"\n\n")
                continue

@bot.command()
async def howepic(ctx, *, thing = None):
    content = ''
    if thing == None:
        thing = ctx.author.name

    embed = discord.Embed(title = f"How epic is {thing}?", color = discord.Colour.teal())

    epic_level = random.randint(0,100)

    if epic_level < 10:
        content = 'That is the unepic-est.'
    elif epic_level >= 10 and epic_level < 20:
        content = 'That is quite unepic.'
    elif epic_level >= 20 and epic_level < 35:
        content = 'That is pretty unepic.'
    elif epic_level >= 35 and epic_level < 45:
        content = 'That is kinda unepic.'
    elif epic_level >= 45 and epic_level < 55:
        content = "That's not too bad."
    elif epic_level >= 55 and epic_level < 65:
        content = 'That is kinda epic.'
    elif epic_level >= 65 and epic_level < 80:
        content = 'That is pretty epic.'
    elif epic_level >= 80 and epic_level < 90:
        content = 'That is quite epic.'
    elif epic_level >= 90:
        content = 'That is the epic-est.'

    if thing.lower() == 'cora':
        epic_level = '`OVERFLOW ERROR`'
        content = '❤️❤️😍😍❤️❤️❤️😍😍😍😍🥰❤️🥰🥰❤️❤️❤️❤️❤️'

    embed.add_field(name = 'Result:', value = f'{thing} is {epic_level}% epic.\n{content}', inline = False)

    await ctx.send(embed = embed)

@bot.command()
async def pissandshit(ctx):
    for i in range(random.randint(1,20)):
        await ctx.send("OH FUCK I'M PISSING AND SHITTING EVERYWHERE")

    dm = await ctx.member.createdm()

    await dm.send("Well you've made a mess.")

@bot.command()
async def tictactoe(ctx, *, players = 1):
    game_on = True
    game_complete = False
    game_value = ''
    turn = "Your Turn"

    game_board = [
        ['⬛','⬛','⬛'],
        ['⬛','⬛','⬛'],
        ['⬛','⬛','⬛']]

    for i,row in enumerate(game_board):
        for j,spot in enumerate(row):
            game_value += spot
            if j < 2:
                game_value += '⬜'

        if i < 2:
            game_value += '\n⬜⬜⬜⬜⬜\n'


    game = discord.Embed(title = "Tic Tac Toe!", color = discord.Colour.teal())
    game.add_field(name = turn, value = game_value)

    await ctx.send(embed = game)

@bot.command()
async def say(ctx, *, stuff):
    await ctx.send(stuff)

@bot.command(name = "8ball")
async def eight_ball(ctx, *, question):

    decision = random.randint(1,25)
    die_roll = random.randint(1,100)

    rant = "If you put me in a room with Hitler, my worst enemy, and someone who says yes to this, and you gave me 100 bullets and a gun, I would shoot the third person 99 times, then I'd shoot myself because I don't want to live on this planet knowing that people like them exist."

    answers = {
        1: "Definitely",
        2: "Probably",
        3: "I mean, I don't see why not",
        4: "Yeah",
        5: "Only a dumbass would say no to that",
        6: "Literally everybody I know thinks the answer's yes",
        7: "Of course, yes",
        8: "Obviously!",
        9: "I can't see any way that this wouldn't be true",
        10: "Normally I'd say no, but in this case, I'm gonna say yeah",
        11: "What the fuck did you just ask?",
        12: f"Someone needs to put {ctx.message.author.name} behind bars for asking this",
        13: "I'm gonna pretend you didn't just say those words",
        14: "Who cares?",
        15: "Idfk",
        16: "Hell no",
        17: "You are an idiot if you think I'm gonna say yes",
        18: "Nah",
        19: "Fuck off, that's a no",
        20: "Yeah, I can't see this being a yes in any scenario",
        21: "100% no",
        22: "I'm sorry, but that's gonna be a no from me",
        23: "Probably not",
        24: "It's not lookin' good, chief",
        25: "No, obviously not"
    }

    answer = discord.Embed(title = "Epic 8 Ball", color = discord.Colour.teal())

    if die_roll == 1:
        answer.add_field(name = f"{ctx.message.author.name} asks: {question}", value = rant)
    else:
        answer.add_field(name = f"{ctx.message.author.name} asks: {question}", value = answers[decision])

    await ctx.send(embed = answer)






# @bot.command()
# async def destroy(ctx, user, *, reason = None):
#     user = discord.utils.get(ctx.guild.members, name = user)
#     await user.ban()
#     await ctx.send("boom.")

bot.run(TOKEN)
