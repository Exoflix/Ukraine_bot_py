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
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a ??t?? renseign??"):
    mutedRole = await getMutedRole(ctx)
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.magenta()
    )
    test_e.add_field(name=f"{member.name} a ??t?? mute !", value="Merci de ne pas le mentionner durant son mute")
    test_e.set_footer(text="YoRHa", icon_url=bot.user.avatar_url)
    test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
    test_e.set_thumbnail(url = "https://i.imgur.com/sOHZQZI.png")
    await ctx.send(embed=test_e)
    await member.add_roles(mutedRole, reason = reason)

@bot.command()
@commands.has_permissions(kick_members = True)
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a ??t?? renseign??"):
    mutedRole = await getMutedRole(ctx)
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.magenta()
    )
    test_e.add_field(name=f"{member.name} a ??t?? unmute !", value="Ne refait pas la m??me b??tise", inline=False)
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
	await ctx.send("La vid??o est r??p??t?? ind??finiment")

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
    test_e.set_author(name="Le prefix du bot est = y!")
    test_e.add_field(name="Commandes", value="Help, serveurinfo, coucou, say", inline=False)
    test_e.add_field(name="Commandes Musique", value="Ajouter le bot musique YoRHa (indisponible pour le moment)", inline=False)
    test_e.add_field(name="Commandes Alliance", value="guide, pack, pays, reunion, resume, probleme", inline=False)
    test_e.add_field(name="Autres...", value="covid (pays), avatar", inline=False)
    test_e.add_field(name="Commandes Mod??ration", value="mute, unmute, ban, unban, kick, clear ..., ")
    test_e.add_field(name="y!ally", value="Voir le post forum de l'alliance !")
    test_e.add_field(name="Annonces importantes :", value="***Ne cliquez pas sur les liens comme un site pr??tendant ??tre un site de notre alliance si vous tenez ?? ne pas vous faire hack (IP Logger, etc.***")
    test_e.add_field(name="Bot", value="Version : 0.8_DYBot | Mise ?? jour le 10/10/21 ?? 12h01", inline=False)
    test_e.set_footer(text="YoRHa", icon_url=bot.user.avatar_url)
    test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
    test_e.set_thumbnail(url = "https://i.imgur.com/QQ2w7CK.png")
    await ctx.send(embed=test_e)

@bot.event
async def on_ready():
    print("Je suis pr??t")

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
    test_e.add_field(name="Membres :", value= f"Ce serveur poss??de {numberOfPerson} membres", inline=False)
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
    await ctx.send(f"{user} ?? ??t?? ban car : {reason}.")

@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, user, *reason):
    reason = " ".join(reason)
    userName, userId = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userId:
            await ctx.guild.unban(i.user, reason = reason)
            await ctx.send(f"{user} ?? ??t?? d??banni du serveur.")
            return
    await ctx.send(f"L'utilisateur {user} n'a pas ??t?? ban")

@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.gold()
    )
    test_e.add_field(name=f"{user} a ??t?? kick du serveur par {author}", value=f"Raison : {reason}")
    test_e.set_footer(text="YoRHa", icon_url=bot.user.avatar_url)
    test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
    test_e.set_thumbnail(url = "https://i.imgur.com/APyQzZX.png")
    await ctx.guild.kick(user, reason = reason)
    await ctx.send(embed=test_e)

@bot.command(case_insensitive=True)
async def say(ctx, saymsg=None):
    if saymsg==None:
        return await ctx.send("Merci d'??crire la phrase dont vous voulez que le bot r??p??te")
     
    sayEmbed = discord.Embed(title=f"{ctx.author.name} a envoy?? :", color = discord.Color.blue(), description=f"{saymsg}")
    sayEmbed.timestamp = ctx.message.created_at
    
    await ctx.send(embed = sayEmbed)

