import discord
import statusAPI
import config
from statusAPI import checkSerwer
from discord.ext import commands
from discord.utils import get

ip = config.configCheck('ip')
port = config.configCheck('port')

inviteRanks = [
    #ranga, próg
    ['🏳️', 0],
    ['🏴', 5],
    ['🚩', 10],
    ['🔥', 15],
    ['🚀', 20],
    ['💎', 25],
    ['👑', 50],
]

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @commands.command()
    async def ban(self, ctx, user: discord.Member, *, powod="Brak powodu"):
        adminRank = get(ctx.author.guild.roles, id=config.configCheck('adminrank'))
        if adminRank in ctx.author.roles:
            if not(adminRank in user.roles):
                embed = discord.Embed(title="BAN", description="Użytkownik "+user.display_name+" został zbanowany!", color=0x2333cc)
                embed.add_field(name="Powód: ", value=powod, inline=False)
                embed.add_field(name="Banujący: ", value=ctx.author.display_name, inline=False)
                avatar = user.avatar_url
                embed.set_thumbnail(url=avatar)
                await ctx.send(embed=embed)
        
        
                dm = await user.create_dm()
                embed2 = discord.Embed(title="BAN", description="Zostałeś zbanowany!", color=0x2333cc)
                embed2.add_field(name="Powód: ", value=powod, inline=False)
                embed2.add_field(name="Banujący: ", value=ctx.author.display_name, inline=False)
                await dm.send(embed=embed2)
                await user.guild.ban(user, reason=powod+" ~"+ctx.author.display_name)

    @commands.command()
    async def zaproszenia(self, ctx):
        totalInvites = 0
        for i in await ctx.guild.invites():
            if i.inviter == ctx.author:
                totalInvites += i.uses
        embed = discord.Embed(title="Zaproszenia", description="Zaprosiłeś "+str(totalInvites)+" osób na discorda.", color=0x2333cc)
        checkRank = []
        for rank in inviteRanks:
            if totalInvites >= rank[1]:
                dodaj = [rank[0], rank[1]]
                checkRank.append(dodaj)
        rangaNazwa = None
        rangaProg = 0
        for rank in checkRank:
            if rangaProg <= rank[1]:
                rangaNazwa = rank[0]
                rangaProg = rank[1]
                
        embed.add_field(name="Twoja ranga: ", value=rangaNazwa, inline=False)
        avatar = ctx.author.avatar_url
        embed.set_thumbnail(url=avatar)
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="POMOC", description="Lista dostępnych komend", color=0x3333cc)
        embed.add_field(name="*zaproszenia", value="Twoja aktualna ranga oraz liczba zaproszonych osób", inline=False)
        embed.add_field(name="*serwer", value="Informacje o tym serwerze", inline=False)
        embed.add_field(name="*status", value="Status serwera MTA", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def serwer(self, ctx):
        online=[]
        offline=[]
        for user in ctx.guild.members:
            if user.status != discord.Status.offline:
                online.append(user)
            else:
                offline.append(user)
        guild = ctx.author.guild
        description=guild.name+'\n:green_circle: Online: '+str(len(online))+'\n:red_circle: Offline: '+str(len(offline))+'\nRegion: '+str(guild.region)+'\nWłaściciel: '+guild.owner.display_name
        embed = discord.Embed(title="Informacje Serwerowe", description=description, color=0x3333cc)
        icon = guild.icon_url
        embed.set_thumbnail(url=icon)
        await ctx.send(embed=embed)


    @commands.command()
    async def status(self, ctx):
        object = checkSerwer(ip, port)
        players = object.players+"/"+object.maxplayers
        embed = discord.Embed(title=object.name, description="Informacje o serwerze:", color=0x3333cc)
        embed.add_field(name="Online", value=players, inline=True)
        embed.add_field(name="Adres IP", value='mtasa://'+ip+':'+str(port), inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Commands(bot))