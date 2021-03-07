import requests as r
import re,discord,asyncio,random
from discord.ext import commands
from bs4 import BeautifulSoup as bs
import datetime

links = []

List= ["``Please Enter Team 1``","``Please Enter Team 2``","``Grabbing links...``"]

def perms():
	def predicate(ctx):
		return ctx.message.author.id == 552583557277679617
	return commands.check(predicate)
def get_links(Link):
	get_page = r.get(f"https://stream.streams100.net/event/{Link}")
	html_data = get_page.text

	soup = bs(html_data,"html.parser")
	
	#print(soup.prettify())

	discord = soup.find("a",href=re.compile('https://discord\.gg/gKqEYyr'))

	if discord is not None:
		for link in discord.find_all_next('a',attrs={"target": "_blank"}):
			a = link.get('href')
			if a not in links:
				links.append(a)
			else:
				pass
	else:
		print("fail")
		
class send_links(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		
	@commands.command(pass_context = True)
	async def match(self,ctx):
		def delete(m):
			return m.author == ctx.author or m.content in List
		def correct(m):
			return m.author == ctx.author
		await ctx.reply("``Please Enter Team 1``", delete_after=600, mention_author=True)
		channel = ctx.message.channel
		try:
			team_1 = (await self.bot.wait_for("message",check = correct,timeout=120.0))
			team1 = str(team_1.content).replace(" ","-")
			await ctx.reply("``Please Enter Team 2``", delete_after=600, mention_author=True)
			team_2 = (await self.bot.wait_for("message",check=correct,timeout=120.0))
			team2 = str(team_2.content).replace(" ","-")
			await ctx.reply("``Grabbing links...``", delete_after=600, mention_author=True)
		except asyncio.TimeoutError:
			return await ctx.send("Request Timed Out", delete_after=600)
		link_part_1 = (f"{team1}-vs-{team2}-match-preview/")
		link_part_2 = (f"{team2}-vs-{team1}-match-preview/")

		#await ctx.send(link_part_1)
		#await ctx.send(link_part_2)
		url_1 = r.get(f"https://stream.streams100.net/event/{link_part_1}")
		url_2 = r.get(f"https://stream.streams100.net/event/{link_part_2}")
		#await ctx.send(url_1)
		#await ctx.send(url_2)
		print(url_1.request.url)
		print(url_2.request.url)
		if url_1.request.url != "https://soccerstreams-100.com":
			get_links(link_part_1)
		if url_2.request.url != "https://soccerstreams-100.com":
			get_links(link_part_2)
		i = 0
		digit = random.randint(10,17)
	#	message = ('\n'.join(map(str, links)))
		select = []
		if links != []:
			with ctx.typing():
				#for send in links:
				#	if i < digit:
				selected_links = links[0:digit]
				message = ('\n'.join(map(str, selected_links)))
				embed = discord.Embed(title = f"{team1} v {team2} \u26BD", color=random.randint(0, 0xFFFFFF))
				embed.set_author(name= "Click To Invite Me To Your Server!",url= "https://discord.com/api/oauth2/authorize?client_id=594663400143847424&permissions=469854295&scope=bot", icon_url=self.bot.user.avatar_url)
				embed.add_field(name= "\u200b",value= message ,inline=True)
				embed.timestamp = datetime.datetime.utcnow()
				embed.set_footer(text= f"Requested By: {ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.avatar_url}")
				await ctx.reply(embed=embed, mention_author=True)
				await channel.purge(limit=6, check = delete, bulk = True)
				i += 1
				links.clear()
				        
		else:
		    m = discord.Embed(color=random.randint(0, 0xFFFFFF))
		    m.description = f"{ctx.author.mention} • **Failed to fetch links** - The Request ``{team1} | {team2}`` Was Wrong and i Could Not Understand Which Game You Wanted To Grab. \n\n*Summon The Command* ``!names`` *To Get a List Of All Matches Available and The Correct Team Names* and/or ``!matchhelp`` *To Get a Detailed Description Of The Module* \n \n``Please Note, To Not Use Pronunciation As The Bot Wont Understand That, Example = [Atlético Madrid (false) = Atletico Madrid (correct)]``"
		    m = await ctx.reply(embed=m, mention_author=True)
		    await channel.purge(limit=6, check = delete, bulk = True)
		    
					
            
			
			
			
			
def setup(bot):
	bot.add_cog(send_links(bot))