#@bot.command()
#async def ukraineinfo(ctx):
#    author = ctx.message.author
#
#    test_e = discord.Embed(
#        colour=discord.Colour.gold()
#    )
#    test_e.add_field(name="Informations relatives ?? l'Ukraine", value=":flag_ua: | L'Ukraine est un Pays Libre. Elle poss??de ses r??gles, ses choix et ne prend exemple sur personne. Pour ??tre un pays UNIQUE ! L'Ukraine fait parti de l'alliance de la YoHRa ! Une alliance LIBRE, FIER et PROTECTRICE. Si tu es nouveau dans le pays, je t'invite ?? executer la commande | u!nouveau | ", inline=False)
#    test_e.set_footer(text="Cordialement : G??rant des informations d'Ukraine", icon_url=bot.user.avatar_url)
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
#    test_e.add_field(name="Petite synth??se", value=" Tu es d??sormais soumis aux r??gles en Ukraine ! Mais pas d'inqui??tude, car en effet nous ne sommes pas tr??s strict. Le but en Ukraine c'est que les membres soient librent de leurs choix. Tu n'auras donc pas tant ?? t'inqui??ter. Je t'invite ?? prendre contact avec le Leader de l'Ukraine (Exoflix) ou avec un officier. Notre but, c'est de t'int??grer un maximum dans le serveur. Aucun membre ne doit ??tre d??laiss??. Tout le monde a une place importante dans le serveur !  ", inline=False)
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
    test_e.add_field(name="Guide de l'alliance", value="**Guide non ?? jour**, il se peut que certains craft o?? autre solutions ne soient plus ?? jour...", inline=False)
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
    test_e.add_field(name="Pack officiel d'alliance : YoRHa", value="Pack officiel de l'alliance (YoRHa). Le pack est v??rifi?? et est compl??tement s??curis??. Ce pack peut aider certains utilisateurs ?? r??duire les lags, parfait pour le PvP ! *(Attention quand vous t??l??chagez des packs, pensez bien ?? toujours v??rifi?? la source :upside_down:)*", inline=False)
    test_e.add_field(name="Adresse du Pack :", value="https://mega.nz/file/zktgXDxS#5wzwqYogIhtK96HF-z_z6tX2d2dfgi46aEdM2IZ3I7U")
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
#    test_e.set_footer(text="Cordialement : G??rant des informations d'Ukraine", icon_url=bot.user.avatar_url)
#    test_e.set_thumbnail(url = "https://i.imgur.com/EMw71zI.png")
#    test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
#    await ctx.send(embed=test_e)

#https://i.imgur.com/EMw71zI.png

@bot.command()
async def covid(ctx, *, countryName = None):
    try:
        if countryName is None:
            embed = discord.Embed(title="Merci d'??crire la commande de cette fa??on ```u!covid (nom du pays)```", colour=0xff0000)
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

            embed2 = discord.Embed(title=f"**Statut du Covid-19 dans le pays : {country}**!", description="Cette commande n'est pas actualis?? en direct ! Ne tenez donc pas forc??ment comptes des chiffres exact.", colour=0x0000ff, timestamp=ctx.message.created_at)
            embed2.add_field(name="**Cas Total**", value=totalCases, inline=True)
            embed2.add_field(name="**Nouveaux cas**", value=todayCases, inline=True)
            embed2.add_field(name="**Morts**", value=totalDeaths, inline=True)
            embed2.add_field(name="**Personnes mortes aujourd'hui**", value=todayDeaths, inline=True)
            embed2.add_field(name="**Gu??ries**", value=recovered, inline=True)
            embed2.add_field(name="**Cas actifs**", value=active, inline=True)
            embed2.add_field(name="**Cas critiques**", value=critical, inline=True)
            embed2.add_field(name="**Cas pour 1M d'habitants**", value=casesPerOneMillion, inline=True)
            embed2.add_field(name="**Morts pour 1M d'habitants**", value=deathsPerOneMillion, inline=True)
            embed2.add_field(name="**Habitants test??s**", value=totalTests, inline=True)
            embed2.add_field(name="**Tests pour 1M d'habitants**", value=testsPerOneMillion, inline=True)

            embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/564520348821749766/701422183217365052/2Q.png")
            await ctx.send(embed=embed2)

    except:
        embed3 = discord.Embed(title="Nom de pays invalide ! Merci de r??essayer... (??crire le nom du pays que vous souhaiter entr??e en **Anglais**", colour=0xff0000)
        embed3.set_author(name="Erreur !")
        await ctx.send(embed=embed3)

@bot.command()
async def pays(ctx):
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.orange()
    )
    test_e.add_field(name="Liste des pays de l'alliance", value=":flag_ir: Iran, :flag_us: ??tats-Unis, :flag_bs: Bahamas, :flag_ca: Canada, :flag_gt: Guatemala, :flag_mt: Malte, :flag_ph: Philippines, :flag_pr: Porto Rico, :flag_white: Sakhaline, :flag_th: Tha??lande, :flag_ua: Ukraine, :flag_bt: Bhoutan, :flag_gy: Guyana, :flag_tt: Trinit??-et-tobago, :flag_ve: Venezuela, :flag_re: La R??union, :flag_cf: Centre-Afrique, :flag_br: Br??sil, :flag_gf: Guyane, :flag_ug: Ouganda, :flag_tw: Ta??wan", inline=False)
    test_e.add_field(name="Info :", value="*Si votre pays ne figure pas dans la liste ci-dessus, merci de contacter Exoflix / Cr??meBr??l??e pour demander l'ajout de celui-ci.*", inline=False)
    test_e.set_footer(text="YoRHa", icon_url=bot.user.avatar_url)
    test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
    await ctx.send(embed=test_e)

