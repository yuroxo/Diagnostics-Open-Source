import os
from datetime import datetime

from discord.ext import commands

from interface import is_confirmed
import traceback
import discord
import config

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command(name="reload", aliases=["리로드"], brief="모듈 핫리로드")
    async def reload(self, ctx, path):
        if path == "*":
            for path in config.extension_list:
                await ctx.send(f"{path} 모듈을 리로드 하는중...")
                self.bot.reload_extension(path)
        else:
            await ctx.send(f"extensions.{path} 모듈을 리로드 하는중...")
            self.bot.reload_extension(f"extensions.{path}")
        
        await ctx.send(f"모듈 리로드 성공")
    @commands.command(name="shutdown", aliases=["종료"], brief="봇 종료")
    @commands.guild_only()
    async def shutdown(self, ctx: commands.Context):
        prompt = await ctx.send("봇을 종료할까요?")
        if await is_confirmed(ctx, prompt):
            await ctx.send("ㅂㅇ")
            await ctx.bot.logout()
    @commands.command(name='eval')
    async def _eval(self, ctx: commands.Context, *, arg):
        try:
            rst = eval(arg)
        except:
            evalout = f'📥INPUT: ```python\n{arg}```\n💥EXCEPT: ```python\n{traceback.format_exc()}```\n ERROR'
            print(traceback.format_exc())
            
        else:
            evalout = f'📥INPUT: ```python\n{arg}```\n📤OUTPUT: ```python\n{rst}```\n SUCCESS'
            print(rst)
        embed=discord.Embed(title='**💬 EVAL**', description=evalout)
        await ctx.send(embed=embed)

    @commands.command(name='await')
    async def _await(self, ctx: commands.Context, *, arg):
        try:
            rst = await eval(arg)
        except:
            evalout = f'📥INPUT: ```python\n{arg}```\n💥EXCEPT: ```python\n{traceback.format_exc()}```\n ERROR'
            print(traceback.format_exc())
            
        else:
            evalout = f'📥INPUT: ```python\n{arg}```\n📤OUTPUT: ```python\n{rst}```\n SUCCESS'
            print(rst)
            
        embed=discord.Embed(title='**💬 AWAIT**',  description=evalout)
        await ctx.send(embed=embed)

    


def setup(bot):
    bot.add_cog(Admin(bot))
