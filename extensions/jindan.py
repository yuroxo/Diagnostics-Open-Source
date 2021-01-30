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
        check = self.check
        for cmds in self.get_commands():
            cmds.add_check(self.check.registered)

    @commands.Cog.listener('on_ready')
    async def on_ready(self):
        self.bot.get_command("가입").remove_check(self.check.registered)
        
    @commands.command(name="가입",usage=f"{config.command_prefixes[0]}가입")
    async def register(self, ctx):
        """
        진단아 가입
        """
        if await self.db.users.find_one({"discordId":ctx.author.id}):
            raise utils.exceptions.AlreadyRegistered
        msg = await ctx.reply("이용약관 ~~~~~~~~~~\n 에 동의하십니까?")
        if await utils.is_confirmed(ctx, msg):
            await self.db.users.insert_one({"discordId": ctx.author.id})
            await msg.edit(content="성공적으로 등록했습니다!")
            

        else:
            await msg.edit(content="취소되었습니다.")
    @commands.command(name="설정",usage=f"{config.command_prefixes[0]}설정 [이름] [비밀번호] [생년월일6자] [지역권] [학급] [학교]")
    @commands.dm_only()
    async def SetJindan(self, ctx, name:str, password:str, birthday:str, area:str, level:str, schoolname:str):
        """
        진단아 설정 [이름] [비밀번호] [생년월일6자] [지역권] [학급] [학교]
        """
        
        hcskr_result = await hcskr.asyncGenerateToken(name, birthday, area, schoolname, level, password)
        if hcskr_result['error']:
            return await ctx.reply(hcskr_result['message'])
        token = hcskr_result['token']
        try:
            await self.db.users.find_one_and_replace({"discordId":ctx.author.id},{"discordId": ctx.author.id, "token": token})
        except Exception as e:
            return print(e)
        embed = discord.Embed(description="")
        await ctx.reply("자가진단 등록 성공!")
    
    @commands.command(name="자가진단", usage=f"{config.command_prefixes[0]}자가진단")
    async def RunJindan(self, ctx):
        """
        진단아 자가진단
        """
        await self.check.jindanRegistered(ctx)

        user_data = await self.db.users.find_one({"discordId": ctx.author.id})
        token = user_data['token']
        hcskr_result = await hcskr.asyncTokenSelfCheck(token)
        await ctx.reply(hcskr_result['message'])


def setup(bot):
    bot.add_cog(JindanCog(bot))