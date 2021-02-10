import discord
from discord.ext import commands
from os import listdir
from os.path import isfile
from os.path import isfile, join
import traceback
import random
import asyncio
import os
import sqlite3
from discord.utils import find
import datetime
import time
from discord.ext import commands

cogs_dir = "cogs"




def get_prefix(bot, message):
    if not message.guild:
        return "!"
    prefix = bot.cur.execute(f"SELECT prefix FROM prefix WHERE guild = {message.guild.id}").fetchall()
    if prefix == []:
        return "!"
    return prefix[0]
    
  
bot = commands.Bot(command_prefix=get_prefix)

bot.con = sqlite3.connect('sqlite.db')

bot.cur = bot.con.cursor()
		
bot.remove_command("help")
@bot.event
async def on_ready():
        await bot.change_presence(status=discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.watching,name=f"{len(bot.guilds)} Servers"))
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        bot.loop.create_task(status_task())
        bot.cur.execute("CREATE TABLE IF NOT EXISTS prefix(guild INT, prefix TEXT)")
        
        
		
 
	
if __name__ == "__main__":
	for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
		try:
			bot.load_extension(cogs_dir + "." + extension)
		except Exception as e:
			print(f'Failed to load extension {extension}.')
			traceback.print_exc()
			
    
        
async def status_task():
    while True:
        now = datetime.datetime.utcnow()
        current_time = now.strftime("%H:%M %p")
        date = now.strftime("%b %d, %Y")
        await bot.change_presence(status=discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.watching,name=f"{current_time} | {date} | {len(bot.guilds)} Servers"))
        await asyncio.sleep(7)
        

        
# Current Guild Prefix Checker. Send The Keyword "prefix"        

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)
    if not message.content.startswith("prefix"):
        return
    prefix = get_prefix(bot, message)
    em = discord.Embed(color=random.randint(0, 0xFFFFFF))
    em.description = f"**Prefix For ``{message.guild}`` Is ``{prefix[0]}``**"
    

        
@bot.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(color=random.randint(0, 0xFFFFFF))
        em.description = f'This command is on cooldown. Please wait ``{error.retry_after:.2f}s``'
        await ctx.send(embed=em)
    elif isinstance(error, commands.MissingPermissions):
        missing_perms = error.missing_permsmissing_perms = error.missing_perms
        em = discord.Embed(color=random.randint(0, 0xFFFFFF))
        em.description = f"You are missing the required permissions: ``{missing_perms}``"
        await ctx.send(embed=em)
        await ctx.message.add_reaction('🚫')
    elif isinstance(error, commands.BotMissingPermissions):
        missing_perms = error.missing_perms
        em = discord.Embed(color=random.randint(0, 0xFFFFFF))
        em.description = f"I am missing the required permissions: ``{missing_perms}``"
        await ctx.send(embed=em)
        await ctx.message.add_reaction('🚫')
    elif isinstance(error, commands.NotOwner):
        em = discord.Embed(color=random.randint(0, 0xFFFFFF))
        em.description = "This Command Is For My Owner Only"
        await ctx.send(embed=em)
        await ctx.message.add_reaction('🚫')
    elif isinstance(error, commands.MissingAnyRole):
        missing_roles = error.missing_roles
        em = discord.Embed(color=random.randint(0, 0xFFFFFF))
        em.description = f"You Are Missing The Required Role(s): ``{missing_roles}``"
        await ctx.send(embed=em)
        await ctx.message.add_reaction('🚫')
    elif isinstance(error, commands.MissingRole):
        missing_roles = error.missing_roles
        em = discord.Embed(color=random.randint(0, 0xFFFFFF))
        em.description = f"You Are Missing The Required Role: ``{missing_roles}``"
        await ctx.send(embed=em)
        await ctx.message.add_reaction('🚫')
    elif isinstance(error, commands.MemberNotFound):
        em = discord.Embed(color=random.randint(0, 0xFFFFFF))
        em.description = "This User Was Not Found."
        await ctx.send(embed=em)
    elif isinstance(error, commands.ChannelNotReadable):
        em = discord.Embed(color=random.randint(0, 0xFFFFFF))
        em.description = "I Cannot Read This Channel, Check Over The Permissions."
        await ctx.send(embed=em)
    elif isinstance(error, commands.RoleNotFound):
        em = discord.Embed(color=random.randint(0, 0xFFFFFF))
        em.description = "Role Not Found"
        await ctx.send(embed=em)
        

    

bot.run('DISCORD_BOT_TOKEN_HERE')