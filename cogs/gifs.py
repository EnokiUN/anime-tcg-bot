import discord 
from discord.ext import commands 
import discord_slash
from discord_slash.utils.manage_commands import create_option
from discord_slash import cog_ext
from ebt import giftools


class gifs(commands.Cog): 
    
    def __init__(self, client):
        self.client = client
    
    @cog_ext.cog_slash(name='neko', description='sends a gif of a neko')
    async def neko(self, ctx):
        embed = await giftools.random_gif('neko', title='Here, have a neko', footer=f'executed by {ctx.author}')
        await ctx.send(embed=embed) 

    @commands.command(name='neko', description='sends a gif of a neko')
    async def nneko(self, ctx):
        embed = await giftools.random_gif('neko', title='Here, have a neko', footer=f'executed by {ctx.author}')
        await ctx.message.reply(embed=embed) 

    @cog_ext.cog_slash(name='F', description='Press F to pay respect')
    async def f(self, ctx):
        embed = await giftools.random_gif('F to pay respects', title='**F** in the chat', footer=f'executed by {ctx.author}')
        await ctx.send(embed=embed)

    @commands.command(name='F', description='Press F to pay respect')
    async def nf(self, ctx):
        embed = await giftools.random_gif('Press F to pay respects', title='**F** in the chat', footer=f'executed by {ctx.author}')
        await ctx.message.reply(embed=embed)    

    @cog_ext.cog_slash(name='fbi', description='calls the fbi')
    async def fbi(self, ctx):
        embed = await giftools.random_gif('fbi raid', title='FBI OPEN UP', footer=f'executed by {ctx.author}')
        await ctx.send(embed=embed)

    @commands.command(name='fbi', description='calls the fbi')
    async def nfbi(self, ctx):
        embed = await giftools.random_gif('fbi raid', title='FBI OPEN UP', footer=f'executed by {ctx.author}')
        await ctx.message.reply(embed=embed)         

    @cog_ext.cog_slash(name='loli', description='sends you a gif of a loli')
    async def loli(self, ctx):
        embed = await giftools.random_gif('anime loli cute', title='here, have a cute loli', footer=f'executed by {ctx.author}')
        await ctx.send(embed=embed)
    
    @commands.command(name='loli', description='sends you a gif of a loli')
    async def nloli(self, ctx):
        embed = await giftools.random_gif('anime loli cute', title='here, have a cute loli', footer=f'executed by {ctx.author}')
        await ctx.message.reply(embed=embed)

    @cog_ext.cog_slash(name='stare',description="stares at the target", options=[create_option(name='target', description='the person you want to kill with stares', option_type=6, required=True)])
    async def stare(self, ctx, target : discord.Member):
        embed = await giftools.two_user_action(ctx.author, target, 'stare', 'stared at')
        await ctx.send(content=target.mention, embed=embed)

    @commands.command(name='stare',description="stares at the target")
    async def nstare(self, ctx, target : discord.Member):
        embed = await giftools.two_user_action(ctx.author, target, 'stare', 'stared at')
        await ctx.message.reply(content=target.mention, embed=embed)

    @cog_ext.cog_slash(name="salute",description="salute the target", options=[create_option(name='target', description='the person you want to pay respect to', option_type=6, required=True)])
    async def salute(self, ctx, target : discord.Member):
        embed = await giftools.two_user_action(ctx.author, target, 'salute', 'saluted')
        await ctx.send(content=target.mention, embed=embed)

    @commands.command(name="salute",description="salute the target")
    async def nsalute(self, ctx, target : discord.Member):
        embed = await giftools.two_user_action(ctx.author, target, 'salute', 'saluted')
        await ctx.message.reply(content=target.mention, embed=embed)

    @cog_ext.cog_slash(name="kill",description="kills the target", options=[create_option(name='target', description='the person you want to kill', option_type=6, required=True)])
    async def kill(self, ctx, target : discord.Member):
        embed = await giftools.two_user_action(ctx.author, target, 'kill', 'killed')
        await ctx.send(content=target.mention, embed=embed)

    @commands.command(name="kill",description="kills the target")
    async def nkill(self, ctx, target : discord.Member):
        embed = await giftools.two_user_action(ctx.author, target, 'kill', 'killed')
        await ctx.message.reply(content=target.mention, embed=embed)

    @cog_ext.cog_slash(name="slap",description="slap the target", options=[create_option(name='target', description='the person you want to slap', option_type=6, required=True)])
    async def slap(self, ctx, target : discord.Member):
        embed = await giftools.two_user_action(ctx.author, target, 'slap', 'slapped') 
        await ctx.send(content=target.mention, embed=embed)

    @commands.command(name="slap",description="slap the target")
    async def nslap(self, ctx, target : discord.Member):
        embed = await giftools.two_user_action(ctx.author, target, 'slap', 'slapped')
        await ctx.message.reply(content=target.mention, embed=embed)

    @cog_ext.cog_slash(name="stab",description="stabs the target", options=[create_option(name='target', description='the person you want to stab', option_type=6, required=True)])
    async def stab(self, ctx, target : discord.Member):
        embed = await giftools.two_user_action(ctx.author, target, 'stab', 'stabbed')
        await ctx.send(content=target.mention, embed=embed)

    @commands.command(name="stab",description="stabs the target")
    async def nstab(self, ctx, target : discord.Member):
        embed = await giftools.two_user_action(ctx.author, target, 'stab', 'stabbed')  
        await ctx.message.reply(content=target.mention, embed=embed)

    @cog_ext.cog_slash(name="punch",description="punches the target", options=[create_option(name='target', description='the person you want to punch', option_type=6, required=True)])
    async def punch(self, ctx, target : discord.Member):
        embed = await giftools.two_user_action(ctx.author, target, 'punch', 'punched')
        await ctx.send(content=target.mention, embed=embed)

    @commands.command(name="punch",description="punches the target")
    async def npunch(self, ctx, target : discord.Member):
        embed = await giftools.two_user_action(ctx.author, target, 'punch', 'punched')  
        await ctx.message.reply(content=target.mention, embed=embed)

    @cog_ext.cog_slash(name="hug",description="hugs the target", options=[create_option(name='target', description='the person you want to hug', option_type=6, required=True)])
    async def hug(self, ctx, target : discord.Member):
        embed = await giftools.two_user_action(ctx.author, target, 'hug', 'hugged')  
        await ctx.send(content=target.mention, embed=embed)

    @commands.command(name="hug",description="hugs the target")
    async def nhug(self, ctx, target : discord.Member):
        embed = await giftools.two_user_action(ctx.author, target, 'hug', 'hugged')    
        await ctx.message.reply(content=target.mention, embed=embed)

    @cog_ext.cog_slash(name="wave",description="wave at the target", options=[create_option(name='target', description='the person you want to wave at', option_type=6, required=True)])
    async def wave(self, ctx, target : discord.Member):
        embed = await giftools.two_user_action(ctx.author, target, 'wave', 'waved at')
        await ctx.send(content=target.mention, embed=embed)

    @commands.command(name="wave",description="wave at the target")
    async def nwave(self, ctx, target : discord.Member):
        embed = await giftools.two_user_action(ctx.author, target, 'wave', 'waved at')  
        await ctx.message.reply(content=target.mention, embed=embed)

    @cog_ext.cog_slash(name="pat",description="pats the target", options=[create_option(name='target', description='the person you want to pat', option_type=6, required=True)])
    async def pat(self, ctx, target : discord.Member):
        embed = await giftools.two_user_action(ctx.author, target, 'pat', 'pat')
        await ctx.send(content=target.mention, embed=embed)

    @commands.command(name="pat",description="pats the target")
    async def npat(self, ctx, target : discord.Member):
        embed = await giftools.two_user_action(ctx.author, target, 'pat', 'pat')
        await ctx.message.reply(content=target.mention, embed=embed)

    @commands.command(name="shrug",description="makes you shrug")
    async def nshrug(self, ctx):
        embed = await giftools.single_user_action(ctx.author, 'shrug', 'shrugged')
        await ctx.message.reply(embed=embed)

    @cog_ext.cog_slash(name="shrug",description="makes you shrug")
    async def shrug(self, ctx):
        embed = await giftools.single_user_action(ctx.author, 'shrug', 'shrugged')
        await ctx.send(embed=embed)

    @commands.command(name="sigh",description="makes you sigh")
    async def nsigh(self, ctx):
        embed = await giftools.single_user_action(ctx.author, 'sigh', 'sighed')
        await ctx.message.reply(embed=embed)

    @cog_ext.cog_slash(name="sigh",description="makes you sigh")
    async def sigh(self, ctx):
        embed = await giftools.single_user_action(ctx.author, 'sigh', 'sighed')
        await ctx.send(embed=embed)

    @commands.command(name='smile', description='makes you smile')
    async def nsmile(self, ctx):
        embed = await giftools.single_user_action(ctx.author, 'smile', 'smiled')
        await ctx.message.reply(embed=embed)

    @cog_ext.cog_slash(name="smile",description="makes you smile")
    async def smile(self, ctx):
        embed = await giftools.single_user_action(ctx.author, 'smile', 'smiled')
        await ctx.send(embed=embed)

    @commands.command(name="laugh",description="makes you laugh")
    async def nlaugh(self, ctx):
        embed = await giftools.single_user_action(ctx.author, 'laugh', 'laughed') 
        await ctx.message.reply(embed=embed)

    @cog_ext.cog_slash(name="laugh",description="makes you laugh")
    async def laugh(self, ctx):
        embed = await giftools.single_user_action(ctx.author, 'laugh', 'laughed')
        await ctx.send(embed=embed)

    @commands.command(name="cry",description="makes you cry")
    async def ncry(self, ctx):
        embed = await giftools.single_user_action(ctx.author, 'cry', 'cried')
        await ctx.message.reply(embed=embed)

    @cog_ext.cog_slash(name="cry",description="makes you cry")
    async def cry(self, ctx):
        embed = await giftools.single_user_action(ctx.author, 'cry', 'cried')
        await ctx.send(embed=embed)

    @commands.command(name="dance",description="makes you dance")
    async def ndance(self, ctx):
        embed = await giftools.single_user_action(ctx.author, 'dance', 'danced')
        await ctx.message.reply(embed=embed)

    @cog_ext.cog_slash(name="dance",description="makes you dance")
    async def dance(self, ctx):
        embed = await giftools.single_user_action(ctx.author, 'dance', 'danced')
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(gifs(client))