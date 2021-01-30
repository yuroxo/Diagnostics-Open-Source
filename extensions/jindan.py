import discord
from discord.ext import commands

import config
import hcskr
import utils
class JindanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.logger = bot.logger
        self.check = utils.check(bot.db)
        for cmds in self.get_commands():
            cmds.add_check(self.check.registered)
    
    @commands.command(name="설정")
    @commands.dm_only()
    async def SetJindan(self, ctx, name:str, password:str, birthday:str, area:str, level:str, schoolname:str):
        """
        진단아 설정 [이름] [비밀번호] [생년월일6자] [지역권] [학급] [학교]
        """
        hcskr_result = await hcskr.asyncGenerateToken(name, birthday, area, schoolname, level, password)
        if hcskr_result['error']:
            pass
            return
        token = hcskr_result['token']
        try:
            await self.db.users.insert_one({"discordId": ctx.author.id, "token": token})
        except Exception as e:
            return print(e)
        embed = discord.Embed(description="")
        await ctx.reply("자가진단 등록 성공!")



def setup(bot):
    bot.add_cog(JindanCog(bot))