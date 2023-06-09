import discord

from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def insert_lines(self, ctx, file, line, *, code):
        me = await self.bot.fetch_user(335579816382300179)
        me_dm = await me.create_dm()

        if ctx.author.id == 335579816382300179:
            code = code[3:len(code) - 3] + "\n"
            lines = []

            with open(file, 'r') as f:
                lines = f.readlines()

            with open (file, "w") as f:
                lines.insert(int(line) - 1, code)
                f.write("".join(lines))

            await me_dm.send(file = discord.File(open(file, 'rb')))


            await ctx.send(f"Line {line} in {file} was inserted with the following code:\n```{code}```")

    @commands.command()
    async def edit_lines(self, ctx, file, line, end_line, *, code):
        me = await self.bot.fetch_user(335579816382300179)
        me_dm = await me.create_dm()

        if ctx.author.id == 335579816382300179:
            code = code[3:len(code) - 3] + "\n"
            lines = []
            line = int(line)
            end_line = int(end_line)

            with open(file, 'r') as f:
                lines = f.readlines()

            with open (file, 'w') as f:
                for i in range(end_line - line + 1):
                    lines.pop(line - 1)

                lines.insert(line - 1, code)
                f.write("".join(lines))

            await me_dm.send(file = discord.File(open(file, 'rb')))

            await ctx.send(f"Lines {line} through {end_line} in {file} were replaced with the following code:\n```{code}```")

    @commands.command()
    async def delete_lines(self, ctx, file, line, end_line):
        me = await self.bot.fetch_user(335579816382300179)
        me_dm = await me.create_dm()

        if ctx.author.id == 335579816382300179:
            lines = []
            line = int(line)
            end_line = int(end_line)

            with open(file, 'r') as f:
                lines = f.readlines()

            with open (file, 'w') as f:
                for i in range(end_line - line + 1):
                    lines.pop(line - 1)

                f.write("".join(lines))

            await me_dm.send(file = discord.File(open(file, 'rb')))

            await ctx.send(f"Lines {line} through {end_line} in {file} were deleted.")

    @commands.command()
    async def send_file(self, ctx, file):
        me = await self.bot.fetch_user(335579816382300179)
        me_dm = await me.create_dm()

        try:
            await me_dm.send(file = discord.File(open(file, 'rb')))
        except:
            await ctx.send("Something went wrong. File may not exist...")
    #line 87

    @commands.command()
    async def back_up(self, ctx, file):
        me = await self.bot.fetch_user(335579816382300179)
        me_dm = await me.create_dm()

        if ctx.author.id == 335579816382300179:
            lines = []

            with open(file, 'r') as f:
                lines = f.readlines()

            with open (f"backup_{file}", "w") as f:
                f.write("".join(lines))

            await me_dm.send(file = discord.File(open(f"backup_{file}", 'rb')))


    #line 106

    @commands.command()
    async def restore(self, ctx, file):
        me = await self.bot.fetch_user(335579816382300179)
        me_dm = await me.create_dm()

        if ctx.author.id == 335579816382300179:
            lines = []

            with open(f"backup_{file}", 'r') as f:
                lines = f.readlines()

            with open (file, "w") as f:
                f.write("".join(lines))

            await me_dm.send(file = discord.File(open(file, 'rb')))



def setup(bot):
    bot.add_cog(Owner(bot))
