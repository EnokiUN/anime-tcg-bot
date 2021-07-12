import discord
from discord.ext import commands
import sqlite3
import json
import ebt
from ebt import DiscordLog

mods = [559226493553737740]

class gameconfig(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def c(self, ctx, *, query):
        if ctx.author.id not in mods:
            return
        table = ebt.SqlTools('at')
        result = table.execute(query)
        table.commit() 
        table.close()
        if not result == '':
            await ctx.message.reply(str(result))
        await DiscordLog(self.client, 860054849047625769, f'{ctx.author} edited the database ({ctx.message.content})')

        
    @commands.command() 
    async def add_char(self, ctx, name, imgurl, pack, rarity, patk, pdef, matk, mdef, moneyl, moneyh, xpl, xph, hp, *, deck):
        if ctx.author.id not in mods:
            return
        table = ebt.SqlTools('at')
        amount = table.execute('SELECT id FROM chars') 
        table.execute(('INSERT INTO chars(id, name, imgurl, pack, rarity, patk, pdef, matk, mdef) VALUES(?, ?,?,?,?,?,?,?,?)') , (len(amount) +1,name, imgurl, pack, rarity, int(patk), int(pdef), int(matk), int(mdef)))
        table.execute(('INSERT INTO enemies(name, show, deck, moneyl, moneyh, xpl, xph, hp) VALUES(?,?,?,?,?,?,?,?)'), (name, pack, deck, int(moneyl), int(moneyh), int(xpl), int(xph),int(hp)))
        table.commit()
        table.close()
        await ctx.message.reply(f'successfully added {name} to the database!')
        await DiscordLog(self.client, 860055076911317022, f"{ctx.author} has added **{name}** from the pack **{pack}**, now we have **{len(amount)+1}** characters! id:{len(amount)+1}")
     
    @commands.command() 
    async def fixthisshitplsuwunyaluvukasumichan(self, ctx):
        if ctx.author.id not in mods:
            return 
        table = ebt.SqlTools('at')
        data=table.execute('SELECT name FROM chars')
        a=0
        for i in data:
            a+=1
            table.execute(f'UPDATE chars SET id={a} WHERE name="{i[0]}"')
        table.commit() 
        table.close() 
        await ctx.message.reply('fixed tehe')
        
    @commands.command() 
    async def restoreee(self, ctx):
        if ctx.author.id not in mods:
            return 
        table = ebt.SqlTools('at')
        data = [(614167364904157184, 200, 10, 2, 110, '[]', '[16,16,16,16,16,16,16,16,16,16,16,16,16,9,9,9,9,9,9,9]', 2, 0), (799319783266189332, 0, 0, 0, 100, '[]', '[16,16,16,16,16,16,16,16,16,16,16,16,16,9,9,9,9,9,9,9]', 0, 0), (694877697008205945, 0, 5, 1, 105, '[]', '[16,16,16,16,16,16,16,16,16,16,16,16,16,9,9,9,9,9,9,9]', 1, 0), (263000003562176512, 100, 5, 1, 105, '[]', '[16,16,16,16,16,16,16,16,16,16,16,16,16,9,9,9,9,9,9,9]', 1, 0), (468117156249206805, 1700, 805, 20, 218, '[9, 9, 16, 16, 16, 9]', '[16,16,16,16,16,16,16,16,16,16,16,16,16,9,9,9,9,9,9,9]', 115, 21), (148103303887060992, 1200, 5, 1, 105, '[]', '[16,16,16,16,16,16,16,16,16,16,16,16,16,9,9,9,9,9,9,9]', 1, 0), (815270004345274418, 100, 5, 1, 105, '[]', '[16,16,16,16,16,16,16,16,16,16,16,16,16,9,9,9,9,9,9,9]', 1, 2)]
        for i in data:
            table.execute(f'INSERT INTO main(id, bal, xp, lvl, hp, cards, deck, wins, losses) VALUES(?,?,?,?,?,?,?,?,?)', (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]))
        table.commit() 
        await ctx.message.reply('restored :)')
        
def setup(client):
    client.add_cog(gameconfig(client))