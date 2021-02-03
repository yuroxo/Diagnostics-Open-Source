import discord
from discord.ext import commands
import datetime
import config
import utils
import sys
class SupportCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.logger = bot.logger
    
    @commands.command(name="가입", usage=f"")
    @commands.guild_only()
    async def Register(self, ctx):
        """
        진단아 가입
        """
        if await self.db.users.find_one({"discordId":ctx.author.id}):
            raise utils.exceptions.AlreadyRegistered
        embed = utils.prompt_embed(None,"* 동의를 거부할 수 있으며, 동의 거부시 서비스 이용에 일부 제한 될 수 있습니다.\n이 자가진단 봇 이용으로 일어난 모든 책임은 사용자 에게 있습니다.\n\n**- 공지\n 이 스크립트는 건강상의 문제가 없을 경우, 브라우저를 열고 복잡한 인증 절차를 거칠 필요 없이 하나의 명령어로 빠르게 자가진단을 마치기 위해서 개발되었습니다. 실행 전 반드시 개인 건강상태를 확인해주시길 바랍니다.**\n\n- 혹여나 유증상인데 이미 앱에서 무증상으로 제출했다면 자가진단 홈페이지에 직접 접속해서 다시 제출하시길 바랍니다.",f'이용약관에 동의하시면 체크 이모지를 눌러주세요!',ctx.author)
        embed.add_field(name="개인 정보 수집 동의", value=f"``자가진단 봇 에서는 서비스 이용 등 서비스 제공을 위해 아래와 같은 최소한의 개인정보를 수집 하고 있습니다.``", inline= False)
        embed.add_field(name="1. 수집하는 개인정보의 항목", value=f"``이름``,``생년월일``,``학교``,``학급``,``지역``,``자가진단 비밀번호``", inline= False)
        embed.add_field(name="2. 개인정보 수집 방법", value=f"``이용약관 동의 후 명령어 : {ctx.prefix}설정 [ 개인정보 ] 입력으로 정보를 수집 합니다.``", inline= False)
        embed.add_field(name="3. 개인정보의 수집 및 이용 목적", value=f"``자동 자가진단 기능을 사용 하기 위해 수집 합니다.``", inline=False)
        embed.add_field(name="4. 개인정보 저장 방법 및 정보보호", value=f"``사용자의 개인정보는 모두 HS256암호화 되어 안전하게 저장됩니다.``", inline= False)
        embed.add_field(name="5. 개인정보의 보유 및 이용기간", value=f"``자가진단 봇의 서비스 종료일 까지.``", inline= False)
        embed.add_field(name="개인정보 제 3자 제공 안내", value=f"``자가진단 봇 에서는 수집된 정보를 제3자에게 제공하지 않습니다.``", inline= False)
        msg = await ctx.reply(embed=embed)
        if await utils.is_confirmed(ctx, msg):
            await self.db.users.insert_one({"discordId": ctx.author.id})
            await msg.edit(embed=utils.success_embed(f"{config.yes_emoji} 이용약관에 성공적으로 동의 하셨습니다.", None, author=ctx.author))
            self.logger.info(f"{sys._getframe().f_code.co_name}: {ctx.author}({ctx.author.id}) 님이 이용약관에 동의하고, DB에 등록되었습니다.")
        else:
            await msg.edit(embed=utils.error_embed(f"{config.no_emoji} 이용약관 동의를 취소하였습니다.",None,author=ctx.author))
    @commands.command(name="도움말", usage=f"")
    async def Help(self, ctx):
        embed = utils.info_embed(f"{self.bot.user.name} 도움말", f">>> [**초대하기**](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=650368&scope=bot)", author=ctx.author)
        embed.add_field(name=f"{ctx.prefix}도움말", value=f"``{self.bot.user.name}의 정보와 명령어를 알려 줍니다.``", inline= False)
        embed.add_field(name=f"{ctx.prefix}가입", value=f"``{self.bot.user.name} 서비스에 가입합니다.``", inline= False)
        embed.add_field(name=f"{ctx.prefix}설정 [이름] [비밀번호] [생년월일6자] [지역권] [학교급] [학교]", value=f"``자가진단 기능에 필요한 정보를 설정 합니다.``", inline= False)
        embed.add_field(name=f"{ctx.prefix}탈퇴", value=f"``더 이상 사용하기 싫거나 정보를 삭제해야 할 때 탈퇴를 하면 회원정보가 제거됩니다.``", inline= False)
        embed.add_field(name=f"{ctx.prefix}자가진단", value=f"``자동 자가진단을 수행 합니다.``", inline= False)
        embed.add_field(name=f"{ctx.prefix}정보", value=f"``서포트서버/개발자/서버상태 등 봇의 정보를 알려 줍니다.``", inline=False)
        await ctx.reply(embed=embed)
    @commands.command(name="정보")
    async def Info(self, ctx):
        text = ""
        if ctx.channel.type != discord.ChannelType.private:
            text += f"`이 서버의 Shard ID: {ctx.guild.shard_id}`\n"
        text += "```"
        for shard in self.bot.shards.values():
            text += f"Shard#{shard.id}: {int(shard.latency*1000)}ms\n"
        text += "```"
        embed = utils.info_embed(author=ctx.author)
        embed.add_field(name="개발자", value=f">>> <@435841275632287745> 2020/12/17 ~\n<@687623503985508380> 2021/02/01 ~")
        embed.add_field(name="사용 모듈", value=f">>> **[Hcskr](https://github.com/331leo/hcskr_python)** 오픈소스를 이용해 제작된 봇입니다")
        embed.add_field(name="프사 정보", value=f"- 수세밀네님 커미션 \n>>> 인스타그램 : @susamilneh\n디스코드 : Susamilneh#1000\n이메일 : sumichip0215@naver.com ")
        embed.add_field(name="서버 상태(핑)", value=text)
        embed.set_image(url='https://media.discordapp.net/attachments/789461017813712908/800991990568845352/Untitled-1.png')
        await ctx.reply(embed=embed,content='https://discord.gg/XnAqJW2huv')
def setup(bot):
    bot.add_cog(SupportCog(bot))
        