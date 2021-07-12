import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands, tasks
import os
import random
import sqlite3
import ebt
from discord import utils
import json
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType, Select, SelectOption
import asyncio
import threading
import datetime
from threading import Thread
from discordTogether import DiscordTogether
from deadnt import thou_shall_not_die


mods = [559226493553737740]


class CustomHelpCommand(commands.HelpCommand):
	def __init__(self):
		super().__init__()

	async def send_bot_help(self, mapping):
		embed = discord.Embed(title='Commands', colour=ebt.embed_colour) 
		hidden=['gameconfig']
		for cog in mapping:
			if not cog is None:
				if not mapping[cog] == [] or cog.name in hidden:
					embed.add_field(name=cog.qualified_name,
					                value=' '.join(
					                    map(str, [
					                        command.qualified_name
					                        for command in mapping[cog]
					                    ])))
		await self.get_destination().send(embed=embed)

	async def send_cog_help(self, cog):
		embed = discord.Embed(
		    title=cog.qualified_name + ' Commands',
		    description=' '.join(
		        map(str,
		            [command.qualified_name
		             for command in cog.get_commands()])),
		    colour=ebt.embed_colour)
		await self.get_destination().send(embed=embed)

	async def send_command_help(self, command):
		desc = [
		    command.description if command.description is not None else ''
		][0]
		usage = '.' + command.qualified_name + ' ' + [
		    ' '.join(map(str, command.clean_params))
		    if command.clean_params is not None else ''
		][0]
		embed = discord.Embed(title=command.qualified_name,
		                      description=desc + '\n\n' + usage,
		                      colour=ebt.embed_colour)
		await self.get_destination().send(embed=embed)



client = commands.Bot(case_insensitive=True,
                      command_prefix='.',
                      help_command=CustomHelpCommand())
slash = SlashCommand(client, sync_commands=True)
togetherControl = DiscordTogether(client)


@client.event
async def on_ready():
	print('I\'m ready')
	conn = sqlite3.connect('at.db')
	c = conn.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS 'main' (
        'id' INT,
        'bal' INT DEFAULT 0,
        'xp' INT DEFAULT 0,
        'lvl' INT DEFAULT 0, 
        'hp' INT DEFAULT 100,
        'cards' TEXT DEFAULT '[]',
        'deck' TEXT DEFAULT '[16,16,16,16,16,16,16,16,16,16,16,16,16,9,9,9,9,9,9,9]',
        'wins' INT DEFAULT 0, 
        'losses' INT DEFAULT 0, 
        'currfloor' INT DEFAULT 1,
        'maxfloor' INT DEFAULT 1,
        PRIMARY KEY('id')
    );
    """)
	conn.commit()
	c.execute("""CREATE TABLE IF NOT EXISTS 'chars' (
        'id' INT, 
        'name' STR,
        'pack' STR DEFAULT 'none',
        'rarity' STR DEFAULT 'bronze',
        'imgurl' STR, 
        'patk' INT DEFAULT 0,
        'pdef' INT DEFAULT 0,
        'matk' INT DEFAULT 0, 
        'mdef' INT DEFAULT 0, 
        PRIMARY KEY('id')
    );
    """)
	conn.commit()
	c.execute("""CREATE TABLE IF NOT EXISTS 'packs' (
        'name' STR, 
        'price' INT,
        'series' STR, 
        'bronze' INT DEFAULT 0,
        'silver' INT DEFAULT 0,
        'gold' INT DEFAULT 0, 
        PRIMARY KEY('name')
    );
    """)
	conn.commit()
	c.execute("""CREATE TABLE IF NOT EXISTS 'enemies' (
        'name' STR, 
        'deck' STR,
        'moneyl' INT, 
        'moneyh' INT DEFAULT 0,
        'xpl' INT DEFAULT 0,
        'xph' INT DEFAULT 0, 
        'hp' INT DEFAULT 100,
        'show' STR, 
        PRIMARY KEY('name')
    );
    """)
	conn.commit() 
	c.execute("""CREATE TABLE IF NOT EXISTS 'floors' (
        'id' INT, 
        'show' STR,
        'boss' STR, 
        'lvll' INT DEFAULT 0,
        'lvlh' INT DEFAULT 0,
        PRIMARY KEY('id')
    );
    """)
	conn.commit() 
	c.close()
	conn.close() 
	DiscordComponents(client)


@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		pass
	elif isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('etoo, you have to enter all the required arguments')
	elif isinstance(error, commands.BotMissingPermissions):
		await ctx.send(
		    f'welll, it looks like you must provide me with the{error.missing_perms[0]} permission for this command to work, hope that isn\'t too much'
		)
	else:
		await ctx.message.reply(f'ehhh, it looks like {error}')

@client.event
async def on_command(ctx):
    f =  open('log.txt', 'a')
    f.write(f'{ctx.author} invoked the {ctx.command} command in {ctx.guild.name} at {datetime.datetime.now()} ({ctx.message.content})\n')
    f.close()
        
@client.event
async def on_message(message):
	ch = message.channel
	auth = message.author
	if auth.bot is False and ch.guild is not None:
		await client.process_commands(message)


@client.command()
async def together(ctx, ttype):
    link = await togetherControl.create_link(ctx.author.voice.channel.id, ttype)
    await ctx.message.reply(f"Click the blue link!\n{link}")



@client.command(description='mod command')
async def load(ctx, extension):
	if ctx.author.id in mods:
		client.load_extension(f'cogs.{extension}')
		await ctx.message.reply('successfully loaded ' + extension)

@client.command(description='mod command')
async def unload(ctx, extension):
	if ctx.author.id in mods:
		client.unload_extension(f'cogs.{extension}')
		await ctx.message.reply('successfully unloaded '+extension)

@client.command()
async def reload(ctx, cog=None):
	if ctx.author.id in mods:
		if cog is None:
			for i in os.listdir('./cogs'):
				if i.endswith('.py'):
					client.unload_extension(f'cogs.{i[:-3]}')
					client.load_extension(f'cogs.{i[:-3]}')
			await ctx.message.reply('successfully reloaded **every cog**')
		else:
			client.unload_extension(f'cogs.{cog}')
			client.load_extension(f'cogs.{cog}')
			await ctx.message.reply('successfully reloaded '+cog)

def autoload():
	for i in os.listdir('./cogs'):
		if i.endswith('.py'):
			client.load_extension(f'cogs.{i[:-3]}')


@client.command()
async def backup(ctx, dir = None):
    if ctx.author.id in mods:
        if dir is not None:
            await ctx.author.send(file=discord.File(dir))
            return
        for i in os.listdir('./cogs'):
            if i.endswith('.py'):
                await ctx.author.send(file=discord.File('./cogs/' + i))
        for i in os.listdir('./templates'):
            if i.endswith('.html'):
                await ctx.author.send(file=discord.File('./templates/' + i))
        for i in os.listdir('.'):
            if not os.path.isdir(i):
                await ctx.author.send(file=discord.File(i))
        await ctx.message.reply('backuped!')


autoload()
thou_shall_not_die() 
client.run(os.getenv('TOKEN'))
