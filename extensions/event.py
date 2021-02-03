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
    async def on_guild_join(self, guild):
        def check(event):
            return event.target.id == self.bot.user.id
        bot_entry = await guild.audit_logs(action=discord.AuditLogAction.bot_add).find(check)
        embed = utils.info_embed("안녕하세요? 저는 **진단이** 입니다!",f"명령어를 보고 싶으시다면 ``{config.command_prefixes[0]}도움말`` 을 입력하세요.\n\n>>> [**디스코드 지원 서버**](https://discord.gg/XnAqJW2huv)",f"{guild.name} 서버에 초대해주셔서 정말로 감사합니다!")
        embed.set_image(url='https://media.discordapp.net/attachments/789461017813712908/800991990568845352/Untitled-1.png')
        self.logger.info(f"GuildJoin: {guild.name}({guild.id}) 길드에 {bot_entry}({bot_entry.id})님이 봇을 추가하였습니다!")
        try:
            await bot_entry.user.send(embed=embed)
        except:
            pass

    @commands.Cog.listener('on_command_error')
    async def error_handle(self, ctx: commands.Context, error: Exception):
        print(error)
        if isinstance(error, utils.exceptions.NotRegistered):
            return await ctx.reply(embed=utils.info_embed(f"{config.no_emoji} 가입 필요", f"이 명령어는 이용약관에 동의한 유저만 사용할수 있습니다. `{ctx.prefix}가입`을 통해 가입을 진행해 주세요.", author=ctx.author))
        if isinstance(error, utils.exceptions.AlreadyRegistered):
            return await ctx.reply(embed=utils.error_embed(f"{config.no_emoji} 이미 가입되어 있는 이용자입니다!",footer=f"`{ctx.prefix}탈퇴` 로 가입을 해제할수 있어요!",author=ctx.author))
        if isinstance(error, commands.PrivateMessageOnly):
            return await ctx.reply(embed=utils.waring_embed(f"{config.no_emoji} 이 명령어는 DM체널에서만 이용할수 있습니다.", author=ctx.author))
        if isinstance(error, commands.NoPrivateMessage):
            return await ctx.reply(embed=utils.waring_embed(f"{config.no_emoji} 이 명령어는 길드체널(서버)에서만 이용할수 있습니다.",author=ctx.author))
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.reply(embed=utils.info_embed(f"{config.no_emoji} 올바르지 않은 사용",f"```{ctx.command.help}```올바른 사용법: `{ctx.prefix}{ctx.command} {ctx.command.usage}`",author=ctx.author))
        if isinstance(error, utils.exceptions.JindanNotRegistered):
            return await ctx.reply(embed=utils.waring_embed(f"{config.no_emoji} 정보가 등록되지 않음", f"자가진단 정보가 등록되지 않았습니다. `{config.command_prefixes[0]}설정` 으로 자가진단 정보를 먼저 등록해주세요!", author=ctx.author))
    
def setup(bot):
    bot.add_cog(CheckCog(bot))