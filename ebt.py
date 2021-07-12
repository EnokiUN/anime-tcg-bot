import discord
import TenGiphPy
import sqlite3 
import datetime
import random
# from mal import AnimeSearch 

t = TenGiphPy.Tenor(token='HZZF1MLZR52P')

#config
embed_colour = 0xBC13FE # hex colour code with "0x" before it for the side bar of the embeds 
database_name = "at.db" # string which ends with ".db" with only normal letters before it
start_message = 'You have successfully created an account'
duplicate_start_message = 'You already have an account tho-'
do_start_message = 'oh, it appears you haven\'t started yet, use the start command to start' # the message that's sent when a user still hasn't used the start command in a command that requires it
other_member_do_start_message = 'it looks like {{member}} hasn\'t started yet' # the message that's sent when you try to get info about another member who hasn't started, use "{{member}}" to represent the member with a mention
cooldown_message = 'HEY, too quick there, you need to wait **{{remaining_time}}** before you do this again' # the message that's sent when a user is still under cooldown, use "{{remaining_time}}" to represent the remaining time
currency = '<:UacCurrency:816252229706973184>' # must be a string, if you want it to be an emoji get the name and id of the emoji and paste it in the form <:name:id>, must be a string too

class giftools():

    async def single_user_action(author, action, actionverb):
        if author.nick is None:
            author_name = author.name
        else:
            author_name = author.nick
        embed = discord.Embed(
          title = f'**{author_name}** {actionverb}',
          colour = discord.Colour(embed_colour)
        )
        embed.set_image(url=t.random(str(f'anime {action}')))
        embed.set_footer(text=f'executed by {author}')
        return embed
        
    async def two_user_action(author, target : discord.Member, action, actionverb):
        if target.nick is None:
            member_name = target.name
        else:
            member_name = target.nick
        if author.nick is None:
            author_name = author.name
        else:
            author_name = author.nick
        embed = discord.Embed(
          title = f'**{author_name}** {actionverb} **{member_name}**',
          colour = discord.Colour(embed_colour)
        )
        embed.set_image(url=t.random(str(f'anime {action}')))
        embed.set_footer(text=f'executed by {author}')
        return embed
    
    async def random_gif(content, title=discord.Embed.Empty, description=discord.Embed.Empty, footer=discord.Embed.Empty):
        embed=discord.Embed(title=title, description=description, colour=discord.Colour(embed_colour))
        if footer is not discord.Embed.Empty:
            embed.set_footer(text=footer)
        embed.set_image(url=t.random(str(content)))
        return embed

class embedtools():
    
    async def create_embed(title=discord.Embed.Empty, description=0, colour=embed_colour, footer=discord.Embed.Empty,author=discord.Embed.Empty, imgurl=discord.Embed.Empty, footerurl=discord.Embed.Empty, authorimgurl=discord.Embed.Empty, thumbnailurl=discord.Embed.Empty, url=discord.Embed.Empty, authorurl=discord.Embed.Empty, *, fields=[]):
        embed = discord.Embed(title=title, description=description, url=url, colour=discord.Colour(colour))
        if imgurl is not discord.Embed.Empty:
            embed.set_image(url=imgurl)
        if footer is not discord.Embed.Empty:
            embed.set_footer(text=footer,icon_url=footerurl)
        if thumbnailurl is not discord.Embed.Empty:
           embed.set_thumbnail(url=thumbnailurl)
        if author is not discord.Embed.Empty:
            embed.set_author(name=author, url=authorurl, icon_url=authorimgurl)
        for i in fields:
            embed.add_field(name=i[0], value=i[1], inline=i[2])
        return embed
 
