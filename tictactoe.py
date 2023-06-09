import random
import discord
import json

from discord.ext import tasks, commands

class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = []

    @commands.command(name = 'tictactoe', cls = None, description = "Epic Bot will learn to play Tic Tac Toe with you.")
    async def tictactoe(self,ctx,opponent = None):
        # if ctx.author.id != 335579816382300179:
        #     return

        # await ctx.send(Case(['1️⃣','⭕','3️⃣','❌','⭕','6️⃣','7️⃣','❌','9️⃣'], {'1️⃣':7, '3️⃣':9, '6️⃣':2.6, '7️⃣':0.2, '9️⃣':1}).flip_board(['1️⃣','⭕','3️⃣','❌','⭕','6️⃣','7️⃣','❌','9️⃣']))
        for game in self.games:
            if game.player[1] == ctx.author:
                await ctx.send("You're already playing!")

                return

        if opponent is None:
            opponent = self.bot.user
        else:
            if '!' in opponent:
                opponent = self.bot.get_user(int(opponent[3:len(opponent) - 1]))
            else:
                opponent = self.bot.get_user(int(opponent[2:len(opponent) - 1]))

            if opponent not in ctx.guild.members:
                await ctx.send("Couldn't find that player...")
                return
            
            if opponent == ctx.author:
                await ctx.send("You can't play against yourself!")
                return
            # else:
                # await ctx.send("Player found!")
                # return
                # pass

        self.games.append(Game(self.bot, ctx.author, opponent))

        await ctx.send(embed = self.games[-1].play())

    @commands.Cog.listener()
    async def on_message(self, message):
        for embed in message.embeds:
            if message.author == self.bot.user and embed.title == "Tic Tac Toe!":
                for game in self.games:
                    if not game.complete and (game.player[1].name == embed.fields[2].value or (game.player[0].name == embed.fields[1].value and game.player[0] != self.bot.user)):
                        game.game_message = message
                        for spot in game.board:
                            if spot != '⭕' and spot != '❌':
                                await message.add_reaction(spot)

                        await game.end_game.start()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, member):
        if member == self.bot.user:
            return

        for embed in reaction.message.embeds:
            if reaction.message.author == self.bot.user and embed.title == 'Tic Tac Toe!':
                for game in self.games:
                    if not game.complete and game.cur_player != self.bot.user and game.cur_player == member:
                        game.reset_timer()
                        await reaction.message.edit(embed = game.play(reaction))

                        if not game.complete and game.cur_player == self.bot.user:
                            # time.sleep(2)
                            # await reaction.message.edit(embed = game.play())
                            # await game.end_game.start()
                            await game.bot_play.start()
                        elif not game.complete and game.cur_player != self.bot.user:
                            await game.end_game.start()

                    if game.complete:
                        self.games.pop(self.games.index(game))


class Case:
    def __init__(self, board, unused):
        self.board = [spot for spot in board]
        self.default = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']

        if unused == {}:
            for spot in board:
                if spot != '⭕' and spot != '❌':
                    unused[spot] = 100
        
        self.unused = unused

    def format_board(self, board):
        square = []

        for i in range(len(board)):
            if i % 3 == 0:
                square.append([])

        for i in range(len(board)):
            square[int(i / 3)].append(board[i])

        return square

    def deformat_board(self, board):
        line = []

        for row in board:
            for spot in row:
                line.append(spot)

        return line
        

    def rotate_board(self, board, times = 1, keepUnused = True):
        formated = self.format_board(board)
        rotated = []
        for i in range(len(board)):
            rotated.append('')

        rotated = self.format_board(rotated)

        for i, row in enumerate(formated):
            for j, spot in enumerate(row):
                change_r = int(i)
                change_s = int(j)

                if not (change_r == 1 and change_s == 1):
                    for t in range(2*times):
                        if change_r == 0 and change_s + 1 < 3:
                            change_s += 1
                        elif change_s == 2 and change_r + 1 < 3:
                            change_r += 1
                        elif change_r == 2 and change_s - 1 > -1:
                            change_s -= 1
                        elif change_s == 0 and change_r - 1 > -1:
                            change_r -= 1

                if not keepUnused:
                    rotated[change_r][change_s] = spot

                elif spot == '⭕' or spot == '❌':
                    rotated[change_r][change_s] = spot

        rotated = self.deformat_board(rotated)

        if keepUnused:
            for i in range(len(rotated)):
                if rotated[i] != '⭕' and rotated[i] != '❌':
                    rotated[i] = self.default[i]


        return rotated


    def flip_board(self, board, keepUnused = True):
        flipped = []

        for i in range(len(board)):
            flipped.append('')

        for i, spot in enumerate(board):
            change = int(i)

            if i % 3 < 1:
                change += 2
            elif i % 3 > 1:
                change -= 2

            if not keepUnused:
                flipped[change] = board[i]
            elif spot == '⭕' or spot == '❌':
                flipped[change] = board[i]

        if keepUnused:
            for i in range(len(flipped)):
                if flipped[i] != '⭕' and flipped[i] != '❌':
                    flipped[i] = self.default[i] 

        return flipped


