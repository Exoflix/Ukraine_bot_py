import discord
from discord.ext import commands
import asyncio
import os
from discord.utils import get
import colorsys
import requests
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
import youtube_dl

bot = commands.Bot(command_prefix = "y!", description = "YoRHaBot")
bot.remove_command('help')
musics = {}
ytdl = youtube_dl.YoutubeDL()

async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "Creation du role Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

async def on_message(self, message):
	def _check(m):
		return (m.author == message.author
				and len(m.mentions)
				and (datetime.utcnow()-m.created_at).seconds < 60)

	if not message.author.bot:
		if len(list(filter(lambda m: _check(m), self.bot.cached_messages))) >= 3:
			await message.channel.send("Don't spam mentions!", delete_after=10)
			unmutes = await self.mute_members(message, [message.author], 5, reason="Mention spam")

			if len(unmutes):
				await sleep(5)
				await self.unmute_members(message.guild, [message.author])

		elif profanity.contains_profanity(message.content):
			await message.delete()
			await message.channel.send("You can't use that word here.", delete_after=10)

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role

    return await createMutedRole(ctx)

@bot.command()
@commands.has_permissions(kick_members = True)
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.magenta()
    )
    test_e.add_field(name=f"{member.name} a été mute !", value="Merci de ne pas le mentionner durant son mute")
    test_e.set_footer(text="YoRHa", icon_url=bot.user.avatar_url)
    test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
    test_e.set_thumbnail(url = "https://i.imgur.com/sOHZQZI.png")
    await ctx.send(embed=test_e)
    await member.add_roles(mutedRole, reason = reason)

@bot.command()
@commands.has_permissions(kick_members = True)
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.magenta()
    )
    test_e.add_field(name=f"{member.name} a été unmute !", value="Ne refait pas la même bétise", inline=False)
    test_e.set_footer(text="YoRHa", icon_url=bot.user.avatar_url)
    test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
    test_e.set_thumbnail(url = "https://i.imgur.com/7NieAyC.png")
    await ctx.send(embed=test_e)
    await member.remove_roles(mutedRole, reason = reason)


@bot.command()
async def test(ctx):
	await ctx.send(f":white_check_mark: | Le Bot est fonctionnel !")

@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")

@bot.command()
async def repeat(ctx):
	print("repeat")
	client = ctx.guild.voice_client
	client.repeat()
	await ctx.send("La vidéo est répété indéfiniment")

@bot.command()
async def sendembed(ctx):
    embed = discord.Embed(
        title="Test Embed",
        color=discord.Color.blue(),
        description="Some description that I wrote without even thinking about it."
    )
    embed.add_field(
        name="Field 1", value="This is the 1st inline field.", inline=True)
    embed.add_field(
        name="Field 2", value="This is the 2nd inline field.", inline=True)
    embed.add_field(
        name="Field 3", value="This is the 3rd inline field,", inline=False)
    embed.set_image(url="https://i.stack.imgur.com/8xAac.png")
    embed.set_thumbnail(url="https://i.stack.imgur.com/8xAac.png")
    embed.set_author(name="Author's name", icon_url=bot.user.avatar_url)
    embed.set_footer(text="This is a footer", icon_url=bot.user.avatar_url)
    embed.timestamp = datetime.utcnow()
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.orange()
    )
    test_e.set_author(name="Le prefix du bot est = u!")
    test_e.add_field(name="Commandes", value="Help, serveurinfo, coucou, say", inline=False)
    test_e.add_field(name="Commandes Musique", value="Soon... les commandes musique. Soon... :o", inline=False)
    test_e.add_field(name="Commandes Alliance", value="guide, pack", inline=False)
    test_e.add_field(name="Autres...", value="covid (pays)", inline=False)
    test_e.add_field(name="Commandes Modération", value="mute, unmute, ban, unban, kick, clear ..., ")
    test_e.add_field(name="Info", value="Bêta 0.1_DYB", inline=False)
    test_e.set_footer(text="YoRHa", icon_url=bot.user.avatar_url)
    test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
    test_e.set_thumbnail(url = "https://i.imgur.com/QQ2w7CK.png")
    await ctx.send(embed=test_e)

@bot.event
async def on_ready():
    print("Je suis prêt")

@bot.command()
async def coucou(ctx):
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.orange()
    )
    test_e.set_author(name="salut")
    await ctx.send(embed=test_e)

@bot.command(pass_context=True)
async def serveurinfo(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    serverDescription = server.description
    numberOfPerson = server.member_count
    serverName = server.name
    author = ctx.message.author
    
    test_e = discord.Embed(
        colour=discord.Colour.blurple()
    )
    test_e.add_field(name="Nom du serveur :", value= f"{serverName}", inline=False)
    test_e.add_field(name="Nombre de salons :", value= f"Il y'a {numberOfVoiceChannels} salons vocaux et {numberOfTextChannels} salons textuels", inline=False)
    test_e.add_field(name="Membres :", value= f"Ce serveur possède {numberOfPerson} membres", inline=False)
    test_e.add_field(name="Description de serveur (si il y'en a)", value= f"{serverDescription}", inline=False)
    test_e.set_footer(text="YoRHa", icon_url=bot.user.avatar_url)
    test_e.set_thumbnail(url = "https://i.imgur.com/EMw71zI.png")
    test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
    await ctx.send(embed=test_e)

@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, nombre : int):
    messages = await ctx.channel.history(limit = nombre + 1).flatten()
    for message in messages:
        await message.delete()

