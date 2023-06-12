import discord
from discord.ext import commands

class NormalCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'help', description = 'Sends a help message.')
    async def help(self,ctx):
        cop = [cmd for cmd in self.bot.commands]
        names = [cmd.name for cmd in cop]
        names.sort()

        in_order = []
        for n in names:
            for cmd in cop:
                if n == cmd.name:
                    in_order.append(cmd)
                    break
        
        com = discord.Embed(title = "Epic Help", color = discord.Colour.teal())

        for thing in in_order:
            print(thing.name, thing.description)
            desc = thing.description

            if thing.description == '':
                desc = "None"

            if desc != "None":
                com.add_field(name = thing.name, value = desc)
            # if thing.name == 'test':
            #     com.add_field(name = thing.name, value = thing.description)

        await ctx.send(embed = com)

async def setup(bot):
    await bot.add_cog(NormalCommands(bot))