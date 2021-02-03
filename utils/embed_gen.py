import datetime
import config
import discord
import utils
from typing import Optional, Union
from discord.ext import commands
KST = datetime.timedelta(hours=9)

colormap = {
    "aqua": 0x00f1ff,
    "hotpink": 0xFF69B4,
    "yellowgreen": 0xADFF2F,
    "red": 0xff0000,
    "purple": 0x800080,
    "skyblue": 0xadd8e6,
    "lightgreen": 0x90ee90,
    "lightpink": 0xffc0cb,
    "yellow": 0xfcf794
}        

def success_embed(title: str = None, description: str = None, footer: Optional[str] = None, author:Optional[discord.User]=None):
    embed = discord.Embed(title=title,
                          description=description,
                          color=colormap['lightgreen'],
                          timestamp=datetime.datetime.utcnow()
                          )
    if author:
        embed.set_author(name=f"{author}", icon_url=str(author.avatar_url))
    if footer:
        embed.set_footer(text=footer)
    return embed
def prompt_embed(title: str = None, description: str = None, footer: Optional[str] = None, author:Optional[discord.User]=None):
    embed = discord.Embed(title=title,
                          description=description,
                          color=colormap['yellow'],
                          timestamp=datetime.datetime.utcnow()
                          )
    if author:
        embed.set_author(name=f"{author}", icon_url=str(author.avatar_url))
    if footer:  
        embed.set_footer(text=footer)
    return embed
def info_embed(title: str = None, description: str = None, footer: Optional[str] = None, author:Optional[discord.User]=None):
    embed = discord.Embed(title=title,
                          description=description,
                          color=colormap['skyblue'],
                          timestamp=datetime.datetime.utcnow()
                          )
    if author:
        embed.set_author(name=f"{author}", icon_url=str(author.avatar_url))
    if footer:
        embed.set_footer(text=footer)
    return embed
def error_embed(title: str = None, description: str = None, footer: Optional[str] = None, author:Optional[discord.User]=None):
    embed = discord.Embed(title=title,
                          description=description,
                          color=colormap['red'],
                          timestamp=datetime.datetime.utcnow()
                          )
    if author:
        embed.set_author(name=f"{author}", icon_url=str(author.avatar_url))
    if footer:
        embed.set_footer(text=footer)
    return embed
def waring_embed(title: str = None, description: str = None, footer: Optional[str] = None, author:Optional[discord.User]=None):
    embed = discord.Embed(title=title,
                          description=description,
                          color=colormap['lightpink'],
                          timestamp=datetime.datetime.utcnow()
                          )
    if author:
        embed.set_author(name=f"{author}", icon_url=str(author.avatar_url))
    if footer:
        embed.set_footer(text=footer)
    return embed