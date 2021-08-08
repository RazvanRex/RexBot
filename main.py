# Importing the library
import nekos
import discord
from discord.ext import commands
import random


# prefix
botPrefix = '!'

# Bot Stuff
client = commands.Bot(command_prefix = botPrefix)
client.remove_command('help')

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
    helpEmbedVar.add_field(name="Images/GIFs:", value="**!neko**: Sends SFW/NSFW images using the `nekos.life` api.", inline=False)
    helpEmbedVar.add_field(name="Fun:", value="**!8ball**: Ask the magic 8ball!", inline=False)
    helpEmbedVar.add_field(name="Others:", value="**!ping**: Pong!", inline=False)
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


# Ping Command
@client.command()
async def ping(ctx):
    """Pong!"""
    await ctx.send(f'Pong! Time: {round(client.latency * 1000)}ms')


# Info command
#@client.command()
#async def info(ctx, *, member: discord.user):
#    """Tells you some info about the member."""
#    fmt = '{0} joined on {0.joined_at} and has {1} roles.'
#    await ctx.send(fmt.format(member, len(member.roles)))

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



@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'Error: CommandNotFound | {error}.')



# token
client.run("TOKEN")
