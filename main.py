import discord
from discord.ext import commands, tasks
from discord.utils import get
import config

intents = discord.Intents.all()
TOKEN = config.configCheck('token')
bot = commands.Bot(command_prefix=config.configCheck('prefix'), intents=intents)

extensions = ['commands', 'events']

for extension in extensions:
    bot.load_extension(extension)

bot.run(TOKEN)