@bot.command()
async def maj(ctx):
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.blurple()
    )
    test_e.add_field(name="Mise ?? jour du 11/10/21 ", value="Ajout de la commande ***y!pays*** permettant de voir la liste officiel des pays de l'alliance", inline=False)
    await ctx.send(embed=test_e)


@bot.command()
async def ally(ctx):
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.blue()
    )
    test_e.add_field(name="Adresse du post forum de l'alliance :", value="https://nationsglory.fr/forums/thread/yorha.2025")
    test_e.set_footer(text="YoRHa", icon_url=bot.user.avatar_url)
    test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
    await ctx.send(embed=test_e)

#@bot.command()
#async def mp(ctx, *, args=None):
#	if args !=None:
#		members = ctx.guild.members
#		author = ctx.message.author
#
#    			test_e = discord.Embed(
#        		    colour=discord.Colour.blue()
#    			)
#		for member in members:
#			try:
#				test_e.add_field(name="Erreur :", value=(args))
#    				test_e.set_footer(text="YoRHa", icon_url=bot.user.avatar_url)
#    				test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
#				await ctx.send(embed=test_e)
#			except:
#				print("Es-tu s??r d'avoir bien taper la commande ????")
#	else:
#		test_e.add_field(name="Erreur :", value="Merci d'??crire ce que tu veux que j'envoie ?? tout les membres de ce serveur :Issouserious:")
#		test_e.set_footer(text="YoRHa", icon_url=bot.user.avatar_url)
#    		test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
#		await ctx.send(embed=test_e)

@bot.command()
async def avatar(ctx, member: discord.Member=None):
    if member == None:
        member = ctx.author
    
    icon_url = member.avatar_url 
 
    avatarEmbed = discord.Embed(title = f"Voici l'avatar de {member.name}", color = 0xFFA500)
 
    avatarEmbed.set_image(url = f"{icon_url}")
 
    avatarEmbed.timestamp = ctx.message.created_at 
 
    avatarEmbed.set_footer(text="YoRHa", icon_url=bot.user.avatar_url)

    await ctx.send(embed = avatarEmbed)
		
@bot.command()
@commands.has_permissions(manage_messages = True)
async def marchepas(ctx):
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.blue()
    )
    test_e.add_field(name="R??sum?? de la r??union du 09/10", value="Reprise de l???activit?? de l???alliance Pink. Soyez solidaire, et entraidez-vous.Mobilisez-vous !")
    test_e.add_field(name="Strat??gie :", value="Chercher et exterminer les pays build et pays farm afin d???affaiblir l???ennemi en terme de stuff : France, Indon??sie, Russie etc.")
    test_e.add_field(name=":arrow_lower_right:", value="Sortez avec un bon stuff, pas non plus votre stuff le plus puissant, la r??gle principal ??tant de ne pas risquer de drop des trucs cher face ?? l???ennemi. L???erreur serait grande de les fournir en stuff???")
    test_e.add_field(name=":comet:", value="Si vous avez des ali??s d???autres serveurs, de bon joueurs en PVP, BUILD, FARM??? Convainquez-les de nous rejoindre. Plus l???unit?? grandis et plus on devient puissant. On vous rappel que ce n???est pas le nombre qui fait la victoire, mais la capacit?? de tout le monde ?? pr??server cette unit?? pour pouvoir vaincre.")
    test_e.add_field(name="Organisation :", value="Partagez-vous vos stuff : missiles, ressources, outils etc. Il n???y a aucune utilit?? ?? garder quelque chose que vous n???utilisez ou n???utiliserez jamais.")
    test_e.add_field(name="Nos ennemis :", value="Dans l???alliance adverses, aucune unit??. Leur puissance r??side dans la peur et les int??r??ts qu???ils ont les un envers les autres. Une petite erreur et leur alliance s???effondre tel l???URSS")
    test_e.add_field(name="Nombre de personnes pr??sentes ?? la r??union :", value="Pointe ?? 26 personnes pr??sentes ?? la r??union dont les Hauts Grad??s Sam12 et TheSpeeding. Un grand Merci aux membres qui ont ??t?? pr??sents lors de la r??union du Samedi 09 Octobre 2021")
    test_e.add_field(name="Petite phrase d'accroche :", value="N'oubliez jamais que la YoRHa est une alliance fond?? dans l'unit?? et la confiance entre tout ses membres !")
    test_e.set_footer(text="YoRHa", icon_url=bot.user.avatar_url)
    test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
    await ctx.send(embed=test_e)