class economytools():
    
    async def create_database(cooldown_command_names=[]):
        if cooldown_command_names == [] or any(type(a) != str for a in cooldown_command_names):
                return 'Error, Parameter error: Invalid argument for cooldown_command_names'
        else:
            try:
                conn = sqlite3.connect(database_name)
                c = conn.cursor() 
                c.execute("""CREATE TABLE IF NOT EXISTS 'main' (
                    'id' INT PRIMARY KEY, 
                    'bal' INT DEFAULT 0
                );
                """)
                q = "CREATE TABLE IF NOT EXISTS 'cds' (\n  'id' INT PRIMARY KEY"
                for i in cooldown_command_names:
                    q = q + f",\n  '{i}' INT DEFAULT 0"
                q = q + '\n);'
                c.execute(q) 
                conn.commit() 
                c.close()
                conn.close()
            except Exception as e:
                return e
            else:
                return 'OK'

    async def start_user(author):
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        c.execute(f'SELECT id FROM main WHERE id = {author.id}')
        if c.fetchone() is None:
            c.execute(f'INSERT INTO main(id) VALUES({author.id})')
            c.execute(f"INSERT INTO cds(id) VALUES({author.id})")
            conn.commit() 
            return start_message
        else:
            return duplicate_start_message
        c.close()
        conn.close() 

    async def edit_balance(memberid, amount, cooldown, command, msg):
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        c.execute(f'SELECT id FROM main WHERE id = {memberid}')
        if c.fetchone() is not None:
            c.execute(f'SELECT "{command}" FROM cds WHERE id = {memberid}')
            check = c.fetchone()
            if check is None:
                c.execute(f'INSERT INTO cds(id) VALUES({memberid})')
                conn.commit()
                c.execute(f'SELECT "{command}" FROM cds WHERE id = {memberid}')
                litime = c.fetchone()[0]
            else:
                litime = check[0]
            tl = (litime + cooldown) - datetime.datetime.now().timestamp()
            if tl <= 0:
                c.execute(f'SELECT bal FROM main WHERE id = {memberid}')
                bal = c.fetchone()[0]
                c.execute(f'UPDATE main SET bal = {bal + amount}    WHERE id = {memberid}')
                c.execute(f'UPDATE cds SET "{command}" = {datetime.datetime.now().timestamp()} WHERE id = {memberid}') 
                conn.commit()
                msg = msg.replace('{{amount}}', str(amount)) 
                msg = msg.replace('{{bal}}', str(bal + amount)) 
                msg = msg.replace('{{currency}}', currency)
                return msg
            else:
                ttce = ''
                if tl >= 86400:
                    ttce = str(round(tl/86400)) + ' days'
                elif tl >= 3600:
                    ttce = str(round(tl/3600)) + ' hours'
                elif tl >= 60:
                    ttce = str(round(tl/60)) + ' minutes'
                else:
                    ttce = str(round(tl, 2)) + ' seconds'
                cdmsg = cooldown_message.replace('{{remaining_time}}', ttce)
                return cdmsg
        else:
            return do_start_message
        c.close()
        conn.close()
        
    async def profile(member):
        conn = sqlite3.connect(database_name) 
        c = conn.cursor() 
        c.execute(f"SELECT bal FROM main WHERE id = {member.id}")
        check = c.fetchone() 
        if check is None:
            return other_member_do_start_message.replace('{{member}}', member.mention)
        bal = check[0]
        embed= discord.Embed(title=member.name + '\'s profile', description=f'balance: **{bal}**', colour=discord.Colour(embed_colour))
        embed.set_thumbnail(url=member.avatar_url)
        return embed, bal
        c.close()
        conn.close()
        
    async def balance_leaderboard(size):
        conn = sqlite3.connect(database_name) 
        c = conn.cursor() 
        c.execute(f'SELECT id, bal FROM main ORDER BY bal DESC LIMIT {size}')
        result = c.fetchall()
        embed = discord.Embed(title='**leaderboard**', colour=discord.Colour(embed_colour))
        for x, i in enumerate(result, 1):
            embed.add_field(name=f'#{x}', value=f' <@{i[0]}> - {i[1]} {currency}', inline=False)
        return embed, result
        c.close()
        conn.close()

class misctools():

    async def _8ball():
        options =[ "It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely", "You may rely on it", "As I see it, yes", "Most Likely", "Outlook Good", "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again", "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very Doubtful"]
        return random.choice(options)

    async def topic(keywords_lists=[], sentence_lists=[]):
        if keywords_lists == []:
                return 'Error, Parameter error: Invalid argument for keywords_lists' 
        elif sentence_lists == []:
                return 'Error, Parameter error: Invalid argument for sentence_lists' 
        else:
            abseloute_index = keywords_lists.index(random.choice(keywords_lists))
            return random.choice(sentence_lists[abseloute_index]).replace('{{keyword}}', random.choice(keywords_lists[abseloute_index]))
    
    async def avatar(member):
        embed = discord.Embed(
            title=member.name+'\'s avatar', description=f'(link)[{member.avatar_url}]', colour = discord.Colour(embed_colour))
        embed.set_image(url=member.avatar_url)
        return embed
    
    async def icon(guild):
        embed = discord.Embed(
            title=guild.name+'\'s icon', description=f'(link)[{guild.icon_url}]', colour = discord.Colour(embed_colour))
        embed.set_image(url=guild.icon_url)
        return embed
       
    async def emoji(emote):
        embed = discord.Embed(
            title=emote.name+'\'s image', description=f'(link)[{emote.url}]', colour = discord.Colour(embed_colour))
        embed.set_image(url=emote.url)
        return embed
    
    # async def anime_info(anime):
    #    search =  mal.AnimeSearch(anime)
    #    embed = ''
     #   return [search.results[0], embed]
      
class SqlTools:
    def __init__(self, table):
        self.table = str(table) + '.db'
        self.conn = sqlite3.connect(self.table)
        self.c = self.conn.cursor()

    def execute(self, query, vals=None):
        if vals is not None:
            self.c.execute(query, vals)
        else:
            self.c.execute(query)
        return self.c.fetchall()
    
    def conn(self):
        return self.conn

    def c(self):
        return self.c

    def commit(self):
        self.conn.commit()

    def close(self):
        self.c.close()
        self.conn.close()
        self = None


async def DiscordLog(client, channelId, content):
    channel = await client.fetch_channel(channelId)
    await channel.send(content)

VERSION = '0.6.8'