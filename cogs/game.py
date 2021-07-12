import discord 
from discord.ext import commands 
import discord_slash
from discord_slash.utils.manage_commands import create_option
from discord_slash import cog_ext
import ebt
import random 
import json
import asyncio
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from PIL import Image
import requests
import io
from ebt import DiscordLog
import math
import os



playingchannelslist = list() 
playingplayerslist = list() 


async def initialize_database():
        table = ebt.SqlTools('at')
        return table

async def start_check(table, id):
    result = table.execute('SELECT id FROM main WHERE id =' + str(id))
    if result == []:
        return False
    return True

async def merge(urls, rturn):
        ims = list()
        bg = Image.open('canvas.png')
        for i in urls: 
            ims.append(Image.open(requests.get(url=i, stream=True).raw))
        for i in range(3):
            offset = (i)*200
            bg.paste(ims[i], (offset,0))
        with io.BytesIO() as image_binary:
            bg.save(image_binary, 'PNG')
            image_binary.seek(0)
            file= discord.File(fp=image_binary, filename=f'image{rturn}.png')
            return file

async def levelUp(ctx, memberid, table, client):
    while True:
        lvl, xp, hp = table.execute(f"SELECT lvl, xp, hp FROM main WHERE id =     {memberid}")[0]
        req, preq = await reqXp(lvl)
        if xp >= req:
            table.execute(F'UPDATE main SET lvl = {lvl+1}, hp = {math.floor(hp*1.05)} WHERE id = {memberid}')
            table.commit() 
            await ctx.send(f'Congratulations <@{memberid}>, you reached level **{lvl+1}** (Hp **{hp}** --> **{math.floor(hp*1.05)}**), keep it up,')
            ch = await client.fetch_channel(860801601601798184) 
            await ch.send(file=discord.File('at.db'))
        else:
            break
        
async def reqXp(level):
    preq = math.floor((5 / 6 * level * (2 * level * level + 27 * level + 91)) / 30) 
    req = math.floor((5 / 6 * (level + 1) * (2 * (level + 1) * (level + 1) + 27 * (level + 1) + 91)) / 30)
    return req, preq
    