@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.ban(user, reason = reason)
    await ctx.send(f"{user} à été ban car : {reason}.")

@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, user, *reason):
    reason = " ".join(reason)
    userName, userId = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userId:
            await ctx.guild.unban(i.user, reason = reason)
            await ctx.send(f"{user} à été débanni du serveur.")
            return
    await ctx.send(f"L'utilisateur {user} n'a pas été ban")

@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.gold()
    )
    test_e.add_field(name=f"{user} a été kick du serveur par {author}", value=f"Raison : {reason}")
    test_e.set_footer(text="YoRHa", icon_url=bot.user.avatar_url)
    test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
    test_e.set_thumbnail(url = "https://i.imgur.com/APyQzZX.png")
    await ctx.guild.kick(user, reason = reason)
    await ctx.send(embed=test_e)

@bot.command(case_insensitive=True)
async def say(ctx, saymsg=None):
    if saymsg==None:
        return await ctx.send("Merci d'écrire la phrase dont vous voulez que le bot répète")
     
    sayEmbed = discord.Embed(title=f"{ctx.author.name} a envoyé :", color = discord.Color.blue(), description=f"{saymsg}")
    sayEmbed.timestamp = ctx.message.created_at
    
    await ctx.send(embed = sayEmbed)

#@bot.command()
#async def ukraineinfo(ctx):
#    author = ctx.message.author
#
#    test_e = discord.Embed(
#        colour=discord.Colour.gold()
#    )
#    test_e.add_field(name="Informations relatives à l'Ukraine", value=":flag_ua: | L'Ukraine est un Pays Libre. Elle possède ses règles, ses choix et ne prend exemple sur personne. Pour être un pays UNIQUE ! L'Ukraine fait parti de l'alliance de la YoHRa ! Une alliance LIBRE, FIER et PROTECTRICE. Si tu es nouveau dans le pays, je t'invite à executer la commande | u!nouveau | ", inline=False)
#    test_e.set_footer(text="Cordialement : Gérant des informations d'Ukraine", icon_url=bot.user.avatar_url)
#    test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
#    await ctx.send(embed=test_e)

#@bot.command()
#async def nouveau(ctx):
#    author = ctx.message.author
#
#    test_e = discord.Embed(
#        colour=discord.Colour.gold()
#    )
#    test_e.add_field(name="Informations pour les nouveaux", value=":flag_ua: | Bienvenue en Ukraine !  ", inline=False)
#    test_e.add_field(name="Petite synthèse", value=" Tu es désormais soumis aux règles en Ukraine ! Mais pas d'inquiétude, car en effet nous ne sommes pas très strict. Le but en Ukraine c'est que les membres soient librent de leurs choix. Tu n'auras donc pas tant à t'inquiéter. Je t'invite à prendre contact avec le Leader de l'Ukraine (Exoflix) ou avec un officier. Notre but, c'est de t'intégrer un maximum dans le serveur. Aucun membre ne doit être délaissé. Tout le monde a une place importante dans le serveur !  ", inline=False)
#    test_e.add_field(name="Voici le Guide officiel de l'alliance qui t'aidera tout le long de ton aventure :", value="http://myreader.toile-libre.org/uploads/My_5ff48d12a2e20.pdf")
#    test_e.set_footer(text="YoRHa", icon_url=bot.user.avatar_url)
#    test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
#    test_e.set_thumbnail(url = "https://i.imgur.com/839jIs2.png")
#    await ctx.send(embed=test_e)

@bot.command()
async def guide(ctx):
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.blue()
    )
    test_e.add_field(name="Guide de l'alliance", value="**Guide non mis à jour**, il se peut que certains craft où autre solutions ne soient plus à jour...", inline=False)
    test_e.add_field(name="Adresse du Guide :", value="http://myreader.toile-libre.org/uploads/My_5ff48d12a2e20.pdf")
    test_e.set_footer(text="YoRHa", icon_url=bot.user.avatar_url)
    test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
    await ctx.send(embed=test_e)

@bot.command()
async def pack(ctx):
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.blue()
    )
    test_e.add_field(name="Pack officiel d'alliance : YoHRa", value="Ce pack a été développé Langou (ancien Suprême Leader YoRHa). Le pack est vérifié et complètement sécurisé. (Attention quand vous téléchagez des packs, pensez bien à toujours vérifié la source :upside_down:", inline=False)
    test_e.add_field(name="Adresse du Pack :", value="https://www.mediafire.com/file/z1r1nxd4q5nubne/YoRHa+Pack+16x16+NoLag.rar/file")
    test_e.set_footer(text="YoRHa", icon_url=bot.user.avatar_url)
    test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
    await ctx.send(embed=test_e)

