import asyncio

import discord
import random
import sqlite3

from discord.ext import commands




class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_prefix(self, ctx):
    	if not ctx.guild:
        	return "!"
    	prefix = self.bot.cur.execute(f"SELECT prefix FROM prefix WHERE guild = {ctx.guild.id}").fetchall()
    	if prefix == []:
        	return "!"
    	return prefix[0]

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix):
        if not prefix:
            return await ctx.send("You Did Not Mention a Prefix!")
        list = self.bot.cur.execute(f"SELECT * FROM prefix WHERE guild={ctx.guild.id}").fetchall()
        try:
            if list == []:
                self.bot.cur.execute(f"INSERT INTO prefix(guild, prefix) VALUES({ctx.guild.id}, '{prefix}')")
                em = discord.Embed(color=random.randint(0, 0xFFFFFF))
                em.description = f"Set The Prefix For ​`​`{ctx.guild}​`​` To: ​`​`{prefix}​`​`"
                em.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=em)
                self.bot.con.commit()
            else:
                self.bot.cur.execute(f"UPDATE prefix SET prefix = '{prefix}' WHERE guild = {ctx.guild.id}")
                em = discord.Embed(color=random.randint(0, 0xFFFFFF))
                em.description = f"Updated The Prefix For ​`​`{ctx.guild}​`​` To: ​`​`{prefix}​`​`"
                em.timestamp = datetime.datetime.utcnow()
                mes = f"{ctx.message.author} | {ctx.message.author.id} Changed Prefix to ​`​`{prefix}​`​` in \
                \n {ctx.guild.name} | {ctx.guild.id}"
                await self.bot.get_channel(744200783456895079).send(mes)
                await ctx.send(embed=em)
                self.bot.con.commit()
        except Exception as e:
            print(e)

    @commands.command()
    async def help(self,ctx):
        embed = discord.Embed(title = "*All Public Commands*", color=random.randint(0, 0xFFFFFF))
        embed.set_author(name= "Multi Purpose Stream Grabbing Bot",url= "https://discord.com/api/oauth2/authorize?client_id=594663400143847424&permissions=26688&scope=bot", icon_url=self.bot.user.avatar_url)
        embed.add_field(name= "​`​`​`[p] = Server Custom Prefix\n- !prefix [p] • Change Prefix\n- Say prefix To Check The Custom Prefix​`​`​`", value= "``[p]match\n[p]names\n[p]nfl\n[p]nflnames\n[p]nhl\n[p]nhlnames\n[p]nba\n[p]nbanames\n[p]f1\n[p]f1names\n[p]motogp\n[p]motogpnames\n[p]ufc\n[p]ufcnames\n[p]boxing\n[p]boxingnames\n[p]prefix newprefix",inline=False)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text= "[p]help")
        await ctx.send(embed=embed)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Music(bot))