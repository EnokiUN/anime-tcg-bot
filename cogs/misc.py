import discord 
from discord.ext import commands 
import ebt
import math

class misc(commands.Cog):
    def __init__(self, client):
        self.client = client 
        
    @commands.command(aliases=['test'])
    async def ping(self, ctx):
        await ctx.message.reply(f'My ping is **{round(self.client.latency * 1000)}ms**, running version 0.6.0 beta')
        
    @commands.command(name='8ball', aliases=['8b']) 
    async def _8ball(self, ctx, *, question):
        response = await ebt.misctools._8ball()
        await ctx.message.reply(response)
            
    #@commands.command(aliases=['calc'])
    async def math(self, ctx, *, equation):
        await ctx.message.reply(equation+' = **'+str(eval(equation))+'**')
        
    @commands.command() 
    async def guildsplash(self, ctx):
        await ctx.message.reply(str(ctx.guild.splash_url))
        
    @commands.command() 
    async def memcount(self, ctx):
        a=0
        for i in ctx.guild.members:
            if not i.bot:
                a+=1
        await ctx.message.reply(a)
        
    @commands.command() 
    async def xpCalc(self, ctx, startlvl:int, endlvl:int, currxp:int=0):
        req1 = math.floor((5 / 6 * startlvl * (2 * startlvl * startlvl + 27 * startlvl + 91)) / 30)
        actualcurrxp=req1+currxp
        reqw = math.floor((5 / 6 * endlvl * (2 * endlvl * endlvl + 27 * endlvl + 91)) / 30)
        await ctx.message.reply(f'You need **__{reqw-actualcurrxp}__** xp to each level {endlvl}')
        
def setup(client):
    client.add_cog(misc(client))
