import discord

from discord.ext import commands

class VoiceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'join', description = "Joins the voice channel of the person who invoked the command.")
    async def join(self, ctx):
        user_voice = ctx.author.voice.channel
        await user_voice.connect(timeout = 1.0, reconnect = True)
        for x in self.bot.voice_clients:
            if x.guild == ctx.guild:
                await x.connect(reconnect = True, timeout = 60.0)
                await x.guild.change_voice_state(user_voice)

        await ctx.send("Joining " + user_voice.name)

    @commands.command(name = 'fuckoff', description = 'Leaves the voice channel.')
    async def fuckoff(self, ctx):
        for v in self.bot.voice_clients:
            if v.guild == ctx.guild:
                await ctx.send("Fucking off from " + ctx.author.voice.channel.name)
                await v.disconnect(force = True)

    @commands.command(name = 'bruh', description = 'He says bruh.')
    async def bruh(self, ctx):
        bruhh = open('bruh.wav','rb',buffering=0)
        for v in self.bot.voice_clients:
            if v.guild == ctx.guild:
                v.play(discord.PCMAudio(bruhh))

async def setup(bot):
    await bot.add_cog(VoiceCommands(bot))
