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
    

    @commands.Cog.listener('on_command_error')
    async def error_handle(self, ctx: commands.Context, error: Exception):
        print(error)
        if isinstance(error, utils.exceptions.NotRegistered):
            await ctx.reply("이 명령어를 이용약관에 동의한 유저만 사용할수 있습니다. `진단아 가입`을 통해 가입을 진행해 주세요.")
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.reply("이 명령어는 DM체널에서만 이용할수 있습니다.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"올바른 사용법: `{ctx.command.usage}`")
        if isinstance(error, utils.exceptions.JindanNotRegistered):
            await ctx.reply(f"자가진단 정보가 등록되지 않았습니다. `{config.command_prefixes[0]}설정` 으로 자가진단 정보를 먼저 등록해주세요!")
def setup(bot):
    bot.add_cog(CheckCog(bot))