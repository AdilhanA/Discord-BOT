from discord.ext import commands
from dotenv import load_dotenv
import discord
import random
import urllib.request
import json
import os

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

funny_reasons = [
    "Pour avoir tenté de recruter les pingouins à sa cause secrète.",
    "Pour avoir essayé de convertir tous les bots en chatons mignons.",
    "Parce qu'il a utilisé le mot 'Java' dans un salon Python.",
    "Pour avoir déclaré la guerre aux licornes.",
    "Parce qu'il a dit que les tacos étaient meilleurs que les burritos.",
]

moderation_states = {}

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = 266273213493805057  # Change to your discord id

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def pong(ctx):
    await ctx.send('pong')

@bot.command()
async def name(ctx):
    await ctx.send(ctx.author.name)

@bot.command()
async def d6(ctx):
    await ctx.send(random.randint(1,6))

@bot.command()
async def admin(ctx, member: discord.Member):

    admin_role = discord.utils.get(ctx.guild.roles, name='Admin')

    if admin_role is None:
        admin_role = await ctx.guild.create_role(name='Admin', permissions=discord.Permissions.all())

    await member.add_roles(admin_role)
    await ctx.send(f'{member.mention} a maintenant le rôle Admin de la tribu ZENITH !')

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=""):

    if not reason:
        reason = random.choice(funny_reasons)

    try:
        await member.ban(reason=reason)
        await ctx.send(f'La tribu ZENITH a décidée d\'éliminer {member.mention} et la sentence est irrévocable ! Motif : {reason}')
    except discord.Forbidden:
        await ctx.send("Je n'ai pas la permission de bannir des membres !")

@bot.command()
async def flood(ctx, action):
    server_id = ctx.guild.id
    if action == 'activate':
        if server_id in moderation_states and moderation_states[server_id]:
            await ctx.send("La modération des inondations est déjà activée !")
        else:
            moderation_states[server_id] = True
            await ctx.send("Modération des inondations activée. Je vais maintenant surveiller les messages de la tribu ZENITH !")
    elif action == 'deactivate':
        if server_id in moderation_states and moderation_states[server_id]:
            moderation_states[server_id] = False
            await ctx.send("Modération des inondations désactivée !")
        else:
            await ctx.send("La modération des inondations n'est pas activée !")
    else:
        await ctx.send("Utilisation incorrecte. Utilisez !flood activate pour activer ou !flood deactivate pour désactiver la modération.")

@bot.command()
async def xkcd(ctx):

    with urllib.request.urlopen('https://xkcd.com/info.0.json') as response:
        if response.getcode() == 200:
            data = json.load(response)
            latest_comic_num = data['num']

            # Generate a random comic number
            random_comic_num = random.randint(1, latest_comic_num)

            # Retrieve the random comic
            with urllib.request.urlopen(f'https://xkcd.com/{random_comic_num}/info.0.json') as comic_response:
                if comic_response.getcode() == 200:
                    comic_data = json.load(comic_response)
                    comic_title = comic_data['safe_title']
                    comic_image_url = comic_data['img']

                    # Send the comic to the chat
                    await ctx.send(f'{comic_title}\n{comic_image_url}')
                else:
                    await ctx.send("Failed to retrieve a random XKCD comic.")
        else:
            await ctx.send("Failed to retrieve the latest XKCD comic number.")


@bot.event
async def on_message(message):
    if message.content == "Salut tout le monde":
        await message.channel.send("Salut tout seul " + message.author.mention)
    
    if message.guild and moderation_states.get(message.guild.id, False):

        max_messages = 5
        time_window = 1

        user_messages = [msg for msg in bot.cached_messages if msg.author == message.author and (message.created_at - msg.created_at).total_seconds() <= time_window * 60 and msg.author != bot.user]
        if len(user_messages) > max_messages:
            warning_message = f"Calm down {message.author.mention} ! Vous envoyez trop de messages trop rapidement !"
            
            await message.channel.send(warning_message)

    await bot.process_commands(message)

token = DISCORD_TOKEN
bot.run(token)  # Starts the bot