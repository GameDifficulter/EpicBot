import discord
import random

from discord.ext import commands

class SillyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        camPog = self.bot.get_emoji(797130209848852500)
        fiona_pog = self.bot.get_emoji(789468149765373992)
        the_forbidden_pog = self.bot.get_emoji(759067762735186020)
        virgin_pog = self.bot.get_emoji(808523933308813323)
        wes_pog = self.bot.get_emoji(785891522620424233)
        cat = self.bot.get_emoji(802335831464345650)

        emotes = [camPog, fiona_pog, the_forbidden_pog, virgin_pog, wes_pog, cat]

        if 'pog' in message.content.lower():
            for emote in emotes:
                await message.add_reaction(emote)

        if 'duck' in message.content.lower():
            await message.add_reaction('🦆')


    @commands.command(name = "8ball", description = "Epic Bot will provide a yes or no answer to your deepest questions. Use the format \"epic 8ball [question]\"")
    async def eight_ball(self, ctx, *, question):

        decision = random.randint(1,25)
        die_roll = random.randint(1,100)
        gun_roll = random.randint(1,1000)

        gun = "I have a gun in my mouth."
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
        elif gun_roll == 1:
            answer.add_field(name = f"{ctx.message.author.name} asks: {question}", value = gun)
        else:
            answer.add_field(name = f"{ctx.message.author.name} asks: {question}", value = answers[decision])

        await ctx.send(embed = answer)

    @commands.command(name = "hello", description = "Epic Bot says hello! Add a number to increase the number of times he says it (caps at 100).")
    async def hello(self, ctx, times = 1):
        if times > 100:
            times = 100

        if times == 0:
            await ctx.send("‎")
        else:
            await ctx.send('hello '*times)

    @commands.command(name = "howepic", description = "Measures the epicness of the user who invoked this command. To find the epicness of anything else, use \"epic howepic [thing].\"")
    async def howepic(self, ctx, *, thing = None):
        content = ''
        if thing == None:
            thing = f"<@!{ctx.author.id}>"

        title_thing = thing

        try:
            member = await ctx.guild.fetch_member(thing[thing.find("<@!") + 3:thing.find(">")])
            if member != None:
                title_thing = member.name
        except:
            pass

        embed = discord.Embed(title = f"How epic is {title_thing}?", color = discord.Colour.teal())

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
            if epic_level == 69:
                content = "Nice"
            else:
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

    @commands.command(name = "pissandshit", description = "Sends the message \"OH FUCK I'M PISSING AND SHITTING EVERYWHERE\" a random number of times (up to 20).")
    async def pissandshit(self, ctx):
        for i in range(random.randint(1,20)):
            await ctx.send("OH FUCK I'M PISSING AND SHITTING EVERYWHERE")

        dm = await ctx.author.create_dm()

        await dm.send("Well you've made a mess.")

    @commands.command(name = "say", description = "Epic Bot will say exactly what you type. Use the format \"epic say [thing]\"")
    async def say(self, ctx, *, stuff):
        await ctx.send(stuff)


    @commands.command(name = "test", description = "Test")
    async def test(self, ctx):
        await ctx.send("haha yes I am alive")

async def setup(bot):
    await bot.add_cog(SillyCommands(bot))
