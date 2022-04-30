import discord
from discord.ext import commands
import json
import random

# Get configuration.json
with open("configuration.json", "r") as config:
    data = json.load(config)
    token = data["token"]
    prefix = data["prefix"]

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True

bot = commands.Bot(prefix, intents = intents)

# Load cogs
initial_extensions = [
    "Cogs.help",
    "Cogs.ping"
]

print(initial_extensions)

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}")

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))
    print(discord.__version__)

user_list = []
start_game = 0
@bot.command()
async def start(ctx):
    tick = '✅'
    play = '🔫'

    embed=discord.Embed(title="Russian Roulette", description="Fun game of Russian Roulette", color=0xe8e8e8)
    embed.add_field(name="Join", value="React ✅ to join game", inline=False)
    embed.add_field(name="Start", value=f"React 🔫 to join game \nNote only {ctx.message.author.mention} can start the game", inline=False)
    message = await ctx.send(embed=embed)
    
    await message.add_reaction(tick)
    await message.add_reaction(play)
    
    def check(reaction, user):
        return user == ctx.author and str(
            reaction.emoji) in [tick, play]
    
    while True:
        reaction, user = await bot.wait_for("reaction_add", check=check)

        if str(reaction.emoji) == tick:
            print("added user")
        
        if len(user_list) > 0:
            if str(reaction.emoji) == play:
                print("game started")
                #await ctx.send('\n'.join(map(str, user_list)))
                for users in user_list:
                    mension = bot.get_user(users)
        
                length = len(user_list) 
                print(f"number of items in list = {length}")                     
                start_embed=discord.Embed(title="Russian Roulette", description="Game Started", color=0xe8e8e8)
                start_embed.add_field(name="Join", value="Type `!shoot` to play", inline=False)
                start_embed.add_field(name="Users", value=f"{mension}\n")
                await ctx.send(embed = start_embed)
                global start_game
                start_game = 1
        else:
            await ctx.send("No one has joined game")

##################################################################
@bot.event
async def on_reaction_add(reaction, user):
    tick = '✅'
    play = '🔫'
    bot_id = 965889758427508786

    if str(reaction.emoji) == tick and user.id not in user_list:
        print(reaction, user)
        global add_user
        add_user = user_list.append(user.id)
        print(user_list)
    
    if str(reaction.emoji) == play and user.id in user_list and len(user_list) != 0:
        if bot_id in user_list:
            user_list.remove(bot_id)
        print(user_list)

######################################
@bot.command(name='shoot', help='Use this command to play after the game has started')
async def shoot(ctx):
    global start_game
    if start_game != 0:
        if ctx.message.author.id in user_list:
            print("true")
            generate = random.randint(1,6)
            print(generate)
            
            turn = user_list[0]
            print(turn)
            find_user = bot.get_user(turn)
            global mention
            
            mention = ctx.message.author.mention

            #await ctx.send(f"{mention}'s turn\n type `cmd`")
            
            embed1 = discord.Embed(title="Russian Roulette", description=f"{mention}, has shot", color=0x00ff00)
            embed1.add_field(name="Alive", value=f"{mention} lives to see another day", inline=False)

            embed2=discord.Embed(title="Russian Roulette", description=f"{mention}, has shot", color=0xff0000)
            embed2.add_field(name="Dead", value=f"kicked {mention}", inline=False)
            
            if ctx.author.id in user_list:
                if int(generate) == 1:
                    await ctx.send(embed=embed1)       
                if int(generate) == 2:
                    await ctx.send(embed=embed1) 
                if int(generate) == 3:                
                    await ctx.send(embed=embed1)
                if int(generate) == 4:
                    await ctx.send(embed=embed1)
                if int(generate) == 5:                
                    await ctx.send(embed=embed1)
                if int(generate) == 6:
                    await ctx.send(embed=embed2)
                    start_game = 0
        else:
            await ctx.send("You are not in a game")
    else:
        await ctx.send("Game not started \n`!start` to start a game")

@bot.command()
async def test(ctx):
    print("----test----")
    for users in user_list:
        await ctx.send(bot.get_user(users))

bot.run(token)