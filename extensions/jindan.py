import discord
from discord.ext import commands
import datetime
import config
import hcskr
import utils
import config
class JindanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.logger = bot.logger
        self.check = utils.check(bot.db)
        check = self.check
        for cmds in self.get_commands():
            if str(cmds) == "가입": continue
            cmds.add_check(self.check.registered)
        

    @commands.command(name="가입",usage=f"")
    async def register(self, ctx):
        """
        진단아 가입
        """
        if await self.db.users.find_one({"discordId":ctx.author.id}):
            raise utils.exceptions.AlreadyRegistered
        embed = utils.prompt_embed(None,"* 동의를 거부할 수 있으며, 동의 거부시 서비스 이용에 일부 제한 될 수 있습니다.\n이 자가진단 봇 이용으로 일어난 모든 책임은 사용자 에게 있습니다.\n\n**- 공지\n 이 스크립트는 건강상의 문제가 없을 경우, 브라우저를 열고 복잡한 인증 절차를 거칠 필요 없이 하나의 명령어로 빠르게 자가진단을 마치기 위해서 개발되었습니다. 실행 전 반드시 개인 건강상태를 확인해주시길 바랍니다.**\n\n- 혹여나 유증상인데 이미 앱에서 무증상으로 제출했다면 자가진단 홈페이지에 직접 접속해서 다시 제출하시길 바랍니다.",f'이용약관에 동의하시면 체크 이모지를 눌러주세요!',ctx.author)
        embed.add_field(name="개인 정보 수집 동의", value=f"``자가진단 봇 에서는 서비스 이용 등 서비스 제공을 위해 아래와 같은 최소한의 개인정보를 수집 하고 있습니다.``", inline= False)
        embed.add_field(name="1. 수집하는 개인정보의 항목", value=f"``이름``,``생년월일``,``학교``,``학급``,``지역``,``자가진단 비밀번호``", inline= False)
        embed.add_field(name="2. 개인정보 수집 방법", value=f"``이용약관 동의 후 명령어 : 진단아 설정 [ 개인정보 ] 입력으로 정보를 수집 합니다.``", inline= False)
        embed.add_field(name="3. 개인정보의 수집 및 이용 목적", value=f"``자동 자가진단 기능을 사용 하기 위해 수집 합니다.``", inline=False)
        embed.add_field(name="4. 개인정보 저장 방법 및 정보보호", value=f"``사용자의 개인정보는 모두 HS256암호화 되어 안전하게 저장됩니다.``", inline= False)
        embed.add_field(name="5. 개인정보의 보유 및 이용기간", value=f"``자가진단 봇의 서비스 종료일 까지.``", inline= False)
        embed.add_field(name="개인정보 제 3자 제공 안내", value=f"``자가진단 봇 에서는 수집된 정보를 제3자에게 제공하지 않습니다.``", inline= False)
        embed.add_field(name="🔔 교육의 목적으로 개인정보 일부 사용", value=f"학교에서 발표를 목적으로 완전한 개인 정보가 아닌, 지역과 학급 같은 단순 통개 자료를 사용함에 동의 함으로 간주합니다.", inline= False)
        msg = await ctx.reply(embed=embed)
        if await utils.is_confirmed(ctx, msg):
            await self.db.users.insert_one({"discordId": ctx.author.id})
            await msg.edit(embed=utils.success_embed(f"{config.yes_emoji} 이용약관에 성공적으로 동의 하셨습니다.",None,author=ctx.author))
        else:
            await msg.edit(embed=utils.error_embed(f"{config.no_emoji} 이용약관 동의를 취소하였습니다.",None,author=ctx.author))
    
    @commands.command(name="설정",usage=f"[이름] [비밀번호] [생년월일6자] [지역권] [학교급] [학교]")
    @commands.dm_only()
    async def SetJindan(self, ctx, name:str, password:str, birthday:str, area:str, level:str, schoolname:str):
        """
        자가진단 기능을 이용하기 위해서 개인정보를 등록합니다.
        사용자의 개인정보는 안전하게 암호화 되어 저장됩니다.
        """
        
        hcskr_result = await hcskr.asyncGenerateToken(name, birthday, area, schoolname, level, password)
        if hcskr_result['error']:
            return await ctx.reply(embed=utils.error_embed(f"{config.no_emoji} 자가진단 설정 실패",f"```{hcskr_result['message']}```",author=ctx.author))
        token = hcskr_result['token']
        try:
            await self.db.users.find_one_and_replace({"discordId":ctx.author.id},{"discordId": ctx.author.id, "token": token})
        except Exception as e:
            return print(e)
        
        await ctx.reply(embed=utils.success_embed(f"{config.yes_emoji} 자가진단 등록 성공!","`진단아 자가진단`을 이용해 자가진단을 수행할수 있어요!",author=ctx.author))
    
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


def setup(bot):
    bot.add_cog(JindanCog(bot))