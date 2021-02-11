import requests as r
from bs4 import BeautifulSoup as bs
import re
import discord,asyncio,random
from discord.ext import commands
import datetime
links = []
List= ["``Please Enter Team 1``","``Please Enter Team 2``","``Grabbing links...``"]


def get_links(Link):
	get_page = r.get(f"https://www.nhlstreams100.com/{Link}")
	html_data = get_page.text

	soup = bs(html_data,"html.parser")
	
	#print(soup.prettify())

	
	discord = soup.find("a",href=re.compile('https://discord.gg/hhvRKsr'))
	#print(n)
	if discord is not None:
		for link in discord.find_all_next('a',attrs={"target": "_blank"}):
			a = link.get('href')
			if a not in links:
				links.append(a)
			else:
				pass
	else:
		print("fail")


class nfl(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		
	@commands.command(pass_context = True)
	async def nhl(self,ctx):
		def delete(m):
			return m.author == ctx.author or m.content in List
		def correct(m):
			return m.author == ctx.author
		await ctx.send("``Please Enter Team 1``")
		channel = ctx.message.channel
		try:
			team_1 = (await self.bot.wait_for("message",check = correct,timeout=120.0))
			team1 = str(team_1.content).replace(" ","-")
			await ctx.send("``Please Enter Team 2``")
			team_2 = (await self.bot.wait_for("message",check=correct,timeout=120.0))
			team2 = str(team_2.content).replace(" ","-")
			await ctx.send("``Grabbing links...``")
		except asyncio.TimeoutError:
			return await ctx.send("Request Timed Out")
		link_part_1 = (f"{team1}-at-{team2}-live-stream/")
		link_part_2 = (f"{team2}-at-{team1}-live-stream/")

		#await ctx.send(link_part_1)
		#await ctx.send(link_part_2)
		url_1 = r.get(f"https://www.nhlstreams100.com/{link_part_1}")
		url_2 = r.get(f"https://www.nhlstreams100.com/{link_part_2}")
		#await ctx.send(url_1)
		#await ctx.send(url_2)
		print(url_1.request.url)
		print(url_2.request.url)
		if url_1.request.url != "https://www.nhlstreams100.com":
			get_links(link_part_1)
		if url_2.request.url != "https://www.nhlstreams100.com":
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
				embed = discord.Embed(title = f"{team1} v {team2} :hockey: ", color=random.randint(0, 0xFFFFFF))
				embed.set_author(name= "Click To Invite Me To Your Server!",url= "https://discord.com/api/oauth2/authorize?client_id=594663400143847424&permissions=469854295&scope=bot", icon_url=self.bot.user.avatar_url)
				embed.add_field(name= "\u200b",value= message ,inline=True)
				embed.timestamp = datetime.datetime.utcnow()
				embed.set_footer(text= f"Requested By: {ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.avatar_url}")
				await ctx.send(embed=embed)
				await channel.purge(limit=7, check = delete, bulk = True)
				i += 1
				links.clear()
				        
		else:
		    await ctx.send("``Failed to fetch links`` - *Summon The Command* ``!nhlnames`` *To Get a List Of All Matches Available and The Correct Team Names* And/Or  Summon ``!nbahelp`` For Help")
		    await channel.purge(limit=7, check = delete, bulk = True)

def setup(bot):
        bot.add_cog(nfl(bot))