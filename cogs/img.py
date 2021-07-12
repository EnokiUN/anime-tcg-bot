import json 
import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands, tasks
from discord_slash import cog_ext
import os
import random
import sqlite3
import ebt
from PIL import Image, ImageDraw, ImageFont
import requests
import time 
import io

mods = [559226493553737740]

class img(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command() 
    async def imtxt(self, ctx, url, fontsize, stroke_width, x, y, fontname, *, text):
        eimg = Image.open(requests.get(url=url, stream=True).raw)
        draw = ImageDraw.Draw(eimg) 
        font = ImageFont.truetype(f'{fontname}.ttf',int(fontsize))
        
        width, height = eimg.size
        w, h = font.getsize(text, stroke_width=int(stroke_width))
        
        if x == 'x':
            x = (width-w)/2
        if y == 'y':
            y = (height-h)/2
       
        x = int(x)
        y = int(y)
       
        draw.text((x,y), text, (0,0,0),font=font, stroke_width=int(stroke_width), stroke_fill=(256, 256,256))
        eimg.save("eimage.png")
        await ctx.message.reply(file=discord.File('eimage.png'))
    
    
    @commands.command() 
    async def fix(self, ctx, url):
        i = Image.open(requests.get(url=url, stream=True).raw) 
        i = i.resize((200,300))
        with io.BytesIO() as image_binary:
            i.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.message.reply(file=discord.File(fp=image_binary, filename='image.png'))
    
    @commands.command() 
    async def frame(self, ctx, url):
        i = Image.open(requests.get(url=url, stream=True).raw)
        width, height = i.size
        imsize = i.size[0] + i.size[1]
        new_height = imsize / 2
        new_width = imsize / 3
        left = (width - new_width) / 2
        top = (height - new_height) / 2
        right = (width + new_width) / 2
        bottom = (height + new_height) / 2
        i = i.crop((left, top, right, bottom))
        i = i.resize((200,300))
        with io.BytesIO() as image_binary:
            i.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.message.reply(file=discord.File(fp=image_binary, filename='image.png'))
        
        
    @commands.command() 
    async def merge(self, ctx, *, urlsraw):
        urls=urlsraw.split(' ')
        ims = list()
        bg = Image.open('canvas.png')
        for i in urls: 
            ims.append(Image.open(requests.get(url=i, stream=True).raw))
        for i in range(3):
            offset = (i)*200
            bg.paste(ims[i-1], (offset,0))
        with io.BytesIO() as image_binary:
            bg.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.message.reply(file=discord.File(fp=image_binary, filename='image.png'))
            
         
def setup(client):
    client.add_cog(img(client))
    