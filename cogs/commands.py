import asyncio

import discord
import random
import sqlite3
import datetime
from datetime import timedelta
import requests
from pyowm import OWM

from discord.ext import commands,tasks

extensions = ["cogs.commands","cogs.boxing","cogs.boxingnames","cogs.match","cogs.motogp","cogs.motogpnames","cogs.names","cogs.nba","cogs.nhl","cogs.nhlnames","cogs.ufc","cogs.ufcnames","cogs.f1","cogs.f1names","cogs.nfl","cogs.nflnames"]

owm = OWM('OWM_TOKEN') # Gain the token at https://home.openweathermap.org/users/sign_up
mgr = owm.weather_manager()


afkdict = {}

async def embedsend(destination, msg):
    em = discord.Embed(color=random.randint(0, 0xFFFFFF))
    em.description = msg
    await destination.send(embed=em)

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.unmute_checker.start()
        
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix):
        """custom prefix"""
        if not prefix:
            return await ctx.send("You Did Not Mention a Prefix!")
        list = self.bot.cur.execute(f"SELECT * FROM prefix WHERE guild={ctx.guild.id}").fetchall()
        try:
            if list == []:
                self.bot.cur.execute(f"INSERT INTO prefix(guild, prefix) VALUES({ctx.guild.id}, '{prefix}')")
                em = discord.Embed(color=random.randint(0, 0xFFFFFF))
                em.description = f"Set The Prefix For ``{ctx.guild}`` To: ``{prefix}``"
                em.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=em)
                self.bot.con.commit()
            else:
                self.bot.cur.execute(f"UPDATE prefix SET prefix = '{prefix}' WHERE guild = {ctx.guild.id}")
                em = discord.Embed(color=random.randint(0, 0xFFFFFF))
                em.description = f"Updated The Prefix For ``{ctx.guild}`` To: ``{prefix}``"
                em.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=em)
                self.bot.con.commit()
        except Exception as e:
            print(e)

    @commands.command()
    async def help(self,ctx):
        embed = discord.Embed(title = "*All Public Commands*", color=random.randint(0, 0xFFFFFF))
        embed.set_author(name= "Multi Purpose Stream Grabbing Bot",url= "https://discord.com/api/oauth2/authorize?client_id=594663400143847424&permissions=26688&scope=bot", icon_url=self.bot.user.avatar_url)
        embed.add_field(name= "```[p] = Server Custom Prefix\n- !prefix [p] • Change Prefix\n- Say prefix To Check The Custom Prefix```", value= "``[p]match\n[p]names\n[p]nfl\n[p]nflnames\n[p]nhl\n[p]nhlnames\n[p]nba\n[p]nbanames\n[p]f1\n[p]f1names\n[p]motogp\n[p]motogpnames\n[p]ufc\n[p]ufcnames\n[p]boxing\n[p]boxingnames\n[p]prefix newprefix",inline=False)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text= "[p]help")
        await ctx.send(embed=embed)
        await ctx.message.delete()
        
    @commands.command()
    @commands.is_owner()
    async def reload(self,ctx):
        """reload all cogs"""
        try:
            for cogs in extensions:
                self.bot.reload_extension(cogs)
            
                em = discord.Embed(color=random.randint(0, 0xFFFFFF))
                em.description = "All Cogs Reloaded Successfully."
                
            await ctx.send(embed=em)

        except commands.ExtensionError as e:
            em = discord.Embed(color=random.randint(0, 0xFFFFFF))
            em.description = f"{e.__class__.__name__}: {e}"
            await ctx.send(embed=em)
            
    @commands.command(aliases=["weather","temp"])
    async def weathercheck(self,ctx, *, city):
        """quick weather report on any location, city, country, town. OWM token needed."""
        observation = mgr.weather_at_place(city)
        w = observation.weather
        
        try:
            fmt = "%H:%M %p" # "**%d-%m-%Y** **%H:%M %p** %Z%z"
        
            clouds = w.detailed_status                         
            wind = w.wind()["speed"]                            
            humidity = w.humidity                               
            tempmax  = w.temperature('celsius')["temp_max"]
            temp = w.temperature('celsius')["temp"]
            tempmin = w.temperature('celsius')["temp_min"]
            feelslike = w.temperature('celsius')["feels_like"]  
            cloudpercent = w.clouds
            sunrise_datetime = w.sunrise_time(timeformat='date')
            sunrise = sunrise_datetime.strftime(fmt)
            sunset_datetime = w.sunset_time(timeformat='date')
            sunset = sunset_datetime.strftime(fmt)
            timestamp = timestamps.now()
            time = timestamp.strftime(fmt)

            c = "°C"

            rain = None
            if rain is not None:
                rain = w.rain

            if temp > 11:
                image = "https://cdn.discordapp.com/attachments/822851842715287622/834536500111736883/sun-behind-cloud_26c5.png"
            elif temp > 17:
                image = "https://cdn.discordapp.com/attachments/822851842715287622/834537180394815519/The_Sun_Emoji_grande.png"
            else:
                image = "https://cdn.discordapp.com/attachments/822851842715287622/834537887499681852/f74df038c7948001f079960b1c27d63a-cloudy-icon-by-vexels.png"

            
            em = discord.Embed(color=random.randint(0, 0xFFFFFF),title=f"*Weather Rreport For {city}*",description = f":cloud: **{clouds}**")
            em.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
            em.set_thumbnail(url=image)
            em.timestamp = datetime.datetime.utcnow()
            em.add_field(name=f"Temperature :white_sun_small_cloud:",value=f"[``{temp}{c}``]",inline=True)
            em.add_field(name=f"Max Temperature :heavy_plus_sign:",value=f"[``{tempmax}{c}``]",inline=True)
            em.add_field(name=f"Min Temperature: :heavy_minus_sign:",value=f"[``{tempmin}{c}``]",inline=True)
            em.add_field(name=f"Feels Like: :fog:",value=f"[``{feelslike}{c}``]",inline=True)
            em.add_field(name=f"Clouds %: :white_sun_rain_cloud:",value=f"[``{cloudpercent}%``]",inline=True)
            em.add_field(name=f"Rain: :cloud_rain:",value=f"[``{rain}``]",inline=True)
            em.add_field(name=f"Humidity: :earth_americas:",value=f"[``{humidity}%``]",inline=True)
            em.add_field(name=f"Sunrise: :sunrise_over_mountains:",value=f"[``{sunrise}``]",inline=True)
            em.add_field(name=f"Sunset: :city_sunset:",value=f"[``{sunset}``]")

            await ctx.message.delete()

            await ctx.send(embed=em)

        except Exception:
            e = discord.Embed(color=random.randint(0, 0xFFFFFF))
            em.description = f"The Location Parameter {city} Was Wrong, and I Could Not Grab Data For That. Please Try Again"
            await ctx.reply(embed=e) 
            
    @commands.command()
    async def breakingbad(self,ctx, *, character = None):
        """ A Breaking Bad Character Database command that adapts to a inconsistent and buggy api -_- """
        await ctx.message.delete()
        await ctx.channel.trigger_typing()

        char = str(character).replace(" ","+")

        try:
            if character is not None:
                r = requests.get(f"https://www.breakingbadapi.com/api/characters?name={char}").json()[0]
            else:
                r = requests.get("https://www.breakingbadapi.com/api/character/random").json()[0]

            name = r["name"]
            birthday = r["birthday"]
            job = r["occupation"][0:10]
            image = r["img"]
            status = r["status"]
            nickname = r["nickname"]
            actor = r["portrayed"]
            bettercallsaul = r["better_call_saul_appearance"]
            appearance = r["appearance"]

            if birthday == []:
                birthday = "Unknown"

            occupation = "\n".join(job)
            appearedin = ",".join(map(str,appearance))

            rname = name.replace(" ","+")
            deathsr = requests.get(f"https://www.breakingbadapi.com/api/death-count?name={rname}").json()[0]
            deaths = deathsr["deathCount"]

            if bettercallsaul == []:
                bettercallsaul = "No"
            else:
                bettercallsaul = "Yes"

            em = discord.Embed(color=random.randint(0, 0xFFFFFF),title=f"*{name}* - *{birthday}* - *S {appearedin}*")
            em.set_author(name=name,icon_url=image)
            em.set_thumbnail(url=image)
            em.timestamp = datetime.datetime.utcnow()
            em.add_field(name=f"Status:",value=f"[``{status}``]")
            em.add_field(name=f"Nickname:",value=f"[``{nickname}``]")
            em.add_field(name=f"Job/Purpose:",value=f"[``{occupation}``]")
            em.add_field(name=f"Played By:",value=f"[``{actor}``]")
            em.add_field(name=f"Deaths Responsible For:",value=f"[``{deaths}/271``]")
            em.add_field(name=f"Appears In Better Call Saul?:",value=f"[``{bettercallsaul}``]")

            if not requests.get(f"https://www.breakingbadapi.com/api/quote/random?author={rname}").json() == []:
                quoter = requests.get(f"https://www.breakingbadapi.com/api/quote/random?author={rname}").json()
                q = quoter[0]
                randomquote = q["quote"]
                em.add_field(name=f"Random Quote By {name}",value=f"[``{randomquote}``]")

            if not requests.get(f"https://www.breakingbadapi.com/api/death?name={rname}").json() == []:
                deathinfor = requests.get(f"https://www.breakingbadapi.com/api/death?name={rname}").json()
                de = deathinfor[0]
                deathname = de["death"]
                cause = de["cause"]
                responsible = de["responsible"]
                lastwords = de["last_words"]
                season = de["season"]
                epi = de["episode"]
                deathdate = f"S{season}E{epi}"

                if deathname == responsible:
                    responsible = "Suicide / Self Responsible"

                dead = f"**Cause:** [``{cause}``]\n**Responsible:** [``{responsible}``]\n**Last Words:** [``{lastwords}``]\n**When?:** [``{deathdate}``]"
                em.add_field(name=f"Death Info:",value= dead)

            await ctx.send(embed=em)
        except Exception:
            if character = None:
                await ctx.send("Error, Retrying",delete_after=3)
                await ctx.invoke(self.bot.get_command('breakingbad'))
            else:
                await ctx.send("Unknown Character",delete_after=2)
                
    # basic and plain AFK command, will not support cross server                             
    @commands.command()
    async def afk(self, ctx, *, message="AFK"):
        global afkdict
        
        if ctx.author.id not in afkdict:
            afkdict[ctx.author.id] = message
            
            name = ctx.author.name
            
            if len(name) <= 32:
                num = 32 - len("[AFK] ")
                split = len(name) - num
                name = name[:-split]
                await ctx.author.edit(nick=f"[AFK] {name}")
                
                em = discord.Embed(color=random.randint(0, 0xFFFFFF))
                em.description = f":x: **{ctx.author.name}** is now ``[AFK]``: {afkdict[ctx.author.id]}"
                await ctx.send(embed=em)
                
    @commands.Cog.listener()
    async def on_message(self, message):
        global afkdict
        
        if message.author.id in afkdict and message.author != message.author.bot and "afk" not in message.content:
            afkdict.pop(message.author.id)
            
            em = discord.Embed(color=random.randint(0, 0xFFFFFF))
            em.description = f":white_check_mark:  Welcome back! **{message.author.name}**"
            await message.channel.send(embed=em,delete_after=5)
            await message.author.edit(nick=message.author.name)
            
        for member in message.mentions:
            if member.id in afkdict:
                afkmsg = afkdict[message.author.id]
                
                if member.id != message.author.id:
                    em = discord.Embed(color=random.randint(0, 0xFFFFFF))
                    em.description = f":x: **{member}** is AFK: ``{afkmsg}``"
                    
                    await message.channel.send(embed=em,delete_after=5)
                    
    @commands.command() 
    @commands.is_owner()
    async def mute(self,ctx,member: discord.Member,time = None,*,reason = "No Reason Provided"):
        """db mute command, !mute [@user/user.id/user.name INTs/m/h/d] (reason)"""
        time_convert = {"s":1, "m":60, "h":3600,"d":86400}
        if time[-1] not in time_convert.keys():
            await ctx.send("Time Inputs Are ``s, m, h, d``")
            return
        
        await ctx.message.delete()
        server = ctx.guild

        tempmute = int(time[0]) * time_convert[time[-1]]

        timestr = {"m":"Minute(s)", "h":"Hour(s)", "d":"Day(s)"}

        quick_add = timedelta(hours=1)
        date = datetime.datetime.utcnow() + quick_add

        addedtime = timedelta(seconds=tempmute)
        finaltime = (date + addedtime)

        muted_until = finaltime.strftime("%d:%H:%M:%S")

        try:
            if time is not None:
                self.bot.cur.execute(f"INSERT INTO mutes(userid, finaltime,channelid,guildid) VALUES({member.id}, '{muted_until}',{ctx.channel.id},{ctx.guild.id})")
                self.bot.con.commit()
                
                muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
                result = ''.join([i for i in time if not i.isdigit()])
                strtime = timestr[result]
                timeconvert = time[0]
                
                if reason == "No Reason Provided":
                    msg = f"{member} Muted for {timeconvert} {strtime}"
                else:
                    msg = f"{member} Muted for {timeconvert} {strtime} Reason: {reason}"
                    


                if muted_role is None:
                    for channel in server.channels:
                        await channel.set_permissions(member,overwrite=discord.PermissionOverwrite(send_messages = False))
                    
                    await embedsend(ctx,msg)
                else:
                    await member.add_roles(muted_role)
                    await ctx.send(f"{member} Muted for {time} Untill {muted_until} for Reason: {reason}")
            else:
                if reason == "No Reason Provided":
                    msg = f"{member} Muted."
                else:
                    msg = f"{member} Muted for Reason: {reason}"
                    
                    
                if muted_role is None:
                    for channel in server.channels:
                        await channel.set_permissions(member,overwrite=discord.PermissionOverwrite(send_messages = False))
                        
                    await embedsend(ctx,msg)
                    
                else:
                    await member.add_roles(muted_role)
                    await embedsend(ctx,msg)

        except Exception as e:
            await ctx.send(e)
            print(e)
            
    @tasks.loop(seconds=1)
    async def unmute_checker(self):
        """unmute checker, if muted time == time now, unmute triggered"""
        b = datetime.datetime.utcnow() + timedelta(hours=1)
        a = b.strftime("%d:%H:%M:%S")
        
        tuplelist = self.bot.cur.execute('SELECT finaltime FROM mutes').fetchall()
        
        list = [item for t in tuplelist for item in t]
        
        user = self.bot.cur.execute(f"SELECT userid FROM mutes WHERE finaltime = ?",(a,)).fetchone()
        channelid = self.bot.cur.execute(f"SELECT channelid FROM mutes WHERE finaltime = ?",(a,)).fetchone()
        guildid = self.bot.cur.execute(f"SELECT guildid FROM mutes WHERE finaltime = ?",(a,)).fetchone()
        
        if a in list:
            guild = self.bot.get_guild(guildid[0])
            member = guild.get_member(user[0])
            channel = self.bot.get_channel(channelid[0])
            
            muted_role = discord.utils.get(guild.roles, name="Muted")
            
            if muted_role in member.roles:
                await member.remove_roles(muted_role)
                await embedsend(channel,f"{member.mention} Is Now Unmuted.")
            else:
                await embedsend(channel,f"{member.mention} Is Now Unmuted.")
                for chan in guild.channels:
                    await chan.set_permissions(member,overwrite=discord.PermissionOverwrite(send_messages = True))        

def setup(bot):
    bot.add_cog(help(bot))
