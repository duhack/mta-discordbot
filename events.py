import discord
import statusAPI
import config
from statusAPI import checkSerwer
from discord.ext import commands, tasks
from discord.utils import get

ip = config.configCheck('ip')
port = config.configCheck('port')

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=5.0)
    async def statusUpdate(self):
        object = checkSerwer(ip, port)
        stat = discord.Game(config.configCheck('name')+' | '+str(object.players)+"/"+str(object.maxplayers))
        await self.bot.change_presence(status=discord.Status.online, activity=stat)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Zalogowano!')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('------')
        self.statusUpdate.start()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 800155538566414416:
            channel1 = self.bot.get_channel(800157442260336652)
            await channel1.edit(name="🎈 Jest nas: "+str(member.guild.member_count))
            channel2 = self.bot.get_channel(800157512644296704)
            await channel2.edit(name="🎈 Nowy: "+str(member.name))

def setup(bot):
    bot.add_cog(events(bot))