async def fight(table, client, ctx, enemy):
        if ctx.channel.id in playingchannelslist:
            await ctx.send('Someone is already playing in this channel, try another one')
            return
        if ctx.author.id in playingplayerslist:
            await ctx.send('you can only participate in one fight at a time dummy')
            return
        playingchannelslist.append(ctx.channel.id)
        playingplayerslist.append(ctx.author.id)
        hhp = table.execute(f'SELECT hp FROM main WHERE id = {ctx.author.id}')[0][0]
        mhp = enemy[6]
        stuff = str() 
        ename= f'{enemy[0].capitalize()} [level {enemy[8]}]'
        msg = await ctx.send('initializing, please wait...')
        itc = await client.fetch_channel(859147484445540403)
        hand = list() 
        rturn = 0
        returned = [] 
        acards = table.execute(f"SELECT deck FROM main WHERE id = {ctx.author.id}")[0][0]
        ecards = enemy[1]
        acards = json.loads(acards)
        ecards = json.loads(enemy[1])
        ecardsi = list() 
        ecardsd = list() 
        acardsi = list() 
        acardsd = list() 
        for i in ecards:
            ecardsi.append(table.execute(f'SELECT name, imgurl, patk, pdef, matk, mdef FROM chars WHERE id = {i}')[0])
        for i in acards:
            acardsi.append(table.execute(f'SELECT name, imgurl, patk, pdef, matk, mdef FROM chars WHERE id = {i}')[0])
        random.shuffle(ecardsi)
        random.shuffle(acardsi)
        while mhp > 0 and hhp > 0:
            card = ecardsi[0]
            ecardsi.remove(card)
            ecardsd.append(card)
            if len(ecardsi) == 0:
                ecardsi = ecardsd
                ecardsd = [] 
                random.shuffle(ecardsi)
            name = card[0]
            data = '\n{} :boom: | {} :comet:\n{} :shield: | {} :trident:'.format(card[2],card[4],card[3],card[5])
            rturn += 1
            embed = discord.Embed(title=f'**{ctx.author.name}**: **{hhp}** hp :heart:\n**{ename}**: **{mhp}** hp :heart:', description=f'**[Round {rturn}]**\n'+f'**{name}**'+data+'\n`--------------------------------`\n'+stuff+
                '`--------------------------------`\n**Choose a Card:**', colour=ebt.embed_colour)
            embed.set_thumbnail(url=card[1])
            b = 0
            buttons = []
            buttons2 = [] 
            stuff = ''
            for i in range(3-len(hand)):
                hand.append(acardsi[0]) 
                acardsd.append(acardsi[0])
                acardsi.remove(acardsi[0])
                if len(acardsi) == 0:
                    acardsi = acardsd
                    acardsd = [] 
                    random.shuffle(acardsi)
            urls = list() 
            for i in hand:
                urls.append(i[1])
                b += 1
                buttons.append(Button(style=ButtonStyle.blue, label=str(b)))
                buttons2.append(Button(style=ButtonStyle.blue, label=str(b), disabled = True))
                data = '{} :boom: | {} :comet:\n{} :shield: | {} :trident:'.format(i[2],i[4],i[3],i[5])
                embed.add_field(name='{} - **{}**'.format(b,i[0]) ,value=data, inline=True)
            file = await merge(urls, rturn)
            pic = await itc.send(file=file)
            picurl = pic.attachments[0].url
            embed.set_image(url=picurl)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await msg.edit(content=ctx.author.mention, embed=embed, components=[buttons])
            def check(button):
                return button.message == msg and button.author == ctx.author
            try:
                res = await client.wait_for('button_click', timeout=300.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(f'{ctx.author.mention} you took a long time to choose a card and lost, try again later!')
                playingchannelslist.remove(ctx.channel.id)
                playingplayerslist.remove(ctx.author.id) 
                return None 
            else:
                await res.respond(type=6)
                buttons2[int(res.component.label)-1] = Button(style=ButtonStyle.red, label=res.component.label, disabled=True)
                await msg.edit(embed=embed,components=[buttons2])
                pdiff = 0 
                mdiff = 0
                scard = hand[int(res.component.label) - 1]
                hand.remove(scard)
                pdiff = card[2] - scard[3]
                mdiff = card[4] - scard[5]
                if pdiff > 0 or mdiff > 0:
                    section = f'__{ename}\'s **{card[0]}**__ dealt '
                    if pdiff > 0:
                        hhp -= pdiff
                        section +=  f'**{pdiff}** :boom: Physical Damage'
                    if section.endswith('Damage') and mdiff > 0:
                        section += ' and ' 
                    if mdiff > 0:
                        hhp -= mdiff
                        section += f'**{mdiff}** :comet: Magical Damage'
                    section += f' to __{ctx.author.name}__\n' 
                    stuff += section 
                pdiff = scard[2] - card[3]
                mdiff = scard[4] - card[5]
                if pdiff > 0 or mdiff > 0:
                    section = f'__{ctx.author.name}\'s **{scard[0]}**__ dealt '
                    if pdiff > 0:
                        mhp -= pdiff
                        section +=  f'**{pdiff}** :boom: Physical Damage'
                    if section.endswith('Damage') and mdiff > 0:
                        section += ' and ' 
                    if mdiff > 0:
                        mhp -= mdiff
                        section += f'**{mdiff}** :comet: Magical Damage'
                    section += f' to __{ename}__\n' 
                    stuff += section
        won = False
        if hhp <= 0:
            won = False
            await ctx.send(f'Unfortunately you lost, better luck next time {ctx.author.mention}')
            losses = table.execute(f'SELECT losses FROM main WHERE id = {ctx.author.id}')[0][0]
            table.execute(f'UPDATE main SET losses = {losses+1} WHERE id = {ctx.author.id}')
        elif mhp<=0:
            won = True 
            gold = random.randrange(enemy[2],enemy[3]+1)
            xpg = random.randrange(enemy[4],enemy[5]+1)
            await ctx.send(f'Congratulations {ctx.author.mention}, you won! (**+{gold}** gold, **+{xpg}** xp)')
            wins, bal, xp = table.execute(f'SELECT wins, bal, xp FROM main WHERE id = {ctx.author.id}')[0]
            table.execute(f'UPDATE main SET wins = {wins+1}, bal = {bal+gold}, xp = {xp+xpg} WHERE id = {ctx.author.id}')
            await levelUp(ctx, ctx.author.id, table, client)
        playingchannelslist.remove(ctx.channel.id)
        playingplayerslist.remove(ctx.author.id)
        table.commit()
        return won

class game(commands.Cog): 
    
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def start(self, ctx):
        table = await initialize_database()
        _check = await start_check(table, ctx.author.id)
        if _check is True:
            await ctx.message.reply('ummm, it seems you already have an account, maybe a mistake?')
            return
        table.execute(f'INSERT INTO main(id) VALUES({ctx.author.id})')
        amount = table.execute("SELECT id FROM main")
        table.commit()
        table.close()
        await ctx.message.reply('Sweet, you have created your account, now time to start playing!')
        await DiscordLog(self.client, 860055027816726578, f"{ctx.author} has created an account, now we have **{len(amount)}** players!")

    @commands.command(aliases=['p'])
    async def profile(self, ctx, user:discord.Member=None):
        table = await initialize_database()
        _check = await start_check(table, ctx.author.id)
        if _check is False:
            await ctx.message.reply('oh, it seems you don\'t have an account, would you mind making one using the start command?')
            return 
        if user is None:
            user = ctx.author
        _check = await start_check(table, user.id)
        if _check is False:
            await ctx.message.reply(f'oh, sadly it seems that {user.name} dosen\'t have a profile yet')
            return
        data = table.execute(f'SELECT bal, lvl, xp, wins, losses, hp, maxfloor FROM main WHERE id = {user.id}')[0]
        denom = 1
        if data[4] > 0: denom = data[4]
        req, preq= await reqXp(data[1])
        embed=discord.Embed(title=f'{user.name}\'s profile', description=f'Balance: {data[0]} gold\nHp: {data[5]}\nLevel: {data[1]} ({data[2]-preq}/{req-preq}XP)\nWins/Losses: {data[3]}/{data[4]} (K/D:{round(data[3]/denom, 2)})\nMax Floor: {data[6]}', colour=ebt.embed_colour)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.message.reply(embed=embed)

    @commands.command(aliases=['bal', 'gold', 'g'])
    async def balance(self, ctx, user:discord.Member=None):
        table = await initialize_database()
        _check = await start_check(table, ctx.author.id)
        if _check is False:
            await ctx.message.reply('oh, it seems you don\'t have an account, would you mind making one using the start command?')
            return 
        if user is None:
            user = ctx.author
        _check = await start_check(table, user.id)
        if _check is False:
            await ctx.message.reply(f'oh, sadly it seems that {user.name} dosen\'t have a profile yet')
            return
        bal = table.execute(f'SELECT bal FROM main WHERE id = {user.id}')[0][0]
        await ctx.message.reply(f'{user.name} has **__{bal}__** gold')

    @commands.command()
    async def cards(self, ctx):
        table = await initialize_database()
        _check = await start_check(table, ctx.author.id)
        if _check is False:
            await ctx.message.reply('oh, it seems you don\'t have an account, would you mind making one using the start command?')
            return
        embed = discord.Embed(title='**Cards:**', colour=ebt.embed_colour)
        cards = table.execute('SELECT name, patk, pdef, matk, mdef FROM chars')
        for i in cards:
            data = '{} :boom: | {} :comet:\n{} :shield: | {} :trident:'.format(i[1],i[3],i[2],i[4])
            embed.add_field(name=i[0],value=data, inline=True)
        embed.set_footer(text=f'showing {len(cards)} cards')
        await ctx.message.reply(embed=embed)        
        
    @commands.command(aliases=['ci', 'cinfo'])
    async def info(self, ctx, *, name):
        table = await initialize_database()
        _check = await start_check(table, ctx.author.id)
        if _check is False:
            await ctx.message.reply('oh, it seems you don\'t have an account, would you mind making one using the start command?')
            return 
        def embedify(char):
            enemy = table.execute(f'SELECT moneyl, moneyh, xpl, xph, hp FROM enemies WHERE name = "{char[1]}"')
            enemystr = str() 
            if enemy != []:
                enemy = enemy[0]
                floor = table.execute(f'SELECT id, boss, lvll, lvlh FROM floors WHERE show = "{char[2]}"')[0]
                moneyl = enemy[0]
                moneyh = enemy[1]
                xpl = enemy[2]
                xph = enemy[3] 
                hp = enemy[4]
                bossstr = str() 
                if char[1] == floor[1]:
                    bossstr = 'Boss'
                    for i in range(floor[3]):
                        hp = math.floor(hp*1.05)
                        moneyl = math.floor(moneyl*1.05)
                        moneyh = math.floor(moneyh*1.05)
                        xpl = math.floor(xpl*1.05)
                        xph = math.floor(xph*1.05)
                else:
                    bossstr = 'Enemy'
                    for i in range(floor[2]):
                        xpl = math.floor(xpl*1.05)
                        moneyl = math.floor(moneyl*1.05)
                        hp = math.floor(hp*1.05)
                    for i in range(floor[3]):
                        xph = math.floor(xph*1.05)
                        moneyh = math.floor(moneyh*1.05)
                        hph = math.floor(hp*1.05)
                    hp = f'{hp} - {hph}'
                enemystr = f'\n\n**{bossstr} Data:**\nFloor: {floor[0]}\nXP: {xpl} - {xph}\nGold: {moneyl} - {moneyh}\nHP: {hp}'
            embed=discord.Embed(title=char[1], description=f'Physical Attack: {char[5]} :boom:\nPhysical Defence: {char[6]} :shield:\nMagical Attacks: {char[7]} :comet:\nMagical Defence: {char[8]} :trident:\nRarity: {char[3]}\nPack: {char[2]}{enemystr}',colour=ebt.embed_colour)
            embed.set_image(url=char[4])
            embed.set_footer(text =f'id: {char[0]}')
            return embed
        if name.isdigit():
            data=table.execute(f"SELECT * FROM chars WHERE id = {int(name)}")
        else:
            data = table.execute(f"SELECT * FROM chars WHERE name LIKE '%{name}%'")
        if len(data) == 0:
            await ctx.send('It seems that the character you are looking sadly for doesn\'t exist')
        elif len(data) == 1:
            await ctx.message.reply(embed=embedify(data[0])) 
        else:
            for i in data:
                if i[1].lower() == name.lower():
                    await ctx.message.reply(embed=embedify(i))
                    return
            matches = str() 
            for i in data:
                matches += f'**__{i[1]}__**\n'
            await ctx.message.reply('**More than one character matched you search, please specify which one of the following characters you are looking for:**\n' +matches) 
        
    @commands.command(aliases=['inv']) 
    async def inventory(self, ctx):
        table = await initialize_database()
        _check = await start_check(table, ctx.author.id)
        if _check is False:
            await ctx.message.reply('oh, it seems you don\'t have an account, would you mind making one using the start command?')
            return
        cards = table.execute(f'SELECT cards FROM main WHERE id = {ctx.author.id}')[0][0]
        cards = json.loads(cards)
        cardstr = str() 
        a = 0
        for i in cards:
            a += 1
            name = table.execute(f'SELECT name FROM chars WHERE id = {i}')[0][0]
            cardstr += f'{a} - **__{name}__**\n'
        await ctx.message.reply(embed=discord.Embed(title='**Your Inventory**', description='\n'+cardstr, colour=ebt.embed_colour))
        
    @commands.command() 
    async def deck(self, ctx):
        table = await initialize_database()
        _check = await start_check(table, ctx.author.id)
        if _check is False:
            await ctx.message.reply('oh, it seems you don\'t have an account, would you mind making one using the start command?')
            return
        cards = table.execute(f'SELECT deck FROM main WHERE id = {ctx.author.id}')[0][0]
        cards = json.loads(cards)
        cardstr = str() 
        a = 0
        for i in cards:
            a += 1
            name = table.execute(f'SELECT name FROM chars WHERE id = {i}')[0][0]
            cardstr += f'{a} - **__{name}__**\n'
        await ctx.message.reply(embed=discord.Embed(title='**Your Deck**', description='\n'+cardstr, colour=ebt.embed_colour)) 
        
    @commands.command(aliases=['swap']) 
    async def replace(self, ctx, deckid, invid):
        table = await initialize_database()
        _check = await start_check(table, ctx.author.id)
        if _check is False:
            await ctx.message.reply('oh, it seems you don\'t have an account, would you mind making one using the start command?')
            return
        deck = table.execute(f'SELECT deck FROM main WHERE id = {ctx.author.id}')[0][0]
        inv = table.execute(f'SELECT cards FROM main WHERE id = {ctx.author.id}')[0][0]
        deck = json.loads(deck)
        inv = json.loads(inv)
        if invid.isdigit():
            invid = int(invid)
        else:
            await ctx.message.reply('Please choose a valid card to replace with')
            return
        if deckid.isdigit():
            deckid = int(deckid)
        else:
            await ctx.message.reply('Please choose a valid card to replace')
            return
        if invid < 0 or invid > len(inv):
            await ctx.message.reply('Please choose a valid card to replace with')
            return
        if deckid < 0 or deckid > len(deck):
            await ctx.message.reply('Please choose a valid card to replace')
            return
        dcard = deck[deckid-1]
        icard = inv[invid-1]
        dcardi = table.execute(f'SELECT name, id FROM chars WHERE id = {dcard}')[0]
        icardi = table.execute(f'SELECT name, id FROM chars WHERE id = {icard}')[0]
        await ctx.message.reply(f'Are you sure you want to replace **{dcardi[0]}** with **{icardi[0]}**? (type "y")')
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() in ['y', 'ye', 'yea', 'yeah', 'yup', 'ya', 'yee', 'sure', 'ofc', 'ofcourse ', 'of course', 'yes', 'ok', 'okay', 'oki', 'okey', 'k', 'kk', 'okok', 'oke', 'alright']
        message = await self.client.wait_for('message', timeout=60.0,check=check)
        deck[deckid-1] = icardi[1]
        inv[invid-1] = dcardi[1]
        deck = json.dumps(deck)
        inv = json.dumps(inv)
        table.execute(f'UPDATE main SET deck = "{deck}" WHERE id = {ctx.author.id}')
        table.execute(f'UPDATE main SET cards = "{inv}" WHERE id = {ctx.author.id}')
        table.commit() 
        table.close() 
        await message.reply(f'successfully replaced **{dcardi[0]}** with **{icardi[0]}**!')
    
    @commands.command() 
    async def pack(self, ctx, packname):
        table = await initialize_database()
        _check = await start_check(table, ctx.author.id)
        if _check is False:
            await ctx.message.reply('oh, it seems you don\'t have an account, would you mind making one using the start command?')
            return
        packinfo = table.execute(f'SELECT * FROM packs WHERE name = "{packname}"')
        if packinfo == []:
            await ctx.message.reply('The pack you are trying to buy doesn\'t exist')
            return
        packinfo = packinfo[0]
        bal = table.execute(f'SELECT bal FROM main WHERE id = {ctx.author.id}')[0][0]
        if bal < packinfo[1]:
            await ctx.send(f'You only have **__{bal}__** gold and a **{packinfo[0]}** pack costs **{packinfo[1]}** gold')
            return 
        await ctx.message.reply(f'You spent **{packinfo[1]}** gold and got.....')  
        async with ctx.channel.typing():
            ocards = table.execute(f'SELECT cards FROM main WHERE id = {ctx.author.id}')[0][0]
            ocards = json.loads(ocards)
            cards = list() 
            for i in range(3):
                a = random.randrange(1, 101)
                if a <= packinfo[5]:
                    rank = 'gold'
                elif a <= packinfo[5]+packinfo[4]:
                    rank = 'silver'
                elif a <= packinfo[5]+packinfo[4]+packinfo[3]:
                    rank = 'bronze'
                cards.append(table.execute(f'SELECT id, name, imgurl, rarity FROM chars WHERE rarity = "{rank}" ORDER BY RANDOM() LIMIT 1')[0]) 
            urls = list()
            cardstr = str() 
            for i in cards:
                urls.append(i[2])
                ocards.append(i[0])
                cardstr += f'\n**{i[3]} __{i[1]}__**\n'
            ocards = json.dumps(ocards)
            table.execute(f'UPDATE main SET cards = "{ocards}", bal = {bal-packinfo[1]} WHERE id = {ctx.author.id}')
            table.commit() 
            table.close() 
            embed = discord.Embed(title=f'**{packinfo[0].capitalize()}** pack opened', description='​' +cardstr+'​', colour=ebt.embed_colour)
            embed.set_image(url="attachment://image0.png")
            file = await merge(urls, 0)
            await asyncio.sleep(1)
        await ctx.message.reply(embed=embed, file=file)
        
    @commands.command() 
    async def shop(self, ctx):
        table = await initialize_database()
        _check = await start_check(table, ctx.author.id)
        if _check is False:
            await ctx.message.reply('oh, it seems you don\'t have an account, would you mind making one using the start command?')
            return 
        embed = discord.Embed(title='**Pack Shop**', colour=ebt.embed_colour)
        packs = table.execute('SELECT name, price, bronze, silver, gold FROM packs')
        for i in packs:
            embed.add_field(name=f'**{i[0].capitalize()}** pack - **__{i[1]}__** gold',   value=f'bronze: {i[2]}% | silver: {i[3]}% | gold: {i[4]}%', inline=False)
        embed.set_footer(text='to buy a pack do ".pack <name of the pack>" ')
        await ctx.message.reply(embed=embed)
        
    @commands.command(aliases=['bt']) 
    async def battle(self, ctx):
        table = await initialize_database()
        _check = await start_check(table, ctx.author.id)
        if _check is False:
            await ctx.message.reply('oh, it seems you don\'t have an account, would you mind making one using the start command?')
            return 
        floor = table.execute(f'SELECT currfloor FROM main WHERE id = {ctx.author.id}')[0][0]
        floori = table.execute(f'SELECT * FROM floors WHERE id = {floor}')[0]
        enemy = table.execute(f'SELECT * FROM enemies WHERE show = "{floori[1]}" AND name != "{floori[2]}" ORDER BY RANDOM() LIMIT 1')[0]
        lvl = random.randrange(floori[3], floori[4]+1)
        enemy = list(enemy)
        enemy.append(lvl)
        for i in range(lvl):
            enemy[6] = math.floor(enemy[6]*1.05)
            enemy[5] = math.floor(enemy[5]*1.05) 
            enemy[4] = math.floor(enemy[4]*1.05)
            enemy[3] = math.floor(enemy[3]*1.05)
            enemy[2] = math.floor(enemy[2]*1.05)
        await fight(table, self.client, ctx, enemy) 
        
    @commands.command() 
    async def boss(self, ctx):
        table = await initialize_database()
        _check = await start_check(table, ctx.author.id)
        if _check is False:
            await ctx.message.reply('oh, it seems you don\'t have an account, would you mind making one using the start command?')
            return 
        floor, maxfloor = table.execute(f'SELECT currfloor, maxfloor FROM main WHERE id = {ctx.author.id}')[0]
        floori = table.execute(f'SELECT * FROM floors WHERE id = {floor}')[0]
        enemy = table.execute(f'SELECT * FROM enemies WHERE show = "{floori[1]}" AND name = "{floori[2]}"')[0]
        lvl = floori[4]
        enemy = list(enemy)
        enemy.append(lvl)
        for i in range(lvl):
            enemy[6] = math.floor(enemy[6]*1.05)
            enemy[5] = math.floor(enemy[5]*1.05) 
            enemy[4] = math.floor(enemy[4]*1.05)
            enemy[3] = math.floor(enemy[3]*1.05)
            enemy[2] = math.floor(enemy[2]*1.05)
        won = await fight(table, self.client, ctx, enemy) 
        if floor == maxfloor and won is True:
            table.execute(f'UPDATE main SET maxfloor = {floor+1} WHERE id = {ctx.author.id}')
            await ctx.send(f'You have beaten the floor **{floor}** boss and now can enter floor **{floor+1}**')
        table.commit() 
        table.close() 
        
    @commands.command(aliases=['fl']) 
    async def floor(self, ctx, floor):
        table = await initialize_database()
        _check = await start_check(table, ctx.author.id)
        if _check is False:
            await ctx.message.reply('oh, it seems you don\'t have an account, would you mind making one using the start command?')
            return 
        if not floor.isdigit():
            await ctx.message.reply('Please enter a valid floor to travel to')
            return
        floor = int(floor)
        currfloor = table.execute(f'SELECT currfloor FROM main WHERE id = {ctx.author.id}')[0][0]
        if floor == currfloor:
            await ctx.message.reply(f'You are already in floor **{floor}**')
            return 
        maxfloor = table.execute(f'SELECT maxfloor FROM main WHERE id = {ctx.author.id}')[0][0]
        floors = table.execute('SELECT id FROM floors')
        if floor <= 0 or floor > len(floors):
            await ctx.message.reply('Please enter a valid floor to travel to')
            return
        if floor > maxfloor:
            await ctx.message.reply('You haven\'t unlocked this floor yet')
            return
        table.execute(f'UPDATE main SET maxfloor = {floor} WHERE id = {ctx.author.id}')
        await ctx.message.reply(f'You have successfully traveled to floor **{floor}**')
        table.commit() 
        table.close() 
        
    @commands.command(aliases=['gamble']) 
    async def bet(self, ctx, amount, face):
        table = await initialize_database()
        _check = await start_check(table, ctx.author.id)
        if _check is False:
            await ctx.message.reply('oh, it seems you don\'t have an account, would you mind making one using the start command?')
            return 
        bal = table.execute(f"SELECT bal FROM main WHERE id = {ctx.author.id}")[0][0]
        d1 = {"half":2,"all":1,"quarter":4}
        d2 = {"k":1000, "m":1000000, "b":1000000000}
        d3 = [["h", "heads"], ["t", "tails"]]
        d4 = ["h", "heads", "t", "tails"]
        if amount.lower() in d1:
            amount = math.floor(bal/d1[amount.lower()])
        elif amount.lower()[-1] in d2:
            amount = math.floor(float(amount[:-1])*d2[amount.lower()[-1]])
        else:
            try:
                amount =int(math.floor(float(amount))) 
            except:
                await ctx.message.reply('please enter a valid amount of gold to gamble') 
                return
        if amount <= 0:
            await ctx.message.reply('You must choose an amount above 0 to gamble')
            return
        if amount > bal:
            await ctx.message.reply(f'You only have **__{bal}__** gold')
            return
        if not face.lower() in d4:
            await ctx.message.reply("Please choose either heads (h) or tails (t) to gamble")
            return
        result=random.choice(d3) 
        if face.lower() in result:
            t="You won!"
            table.execute(f'UPDATE main SET bal = {bal+(math.floor(amount*.8))} WHERE id = {ctx.author.id}')
            c = discord.Colour.green() 
            desc = f'You won **__{math.floor(amount*.8)}__** gold'
        else:
            t="You lost..."
            table.execute(f'UPDATE main SET bal = {bal-amount} WHERE id = {ctx.author.id}') 
            c = discord.Color.red()
            desc=f'You lost **__{amount}__** gold'
        embed=discord.Embed(title=f'{t} the coin landed on {result[1]}',colour=c, description=desc)
        await ctx.message.reply(embed=embed)
        table.commit() 
        table.close() 
        
    @commands.command(aliases=['transfer', 'pay']) 
    async def give(self, ctx, user:discord.Member, amount):
        table = await initialize_database()
        _check = await start_check(table, ctx.author.id)
        if _check is False:
            await ctx.message.reply('oh, it seems you don\'t have an account, would you mind making one using the start command?')
            return 
        if user.bot:
            await ctx.message.reply('why are you trying to give money to a bot? they can\'t really use it')
            return 
        if user == ctx.author:
            await ctx.message.reply('...')
            return
        _check = await start_check(table, user.id)
        if _check is False:
            await ctx.message.reply(f'oh, sadly it seems that {user.name} dosen\'t have a profile yet')
            return 
        bal = table.execute(f"SELECT bal FROM main WHERE id = {ctx.author.id}")[0][0]
        d1 = {"half":2,"all":1,"quarter":4}
        d2 = {"k":1000, "m":1000000, "b":1000000000}
        if amount.lower() in d1:
            amount = math.floor(bal/d1[amount.lower()])
        elif amount.lower()[-1] in d2:
            amount = math.floor(float(amount[:-1])*d2[amount.lower()[-1]])
        else:
            try:
                amount =int(math.floor(float(amount))) 
            except:
                await ctx.message.reply('please enter a valid amount of gold to transfer') 
                return
        if amount <= 0:
            await ctx.message.reply('You must choose an amount above 0 to transfer')
            return
        if amount > bal:
            await ctx.message.reply(f'You only have **__{bal}__** gold')
            return
        bal2 = table.execute(f'SELECT bal FROM main WHERE id = {user.id}')[0][0]
        table.execute(f'UPDATE main SET bal = {bal-math.floor(amount)} WHERE id = {ctx.author.id}')
        table.execute(f'UPDATE main SET bal = {bal2+math.floor(amount)} WHERE id = {user.id}')
        await ctx.message.reply(f'Successfully transferred **__{math.floor(amount)}__** to **{user.name}**')
        table.commit() 
        table.close() 

    @commands.command() 
    async def exec(self, ctx, *, command):
        if not ctx.author.id == 559226493553737740:
            return
        await ctx.message.reply(exec(command)) 

    @commands.command() 
    async def eval(self, ctx, *, command):
        if not ctx.author.id == 559226493553737740:
            return
        await ctx.message.reply(eval(command)) 
 

def setup(client):
    client.add_cog(game(client))