class Game(commands.Cog):
    def __init__(self,bot,player,opponent):
        self.bot = bot

        self.player = [opponent, player]
        self.cur_player = self.player[0]
        self.turn = f"{self.player[0].name}'s turn"

        self.started = False
        self.complete = False
        self.default = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']
        self.board = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']

        self.cur_cases = []
        self.cur_moves = []

        self.game_message = None

    # creates a message to send/edit in the chat
    def create_message(self):
        game_value = ''

        # for i,row in enumerate(self.board):
        #     for j,spot in enumerate(row):
        #         game_value += spot
        #         if j < 2:
        #             game_value += '⬜'

        #     if i < 2:
        #         game_value += '\n⬜⬜⬜⬜⬜\n'

        for i, spot in enumerate(self.board):
            if i%3 != 0:
                game_value += '⬜'
            elif i > 0:
                game_value += '\n⬜⬜⬜⬜⬜\n'

            game_value += spot

        game = discord.Embed(title = f"Tic Tac Toe!", color = discord.Colour.teal())
        game.add_field(name = self.turn, value = game_value)
        game.add_field(name = "O", value = f"{self.player[0].name}")
        game.add_field(name = "X", value = f"{self.player[1].name}")

        return game

    # checks if the player won
    def player_wins(self, move):
        # this is probably really bad and terrible and inefficient,
        # but let's just say it's a feature

        # check all rows
        for i in range(0,len(self.board),3):
            if self.board[i] == self.board[i + 1] and self.board[i] == self.board[i + 2] and self.board[i] == move:
                return True
        
        # check all columns
        for i in range(0,3,1):
            if self.board[i] == self.board[i + 3] and self.board[i] == self.board[i + 6] and self.board[i] == move:
                return True

        # check diagonals
        if self.board[0] == self.board[4] and self.board[0] == self.board[8] and self.board[0] == move:
            return True
        if self.board[2] == self.board[4] and self.board[2] == self.board[6] and self.board[2] == move:
            return True

        return False

    
    # makes whoever is playing put their space on the board
    def play(self, reaction = None):
        # check if player is opponent
        if self.cur_player == self.player[0]:
            # check if opponent is epic bot

            # opponent is epic bot
            if self.cur_player == self.bot.user:
                f = open("cases.json", "r")
                c = f.read()
                cases = json.loads(c)

                temp_case = Case(self.board,{})
                rotations = 0
                flip = False

                # you finished unused cases
                # work on random 

                if " ".join(temp_case.board) not in cases['water']:
                    for t in range(6):
                        temp_case.board = temp_case.rotate_board(temp_case.board)
                        rotations += 1

                        if " ".join(temp_case.board) in cases['water']:
                            break

                        if t == 2:
                            temp_case.board = temp_case.flip_board(temp_case.board)
                            flip = True
                            if " ".join(temp_case.board) in cases['water']:
                                break

                if " ".join(temp_case.board) not in cases['water']:
                    # for t in range(rotations):
                    #     if rotations - t == 3:
                    #         if flip:
                    #             temp_case.board = temp_case.flip_board(temp_case.board)
                        
                    #     for iter in range(3):
                    #         temp_case.board = temp_case.rotate_board(temp_case.board)
                    temp_case = Case(self.board,{})
                    self.cur_cases.append(Case(temp_case.board,{}))

                else:
                    temp_case = Case(temp_case.board, cases['water'][" ".join(temp_case.board)]['unused'])
                    self.cur_cases.append(Case(temp_case.board, cases['water'][" ".join(temp_case.board)]['unused']))

                    for t in range(rotations):
                        if rotations - t == 3:
                            if flip:
                                temp_case.board = temp_case.flip_board(temp_case.board,False)
                        for iter in range(3):
                            temp_case.board = temp_case.rotate_board(temp_case.board, 1,False)
                    
                limit = 0
                for key in temp_case.unused:
                    limit += temp_case.unused[key]

                ai_r = random.uniform(0,limit)

                finder = 0
                choice = ''

                for key in temp_case.unused:
                    finder += temp_case.unused[key]
                    if finder > ai_r:
                        choice = key
                        break

                self.cur_moves.append(choice)

                self.board[temp_case.board.index(choice)] = '⭕'


                # r = random.randint(0,8)

                # while(self.board[r] == '⭕' or self.board[r] == '❌'):
                #     r = random.randint(0,8)

                # self.board[r] = '⭕'

                if self.player_wins('⭕'):
                    for i,case in enumerate(self.cur_cases):
                        case.unused[self.cur_moves[i]] += 100
                        cases['water'][" ".join(case.board)] = {'unused': case.unused}

                    with open('cases.json','w') as case_file:
                        json.dump(cases,case_file,ensure_ascii=False)

                    self.turn = f"{self.cur_player.name} wins!"
                    self.complete = True
                    return self.create_message()
                else:
                    for num in self.default:
                        if num in self.board:
                            self.cur_player = self.player[1]
                            self.turn = f"{self.cur_player.name}'s turn"
                            return self.create_message()

                    for i,case in enumerate(self.cur_cases):
                        case.unused[self.cur_moves[i]] += 50
                        cases['water'][" ".join(case.board)] = {'unused': case.unused}

                    with open('cases.json','w') as case_file:
                        json.dump(cases,case_file,ensure_ascii=False)

                    self.complete = True
                    self.turn = "It's a draw!"
                    return self.create_message()


                # self.cur_player = self.player[1]
                # self.turn = f"{self.cur_player.name}'s turn"
                # return self.create_message()

            # opponent is a user
            else:
                if self.board == self.default and not self.started:
                    self.started = True
                    return self.create_message()

                for i,spot in enumerate(self.board):
                    if spot == reaction.emoji and spot != '⭕' and spot != '❌':
                        self.board[i] = '⭕'

                        if self.player_wins('⭕'):
                            self.turn = f"{self.cur_player.name} wins!"
                            self.complete = True
                            return self.create_message()

                        self.cur_player = self.player[1]
                        self.turn = f"{self.cur_player.name}'s turn"
                        return self.create_message()

                self.complete = True
                self.turn = "It's a draw!"
                return self.create_message()

        # check if player is challenger (will always be a user)
        if self.cur_player == self.player[1]:
            for i,spot in enumerate(self.board):
                if spot == reaction.emoji and spot != '⭕' and spot != '❌':
                    self.board[i] = '❌'

                    if self.player_wins('❌'):
                        if self.player[0] == self.bot.user:
                            f = open("cases.json", "r")
                            c = f.read()
                            cases = json.loads(c)

                            has_non_zero = False
                            
                            for i,case in enumerate(self.cur_cases):
                                for key in case.unused:
                                    if case.unused[key] != 0:
                                        has_non_zero = True
                                        break

                                if has_non_zero:
                                    case.unused[self.cur_moves[i]] -= 50
                                    if case.unused[self.cur_moves[i]] < 0:
                                        case.unused[self.cur_moves[i]] = 0
                                else:
                                    for key in case.unused:
                                        case.unused[key] = 100
                                    
                                cases['water'][" ".join(case.board)] = {'unused': case.unused}

                            with open('cases.json','w') as case_file:
                                json.dump(cases,case_file,ensure_ascii=False)
                
                        self.turn = f"{self.cur_player.name} wins!"
                        self.complete = True
                        return self.create_message()

                    self.cur_player = self.player[0]
                    self.turn = f"{self.cur_player.name}'s turn"

                    return self.create_message()

    def reset_timer(self):
        self.end_game.cancel()

    @tasks.loop(seconds = 60, count = 2)
    async def end_game(self):

        if self.end_game.current_loop == 1:
            expired = discord.Embed(title = "Tic Tac Toe!", color = discord.Colour.teal())
            expired.add_field(name = f"{self.cur_player.name} took too long.", value = "Game over!")
            await self.game_message.edit(embed = expired)
            
            self.complete = True

            tcog = self.bot.get_cog("TicTacToe")
            tcog.games.pop(tcog.games.index(self))

    @tasks.loop(seconds = 2, count = 2)
    async def bot_play(self):

        if self.bot_play.current_loop == 1:
            await self.game_message.edit(embed = self.play())

            if not self.complete:
                await self.end_game.start()


def setup(bot):
    bot.add_cog(TicTacToe(bot))