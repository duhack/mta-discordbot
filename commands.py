#AUTHOR: duhack
#GITHUB: https://github.com/duhack
#WWW: https://duhack.pl/ 

import discord
import statusAPI
import config
import mysql.connector
from statusAPI import checkSerwer
from discord.ext import commands
from discord.utils import get

ip = config.configCheck('ip')
port = config.configCheck('port')

configMysql = {
    'user': config.configCheck('user'), #uzytkownik bazy danych
    'password': config.configCheck('password'), #haslo do bazy danych
    'host': config.configCheck('host'), #ip bazy danych
    'database': config.configCheck('database'), #baza danych
}

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
                embed = discord.Embed(title="BAN", description="Użytkownik "+user.display_name+" został zbanowany!", color=config.configCheck('embed_color'))
                embed.add_field(name="Powód: ", value=powod, inline=False)
                embed.add_field(name="Banujący: ", value=ctx.author.display_name, inline=False)
                avatar = user.avatar_url
                embed.set_thumbnail(url=avatar)
                await ctx.send(embed=embed)
        
        
                dm = await user.create_dm()
                embed2 = discord.Embed(title="BAN", description="Zostałeś zbanowany!", color=config.configCheck('embed_color'))
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
        embed = discord.Embed(title="Zaproszenia", description="Zaprosiłeś "+str(totalInvites)+" osób na discorda.", color=config.configCheck('embed_color'))
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
        embed = discord.Embed(title="POMOC", description="Lista dostępnych komend", color=config.configCheck('embed_color'))
        embed.add_field(name="*zaproszenia", value="Twoja aktualna ranga oraz liczba zaproszonych osób", inline=False)
        embed.add_field(name="*serwer", value="Informacje o tym serwerze", inline=False)
        embed.add_field(name="*status", value="Status serwera MTA", inline=False)
        embed.add_field(name="*synchronizacja <kod>", value="Połączenie konta discord, z grą", inline=False)
        embed.add_field(name="AUTOR:", value="duhack", inline=False) #tego nie usuwaj!
        embed.add_field(name="GITHUB:", value="https://github.com/duhack/mta-discordbot", inline=False) #tego nie usuwaj!
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
        embed = discord.Embed(title="Informacje Serwerowe", description=description, color=config.configCheck('embed_color'))
        icon = guild.icon_url
        embed.set_thumbnail(url=icon)
        await ctx.send(embed=embed)


    @commands.command()
    async def status(self, ctx):
        object = checkSerwer(ip, port)
        players = object.players+"/"+object.maxplayers
        embed = discord.Embed(title=object.name, description="Informacje o serwerze:", color=config.configCheck('embed_color'))
        embed.add_field(name="Online", value=players, inline=True)
        embed.add_field(name="Adres IP", value='mtasa://'+ip+':'+str(port), inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def synchronizacja(self, ctx, code = None):
        embed = None
        if code is not None:
            connection = mysql.connector.connect(**configMysql)
            sql_select_Query = "select * from `synchronizacja-dsc` WHERE code='"+code+"'"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            znaleziono = False
            for row in records:
                znaleziono = True
                if str(row[2]) == "nie":
                    cursor.execute("select `nick` from players WHERE uid='"+str(row[0])+"'")
                    records_nick = cursor.fetchall()
                    member = ctx.author
                    role = get(member.guild.roles, id=config.configCheck('synchro_rank')) #ranga ktora ma nadac po pomyslnej synchronizacji
                    await member.add_roles(role)
                    embed = discord.Embed(title="Synchronizacja konta", description="Synchronizacja konta przebiegła prawidłowo, otrzymujesz rangę Zweryfikowany.", color=config.configCheck('embed_color'))
                    embed.add_field(name="Serwer", value=records_nick[0][0])
                    embed.add_field(name="Discord", value=member)
                    sql = "UPDATE `synchronizacja-dsc` SET used = %s, account_discord = %s WHERE code=%s"
                    val = ("tak", member.id, code)
                    cursor.execute(sql, val)
                    connection.commit()
                else:
                    embed = discord.Embed(title="Synchronizacja konta", description="Ten klucz został już zrealizowany!", color=config.configCheck('embed_color'))
            if znaleziono == False:
                embed = discord.Embed(title="Synchronizacja konta", description="Podany kod jest nieprawidłowy!", color=config.configCheck('embed_color'))
            connection.close()
            cursor.close()
        else:
            embed = discord.Embed(title="Synchronizacja konta", description="Aby użyć tej komendy wykonaj wygeneruj klucz w grze (/discord),\n a następnie wpisz go w tej formie: *synchronizacja <KOD>\n Aby sprawdzić status twojej synchronizacji - użyj komendy (/discord-status)", color=config.configCheck('embed_color'))
        if not embed == None:
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Commands(bot))