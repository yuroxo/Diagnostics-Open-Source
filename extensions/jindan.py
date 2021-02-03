import discord
from discord.ext import commands
import datetime
import config
import hcskr
import utils
import config
import sys
class JindanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.logger = bot.logger
        self.check = utils.check(bot.db)
        check = self.check
        for cmds in self.get_commands():
            cmds.add_check(self.check.registered)
    

    @commands.command(name="설정",usage=f"[이름] [비밀번호] [생년월일6자] [지역권] [학교급] [학교]")
    @commands.dm_only()
    async def SetJindan(self, ctx, name:str, password:str, birthday:str, area:str, level:str, schoolname:str):
        """
        자가진단 기능을 이용하기 위해서 개인정보를 등록합니다.
        사용자의 개인정보는 안전하게 암호화 되어 저장됩니다.

        사용 가능한 지역권 이름:
            서울, 부산, 대구, 인천, 광주, 대전, 울산, 세종,
            경기, 강원, 충북, 충남, 전북, 전남, 경북, 경남, 제주
        사용 가능학 학교급 이름:
            유치원, 초등학교, 중학교, 고등학교
        """
        
        hcskr_result = await hcskr.asyncGenerateToken(name, birthday, area, schoolname, level, password)
        if hcskr_result['error']:
            self.logger.info(f"{sys._getframe().f_code.co_name}: {ctx.author}({ctx.author.id}) 자가진단 설정에 실패하였습니다. => {hcskr_result['message']}")
            return await ctx.reply(embed=utils.error_embed(f"{config.no_emoji} 자가진단 설정 실패",f"```{hcskr_result['message']}```",author=ctx.author))
        token = hcskr_result['token']
        try:
            await self.db.users.find_one_and_replace({"discordId":ctx.author.id},{"discordId": ctx.author.id, "token": token})
        except Exception as e:
            return print(e)
        
        await ctx.reply(embed=utils.success_embed(f"{config.yes_emoji} 자가진단 등록 성공!", f"`{ctx.prefix}자가진단`을 이용해 자가진단을 수행할수 있어요!", author=ctx.author))
        self.logger.info(f"{sys._getframe().f_code.co_name}: {ctx.author}({ctx.author.id}) 자가진단 정보를 성공적으로 등록하였습니다!.")
    
    @commands.command(name="자가진단", usage=f"")
    async def RunJindan(self, ctx):
        """
        설정한 정보를 이용해 자가진단을 수행합니다.
        """
        await self.check.jindanRegistered(ctx)

        user_data = await self.db.users.find_one({"discordId": ctx.author.id})
        token = user_data['token']
        hcskr_result = await hcskr.asyncTokenSelfCheck(token)
        await ctx.reply(embed=utils.success_embed(f"{config.yes_emoji} 성공적으로 자가진단을 수행하였습니다!"))
        self.logger.info(f"{sys._getframe().f_code.co_name}: {ctx.author}({ctx.author.id}) 님이 자가진단을 수행하였습니다.")

    @commands.command(name="탈퇴", usage=f"")
    @commands.guild_only()
    async def Unregister(self, ctx):
        """
        진단이 DB에서 모든 데이터를 삭제하고, 탈퇴합니다.
        """
        msg = await ctx.reply(embed=utils.prompt_embed(f"정말로 {self.bot.user.name}를 탈퇴하시겠습니까?", f"모든 데이터가 DB에서 삭제됩니다.\n이에 따라 {self.bot.user.name}의 대부분의 기능을 이용하실 수 없습니다.", author=ctx.author))
        if await utils.is_confirmed(ctx,msg):
            await self.db.users.find_one_and_delete({"discordId": ctx.author.id})
            await msg.edit(embed=utils.success_embed(f"{config.yes_emoji} 성공적으로 모든 데이터를 삭제하였습니다!", f"{self.bot.user.name}를 다시 이용하시려면 `{ctx.prefix}가입`을 이용해주세요!", author=ctx.author))
            return self.logger.info(f"{sys._getframe().f_code.co_name}: {ctx.author}({ctx.author.id}) 님이 탈퇴하셨습니다.")
        await msg.edit(embed=utils.waring_embed(f"{config.no_emoji} 탈퇴 과정을 취소하였습니다."))
def setup(bot):
    bot.add_cog(JindanCog(bot))