#@bot.command()
#async def dm(ctx, user_id=None, *, args=None):
#    if user_id != None and args != None:
#        try:
#            target = await bot.fetch_user(user_id)
#            await target.send(args)
#
#            await ctx.channel.send("'" + args + "' envoy?? ?? : " + target.name)
#
#        except:
#            await ctx.channel.send("Je ne peux pas envoyer de message priv?? ?? cet utilisateur")
#        
#
#    else:
#        await ctx.channel.send("Aucun nom d'utilisateur et / ou message donn??")

@bot.command(aliases=["dmall"]) # You can add more aliases here
async def send(ctx, *, args:str=None):
	if args.strip() == None or args.strip() == "":
		return
	else:
		if log_dms.strip().lower() in ["on","enabled","true","enable"]:
			member_count = 0
			for member in ctx.guild.members:
				member_count += 1
			await ctx.send(f"{member_count} membres d??tect??s, cette op??ration peut durer un petit moment")
			for member in ctx.guild.members:
				if member == client.user:
					await ctx.send(f":x: {member.name} c'est vous, vous ne pouvez pas vous envoyer de message ?? vous m??mes")
					member_count -= 1
					pass
				elif member.bot == True:
					await ctx.send(f":x: {member.name} c'est un bot, vous ne pouvez pas envoyer de message ?? un bot")
					member_count -= 1
					pass
				else:
					try:
						await member.send(args.strip())
						await ctx.send(f":white_check_mark: Message envoy?? ?? {member.name}")
						await asyncio.sleep(delay)
					except discord.errors.Forbidden:
						await ctx.send(f":white_check_mark: Je ne peux pas envoyer de messages ?? {member.name}, probably DMs off")
						member_count -= 1
						pass
					except commands.CommandInvokeError:
						await ctx.send(f":x: Je ne peux pas envoyer de message ?? {member.name}, ce membre a s??rement d??sactiv?? ses mp")
						member_count -= 1
						pass
			await ctx.send(f":white_check_mark: Message priv?? envoy?? ?? {member_count} membres")
			return
		else:
			member_count = 0
			for member in ctx.guild.members:
				member_count += 1
			await ctx.send(f"{member_count} membres d??tect??, cette op??ration peut durer un peu de temps")
			for member in ctx.guild.members:
				if member == client.user or member.bot == True:
					member_count -= 1
					pass
				else:
					try:
						await member.send(args.strip())
						await asyncio.sleep(delay)
					except discord.errors.Forbidden:
						member_count -= 1
						pass
					except commands.CommandInvokeError:
						member_count -= 1
						pass

			await ctx.send(f":white_check_mark: Message priv?? envoy?? ?? {member_count} membres")
			return

@bot.command()
async def probleme(ctx):
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.red()
    )
    test_e.add_field(name="Probl??me(s) remont??es au sein de l'alliance :", value="Le Canada :flag_ca: aimerais join assaut plus souvent. (se sent rejeter)", inline=False)
    test_e.add_field(name="Rappel :", value="Si vous avez des soucis ?? faire remonter aux hauts grad??s de l'alliance, mentionner un membre des Officiers Fondateurs de l'alliance afin que votre probl??me soit ??tudi?? et qu'une solution soit trouv?? !", inline=False)
    test_e.set_footer(text="YoRHa", icon_url=bot.user.avatar_url)
    test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
    await ctx.send(embed=test_e)

@bot.command()
async def reunion(ctx):
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.red()
    )
    test_e.add_field(name="Date de la prochaine r??union :", value="Aucune r??union n'est pr??vu ?? ce jour...", inline=False)
    test_e.set_footer(text="YoRHa", icon_url=bot.user.avatar_url)
    test_e.set_author(name=f"{author}", icon_url=author.avatar_url)
    await ctx.send(embed=test_e)

bot.run("ODkzMTgwNzQxMzk4MTg4MDgz.YVXtYw.4P0bcslNpzSc_C2U6EfDfXrnx8U")
