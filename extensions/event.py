import discord
from discord.ext import commands
import utils
import config

class CheckCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.logger = bot.logger
        self.check = utils.check(bot.db)
    
    @commands.Cog.listener()
    async def on_guild_join(self, ctx):
        def check(event):
            return event.target.id == client.user.id
        bot_entry = await ctx.guild.audit_logs(action=discord.AuditLogAction.bot_add).find(check)
        embed = discord.Embed(title='진단이', color=0x2F3136)
        embed.add_field(name="안녕하세요? 저는 **진단이** 입니다.", value='\n명령어를 보고 싶으시다면 ``진단아 도움말`` 을 입력하세요.\n\n>>> [**디스코드 지원 서버**](https://discord.gg/XnAqJW2huv)', inline=False)
        embed.set_footer(text=f'{guild.name} 서버에 초대해주셔서 정말로 감사합니다!')
        embed.set_image(url='https://media.discordapp.net/attachments/789461017813712908/800991990568845352/Untitled-1.png')
        try:
            await bot_entry.user.send(embed=embed)
        except:
            pass

    @commands.Cog.listener('on_command_error')
    async def error_handle(self, ctx: commands.Context, error: Exception):
        print(error)
        if isinstance(error, utils.exceptions.NotRegistered):
            await ctx.reply(embed=utils.info_embed(f"{config.no_emoji} 가입 필요","이 명령어는 이용약관에 동의한 유저만 사용할수 있습니다. `진단아 가입`을 통해 가입을 진행해 주세요.",author=ctx.author))
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.reply(embed=utils.waring_embed(f"{config.no_emoji} 이 명령어는 DM체널에서만 이용할수 있습니다.",author=ctx.author))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(embed=utils.info_embed(f"{config.no_emoji} 올바르지 않은 사용",f"```{ctx.command.help}```올바른 사용법: `{ctx.prefix}{ctx.command} {ctx.command.usage}`",author=ctx.author))
        if isinstance(error, utils.exceptions.JindanNotRegistered):
            await ctx.reply(embed=utils.waring_embed(f"{config.no_emoji} 정보가 등록되지 않음", f"자가진단 정보가 등록되지 않았습니다. `{config.command_prefixes[0]}설정` 으로 자가진단 정보를 먼저 등록해주세요!",author=ctx.author)
def setup(bot):
    bot.add_cog(CheckCog(bot))