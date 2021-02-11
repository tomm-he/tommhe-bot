import requests as r
import discord,asyncio
from discord.ext import commands
from bs4 import BeautifulSoup as bs
import random
import datetime

names = []

List= ["``Please Enter Team 1``","``Please Enter Team 2``","``Grabbing links...``"]


def perms():
	def predicate(ctx):
		return ctx.message.author.id == 552583557277679617
	return commands.check(predicate)
	
def get_names():
	get_page = r.get(f"https://www.nbastreams100.com/")
	html_data = get_page.text

	soup = bs(html_data,"html.parser")
	
	for n in soup.find_all(["h2"]):
		if n.text.strip() not in names:
			names.append(n.text.strip())
		else:
			pass
			
	get_page2 = r.get(f"https://www.nbastreams100.com/page/2/")
	html_data2 = get_page2.text

	soup2 = bs(html_data2,"html.parser")
	
	for y in soup2.find_all(["h2"]):
		if y.text.strip() not in names:
			names.append(y.text.strip())
		else:
			pass
	
	
		
class send_names(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		
		
	@commands.command()
	async def nbanames(self,ctx):
		async with ctx.typing():
			get_names()
		em = discord.Embed(color=random.randint(0, 0xFFFFFF))
		em.set_author(name= "Click To Invite Me To Your Server!",url= "https://discord.com/api/oauth2/authorize?client_id=594663400143847424&permissions=469854295&scope=bot", icon_url=self.bot.user.avatar_url)
		em.timestamp = datetime.datetime.utcnow()
		em.set_footer(text= f"Requested By: {ctx.author.name}#{ctx.author.discriminator} • !nbanames", icon_url=f"{ctx.author.avatar_url}")
		em.description = f'Make Sure To Copy The Exact Names Below```'+"\n".join(names)+'```'
		await ctx.send(embed=em)
		await ctx.message.delete()
		names.clear()
	
		
	


def setup(bot):
	bot.add_cog(send_names(bot))