#@bot.command(pass_context=True)
#async def infoserveur(ctx):
#	server = ctx.guild
#	numberOfTextChannels = len(server.text_channels)
#	numberOfVoiceChannels = len(server.voice_channels)
#	serverDescription = server.description
#	numberOfPerson = server.member_count
#	serverName = server.name
#	author = ctx.message.author
#   
#    test_e = discord.Embed(
#        colour=discord.Colour.blue()
#    )
#    test_e.add_field(name="Nom du serveur", value=f"{serverName}", inline=False)
#    test_e.add_field(name="Nombre de salons textuels", value=f"{numberOfTextChannels}", inline=False)
#    test_e.add_field(name="Nombre de salons vocals", value=f"{numberOfVoiceChannels}")
#    test_e.add_field(name="Description de serveur", value=f"{serverDescription}", inline=False)
#    test_e.add_field(name="Nombre de Personnes dans le serveur", value=f"{numberOfPerson}")
#    test_e.set_footer(text="Cordialement : Gérant des informations d'Ukraine", icon_url=bot.user.avatar_url)
#    test_e.set_thumbnail(url = "https://i.imgur.com/EMw71zI.png")
#    test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
#    await ctx.send(embed=test_e)

#https://i.imgur.com/EMw71zI.png

@bot.command()
async def avatar(self, ctx, member : discord.Member = None):

        if member is None:
            embed = discord.Embed(title="Pour utiliser la commande, veuillez procéder comme suit : ```+avatar [member]```", colour=0xff0000, timestamp=ctx.message.created_at)
            await ctx.send(embed=embed)
            return

        else:
            embed2 = discord.Embed(title=f"{member}'s Avatar!", colour=0x0000ff, timestamp=ctx.message.created_at)
            embed2.add_field(name="Animated?", value=member.is_avatar_animated())
            embed2.set_image(url=member.avatar_url)
            await ctx.send(embed=embed2)

@bot.command()
async def covid(ctx, *, countryName = None):
    try:
        if countryName is None:
            embed = discord.Embed(title="Merci d'écrire la commande de cette façon ```u!covid (nom du pays)```", colour=0xff0000)
            await ctx.send(embed=embed)


        else:
            url = f"https://coronavirus-19-api.herokuapp.com/countries/{countryName}"
            stats = requests.get(url)
            json_stats = stats.json()
            country = json_stats["country"]
            totalCases = json_stats["cases"]
            todayCases = json_stats["todayCases"]
            totalDeaths = json_stats["deaths"]
            todayDeaths = json_stats["todayDeaths"]
            recovered = json_stats["recovered"]
            active = json_stats["active"]
            critical = json_stats["critical"]
            casesPerOneMillion = json_stats["casesPerOneMillion"]
            deathsPerOneMillion = json_stats["deathsPerOneMillion"]
            totalTests = json_stats["totalTests"]
            testsPerOneMillion = json_stats["testsPerOneMillion"]

            embed2 = discord.Embed(title=f"**Statut du Covid-19 dans le pays : {country}**!", description="Cette commande n'est pas actualisé en direct ! Ne tenez donc pas forcément comptes des chiffres exact.", colour=0x0000ff, timestamp=ctx.message.created_at)
            embed2.add_field(name="**Cas Total**", value=totalCases, inline=True)
            embed2.add_field(name="**Nouveaux cas**", value=todayCases, inline=True)
            embed2.add_field(name="**Morts**", value=totalDeaths, inline=True)
            embed2.add_field(name="**Personnes mortes aujourd'hui**", value=todayDeaths, inline=True)
            embed2.add_field(name="**Guéries**", value=recovered, inline=True)
            embed2.add_field(name="**Cas actifs**", value=active, inline=True)
            embed2.add_field(name="**Cas critiques**", value=critical, inline=True)
            embed2.add_field(name="**Cas pour 1M d'habitants**", value=casesPerOneMillion, inline=True)
            embed2.add_field(name="**Morts pour 1M d'habitants**", value=deathsPerOneMillion, inline=True)
            embed2.add_field(name="**Habitants testés**", value=totalTests, inline=True)
            embed2.add_field(name="**Tests pour 1M d'habitants**", value=testsPerOneMillion, inline=True)

            embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/564520348821749766/701422183217365052/2Q.png")
            await ctx.send(embed=embed2)

    except:
        embed3 = discord.Embed(title="Nom de pays invalide ! Merci de réessayer... (écrire le nom du pays que vous souhaiter entrée en **Anglais**", colour=0xff0000)
        embed3.set_author(name="Erreur !")
        await ctx.send(embed=embed3)

@bot.command()
async def pays(ctx):
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.orange()
    )
    test_e.add_field(name="Liste des pays de l'alliance", value="Aucune donnée d'entrée pour le moment... En attente de la liste officiel des pays faisant partie de l'alliance . . .", inline=False)
    await ctx.send(embed=test_e)


bot.run("ODkzMTgwNzQxMzk4MTg4MDgz.YVXtYw.zSLAAGhT2BGE0gZZP7Yy8Yu1Gf4")
