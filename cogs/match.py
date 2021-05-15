import requests as r
import re,discord,asyncio,random
from discord.ext import commands
from bs4 import BeautifulSoup as bs
import datetime
from disputils import BotEmbedPaginator

links = []

List= ["``Please Enter Team 1``","``Please Enter Team 2``","``Grabbing links...``"]

def perms():
	def predicate(ctx):
		return ctx.message.author.id == 552583557277679617
	return commands.check(predicate)
def get_links(Link):
	get_page = r.get(f"https://soccer.streamsgate.tv/event/{Link}")
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
		
	@commands.command()
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
            		await ctx.reply("``Please Enter Team 2``", delete_after=120.0, mention_author=True)
            		team_2 = (await self.bot.wait_for("message",check=correct,timeout=120.0))
            		team2 = str(team_2.content).replace(" ","-")
            		await ctx.reply("``Grabbing links...``", delete_after=600, mention_author=True)
        	except asyncio.TimeoutError:
            		return await ctx.send(f"{ctx.author.mention} Your ``{ctx.command.name}`` Request Has Timed Out, Please Use ``{ctx.prefix}streamhelp`` For More Information" , delete_after=600)

        	link_part_1 = (f"{team1}-vs-{team2}-match-preview/")
        	link_part_2 = (f"{team2}-vs-{team1}-match-preview/")

        	url_1 = requests.get(f"https://soccer.streamsgate.tv/event/{link_part_1}")
        	url_2 = requests.get(f"https://soccer.streamsgate.tv/event/{link_part_2}")

        	print(url_1.request.url)
        	print(url_2.request.url)

        	if url_1.request.url != "https://soccerstreams-100.com":
            		get_links(link_part_1)

        	if url_2.request.url != "https://soccerstreams-100.com":
            		get_links(link_part_2)

        	i = 0
        	select = []
        	if links != []:
            	await channel.purge(limit=7, check = delete, bulk = True)
            	stream = "http://liveonscore.tv"
            	matches = [i for i in links if stream in i]                                # sorting good streams to the top of the list
            	if matches:
                	[links.remove(i) for i in matches]
                	[links.insert(0,"**:white_check_mark: **" + i) for i in matches]
            	secondstream = "http://givemereddit"
            	results = [o for o in links if secondstream in o]
            	if results:
                	[links.remove(o) for o in results]
                	[links.insert(1, "**:white_check_mark: **" + o) for o in results]

            	selected_links1 = links[0:12]
            	message1 = ('\n'.join(map(str, selected_links1)))

            	selected_links2 = links[12:20]
            	message2 = ('\n'.join(map(str, selected_links2)))

            	embed1 = discord.Embed(title = f"{team1} v {team2} \u26BD *Beta*", color=random.randint(0, 0xFFFFFF))
            	embed1.set_author(name= "Click To Invite Me To Your Server!",url= "https://discord.com/api/oauth2/authorize?client_id=594663400143847424&permissions=469854295&scope=bot", icon_url=self.bot.user.avatar_url)
            	embed1.add_field(name= "\u200b",value= message1 ,inline=True)
            	embed1.timestamp = datetime.datetime.utcnow()
            	embed1.set_footer(text= f"Requested By: {ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.avatar_url}")

            	embeds = [embed1]
            	paginator = BotEmbedPaginator(ctx, embeds)

            	i += 1
            	links.clear()

            	if not selected_links2 == []:
                	embed2 = discord.Embed(title = f"{team1} v {team2} \u26BD *Beta*", color=random.randint(0, 0xFFFFFF))
                	embed2.set_author(name= "Click To Invite Me To Your Server!",url= "https://discord.com/api/oauth2/authorize?client_id=594663400143847424&permissions=469854295&scope=bot", icon_url=self.bot.user.avatar_url)
                	embed2.add_field(name= "\u200b",value= message2 ,inline=True)
                	embed2.timestamp = datetime.datetime.utcnow()
                	embed2.set_footer(text= f"Requested By: {ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.avatar_url}")
                	embeds.insert(1, embed2)

            	
		# success logging purposes, 
            	#e = discord.Embed(title='!match Command Used', colour=0xDE6246)
            	#e.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            	#e.description = f"{team1} v {team2} \n**By User:**\n{ctx.author.name}#{ctx.author.discriminator} | <@{ctx.author.id}>"
            	#e.timestamp = ctx.message.created_at
            	#if ctx.guild is not None:
                	#e.add_field(name='Server', value='{} (ID: {})'.format(ctx.guild.name, ctx.guild.id), inline=False)
                	#e.add_field(name='Channel', value='{} (ID: {}) {}'.format(ctx.channel, ctx.channel.id, ctx.channel.mention), inline=False)
            	#e.set_footer(text='Author ID: {}'.format(ctx.author.id))
            	#senderchannel = self.bot.get_channel(logging_channel_id) # <---
            	#await senderchannel.send(embed=e)
		
		await paginator.run()
            
        	else:
            		m = discord.Embed(color=random.randint(0, 0xFFFFFF))
            		m.description = f"{ctx.author.mention} • **Failed to fetch links** - The Request ``{team1} | {team2}`` Was Wrong and i Could Not Understand Which Game You Wanted To Grab. \n\n*Summon The Command* ``!names`` *To Get a List Of All Matches Available and The Correct Team Names* and/or ``!matchhelp`` *To Get a Detailed Description Of The Module* \n \n``Please Note, To Not Use Pronunciation As The Bot Wont Understand That, Example = [Atlético Madrid (false) = Atletico Madrid (correct)]``"
            		m = await ctx.reply(embed=m, mention_author=True)
            		await channel.purge(limit=6, check = delete, bulk = True)
            		print(f"{ctx.author} Failed a Match Command in: {ctx.guild} With The Keyword: {team1} | {team2}")
            		#m = discord.Embed(title='Failed Match Command', colour=0xDE6246)
            		#m.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            		#m.description = f"**Failed Keyword:**\n``{team1}`` | ``{team2}`` \n{ctx.author.name}#{ctx.author.discriminator} | <@{ctx.author.id}>"
            		#m.timestamp = ctx.message.created_at
            		#f ctx.guild is not None:
                		#m.add_field(name='Server', value='{} (ID: {})'.format(ctx.guild.name, ctx.guild.id), inline=False)
                		#m.add_field(name='Channel', value='{} (ID: {}) {}'.format(ctx.channel, ctx.channel.id, ctx.channel.mention), inline=False)
                		#m.set_footer(text='Author ID: {}'.format(ctx.author.id))
                		#ailchannel = self.bot.get_channel(logging_channel_id) # <---
                		#wait failchannel.send(embed=em)
		    
					
            
			
			
			
			
def setup(bot):
	bot.add_cog(send_links(bot))
