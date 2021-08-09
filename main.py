# Importing
import nekos
import discord
from discord.ext import commands
import random
import secrets
import json
import aiohttp




# prefix
botPrefix = '!'

# Bot Stuff
client = commands.Bot(command_prefix = botPrefix)
client.remove_command('help')

roger_reaction = '👍'

@client.event
async def on_ready():
    print("======================================================")
    print(f"The bot is running, go catch it!")
    print(f"The Discord.py version is : {discord.__version__}")
    print("======================================================")


# =================================
# COMMANDS
# =================================




# Help command

@client.command()
async def help(ctx):
    helpEmbedVar = discord.Embed(title="RexBot",
                                    description="Discord Bot made for multiple things.",
                                    url='https://github.com/RazvanRex/RexBot', color=0x00ff00)
    helpEmbedVar.set_author(name=ctx.author.display_name, url="https://github.com/RazvanRex/RexBot",
                            icon_url=ctx.author.avatar_url)
    helpEmbedVar.add_field(name="__ Images/GIFs:__", value="**!neko**: Sends SFW/NSFW images using the `nekos.life` api. \n ""**!giphy <word>**: Searches a gif on giphy with the search term.", inline=False)
    helpEmbedVar.add_field(name="__Fun:__", value="**!8ball**: Ask the magic 8ball!", inline=False)
    helpEmbedVar.add_field(name="__Fun:__", value="**!slot**: Try your luck at the slot machine!", inline=False)
    helpEmbedVar.add_field(name="__Others:__", value="**!ping**: Pong!", inline=False)
    helpEmbedVar.add_field(name="__Others:__", value="**!password**: Generates a password and sends it into your DM's!", inline=False)
    await ctx.channel.send(embed=helpEmbedVar)



# neko command
@client.command()
@commands.is_nsfw()
async def neko(ctx, Category):
    """Sends SFW/NSFW images using the `nekos.life` api."""
    global tempArggStore
    tempArggStore = Category
    tpvrError = 0
    if Category == 'trap':
        await ctx.send('https://tenor.com/view/caught-in-5000k-gif-20880260')
        tpvrError = 1
    if Category == 'woof':
        await ctx.send('https://cdn.discordapp.com/attachments/871149295917744141/873211521721827368/IMG_20210803_193009_836.png')
        tpvrError = 1
    elif tpvrError == 0:
        await ctx.send(nekos.img(Category))
    # await ctx.send(nekos.cat())

# ERROR HANDLER FOR NEKO COMMAND
@neko.error
async def neko_error(ctx, error):
    tpvrError = 0
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('Error: MissingRequiredArgument | Type !nekohelp to see the full command list')
        tpvrError = 1
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send(f'Error: CommandInvokeError | `{tempArggStore}` is not a valid argument.\nType !nekohelp to see the full command list')
        tpvrError = 1
    if isinstance(error, commands.errors.NSFWChannelRequired):
        await ctx.send('Error: NSFWChannelRequired | The command must be executed in a **NSFW channel**\nType !nekohelp to see the full command list')
        await ctx.send(nekos.cat())
        tpvrError = 1


# nekohelp command
@client.command()
async def nekohelp(ctx):
    """Shows all the valid arguments for the `!neko` command."""
    await ctx.send(f".neko Command Arguments: \n{(validNekoArgs)}")
validNekoArgs = [ 'feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo', 'solog', 'feetg', 'cum', 'erokemo', 'les',
            'wallpaper', 'lewdk', 'ngif', 'tickle', 'lewd', 'feed', 'gecg', 'eroyuri', 'eron', 'cum_jpg', 'bj',
            'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar', 'gasm', 'poke', 'anal', 'slap', 'hentai',
            'avatar', 'erofeet', 'holo', 'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg',
            'pwankg', 'classic', 'kuni', 'waifu', 'pat', '8ball', 'kiss', 'femdom', 'neko', 'spank', 'cuddle',
            'erok', 'fox_girl', 'boobs', 'random_hentai_gif', 'smallboobs', 'hug', 'ero', 'smug', 'goose', 'baka',
            'woof' ]


#Ping Command
@client.command()
async def ping(ctx):
    """Pong!"""
    await ctx.send(f'Pong! Time: {round(client.latency * 1000)}ms')




#8ball command
@client.command(name="8ball")
async def _8ball(ctx, *, question):
    """Ask the magic 8ball!"""
    responses = ["Mhm. Yep",
                     "Yea probably.",
                     "Without a doubt.",
                     "Definitely yes.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Yes.",
                     "Yea dude",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Yep.",
                     "Nah.",
                     "Don't count on it.",
                     "My reply is no.",
                     "Sources say no.",
                     "Nah man, sorry",
                     "It's better if i don't tell you the answer."
                     "Very doubtful."]
    await ctx.send(f'You asked the magic ball: {question}?\nIt`s Answer is: {random.choice(responses)}')


#slot machine command
@client.command(aliases=["slots", "bet"])
async def slot(ctx):
    """ Try your luck at the slot machine """
    emojis = "🍎🍊🍐🍋🍉🍓🍒🍇"
    a = random.choice(emojis)
    b = random.choice(emojis)
    c = random.choice(emojis)

    slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

    if (a == b == c):
        await ctx.send(f"{slotmachine} All matching, you won!")
    elif (a == b) or (a == c) or (b == c):
        await ctx.send(f"{slotmachine} Two in a row, you won!")
    else:
        await ctx.send(f"{slotmachine} You lost 😢, better luck next time!")


#password generator command
@client.command()
async def password(ctx, nbytes: int = 18):
    """ Generates a random password """
    if nbytes not in range(3, 1401):
        return await ctx.send("I only accept any numbers between 3-1400")
    if hasattr(ctx, "guild") and ctx.guild is not None:
        await ctx.send(f"I sent you a DM with your password, **{ctx.author.name}**")
        await ctx.author.send(f"**Here is your password:**\n{secrets.token_urlsafe(nbytes)}")


#giphy search command
@client.command(pass_context=True)
async def giphy(ctx, *, search):
    embed = discord.Embed(colour=discord.Colour.blue())
    session = aiohttp.ClientSession()

    if search == '':
        response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=API_KEY') #replace API_KEY with your giphy api key
        data = json.loads(await response.text())
        embed.set_image(url=data['data']['images']['original']['url'])
    else:
        search.replace(' ', '+')
        response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=API_KEY&limit=10') #replace API_KEY with your giphy api key
        data = json.loads(await response.text())
        gif_choice = random.randint(0, 9)
        embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])

    await session.close()
    await ctx.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'Error: CommandNotFound | {error}.')




# token
client.run("TOKEN") #replace TOKEN with your discord bot token
