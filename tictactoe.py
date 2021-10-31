import random
import time
import discord

from discord.ext import tasks, commands

class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = []

    @commands.command()
    async def tictactoe(self, ctx, opponent):
        for game in self.games:
            if game.player[0] == ctx.author:
                await ctx.send("You're already playing!")

                return

        self.games.append(Game(self.bot, ctx.author))

        await ctx.send(embed = self.games[len(self.games) - 1].create_message())

    @commands.command()
    async def cur_games(self, ctx):
        if ctx.author.id == 335579816382300179:
            await ctx.send(len(self.games))

    @commands.Cog.listener()
    async def on_message(self, message):
        for embed in message.embeds:
            if embed.fields[0].name == 'Your Turn' and message.author == self.bot.user:
                for game in self.games:
                    if game.player[0].name == embed.fields[1].value:
                        for row in game.board:
                            for spot in row:
                                if spot != '⭕' and spot != '❌':
                                    await message.add_reaction(spot)

                        await game.end_game.start(message.channel)


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, member):
        for embed in reaction.message.embeds:
            if embed.fields[0].name == 'Your Turn' and reaction.message.author == self.bot.user:
                for game in self.games:
                    if game.player[0] == member:
                        game.reset_timer()

                        if not game.complete:
                            await reaction.message.edit(embed = game.play(reaction))

                        if not game.complete:
                            async with reaction.message.channel.typing():
                                time.sleep(2)
                                await reaction.message.channel.send(embed = game.play())

                        if game.complete:
                            self.games.pop(self.games.index(game))




class Game(commands.Cog):
    def __init__(self, bot, player):
        self.bot = bot
        self.player = [player]
        self.complete = False
        self.turn = "Your Turn"
        self.counter = 0

        self.board = [
            ['1️⃣','2️⃣','3️⃣'],
            ['4️⃣','5️⃣','6️⃣'],
            ['7️⃣','8️⃣','9️⃣']]

        self.game_value = ''

    def create_message(self):
        for i,row in enumerate(self.board):
            for j,spot in enumerate(row):
                self.game_value += spot
                if j < 2:
                    self.game_value += '⬜'

            if i < 2:
                self.game_value += '\n⬜⬜⬜⬜⬜\n'

        game = discord.Embed(title = f"Tic Tac Toe!", color = discord.Colour.teal())
        game.add_field(name = self.turn, value = self.game_value)
        game.add_field(name = "O", value = f"{self.player[0].name}")
        game.add_field(name = "X", value = "Epic Bot")

        self.game_value = ''

        return game

    def play(self, reaction = None):

        if self.turn == "Your Turn":
            for i,row in enumerate(self.board):
                for j,spot in enumerate(row):
                    if reaction.emoji == spot:
                        self.board[i][j] = '⭕'

            self.turn = "Epic Bot's Turn"

            for i,row in enumerate(self.board):
                for j,spot in enumerate(row):
                    if i == 0 and self.board[i][j] == self.board[i + 1][j] and self.board[i][j] == self.board[i + 2][j] and self.board[i][j] == '⭕':
                        self.turn = "You win!"

                        self.complete = True

                    if j == 0 and self.board[i][j] == self.board[i][j + 1] and self.board[i][j] == self.board[i][j + 2] and self.board[i][j] == '⭕':
                        self.turn = "You win!"

                        self.complete = True

            if self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2] and self.board[0][0] == '⭕':
                self.turn = "You win!"

                self.complete = True

            if self.board[2][0] == self.board[1][1] and self.board[2][0] == self.board[0][2] and self.board[2][0] == '⭕':
                self.turn = "You win!"

                self.complete = True

        elif self.turn == "Epic Bot's Turn":
            for row in self.board:
                for spot in row:
                    if spot != '⭕' and spot != '❌':

                        while True:
                            bot_row = random.randint(0,2)
                            bot_spot = random.randint(0,2)

                            if self.board[bot_row][bot_spot] != '⭕' and self.board[bot_row][bot_spot] != '❌':
                                self.board[bot_row][bot_spot] = '❌'

                                self.turn = "Your Turn"

                                for i,row in enumerate(self.board):
                                    for j,spot in enumerate(row):
                                        if i == 0 and self.board[i][j] == self.board[i + 1][j] and self.board[i][j] == self.board[i + 2][j] and self.board[i][j] == '❌':
                                            self.turn = "Epic Bot Wins!"

                                            self.complete = True

                                        if j == 0 and self.board[i][j] == self.board[i][j + 1] and self.board[i][j] == self.board[i][j + 2] and self.board[i][j] == '❌':
                                            self.turn = "Epic Bot Wins!"

                                            self.complete = True

                                if self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2] and self.board[0][0] == '❌':
                                    self.turn = "Epic Bot Wins!"

                                    self.complete = True

                                if self.board[2][0] == self.board[1][1] and self.board[0][2] == self.board[2][0] and self.board[0][2] == '❌':
                                    self.turn = "Epic Bot Wins!"

                                    self.complete = True

                                return self.create_message()

            self.turn = "It's a draw!"
            self.complete = True



        return self.create_message()

    def reset_timer(self):
        self.counter = 0
        self.end_game.cancel()

    @tasks.loop(seconds = 25)
    async def end_game(self, channel):

        if self.counter == 1:
            await channel.send(f"You took too long to play, <@{self.player[0].id}>. Game over!")
            self.complete = True
            self.counter = 0

            tictactoe = self.bot.get_cog('TicTacToe')
            tictactoe.games.pop(tictactoe.games.index(self))

            self.end_game.cancel()

        self.counter += 1




def setup(bot):
    bot.add_cog(TicTacToe(bot))
