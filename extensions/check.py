import discord
from discord.ext import commands
import utils

class CheckCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.logger = bot.logger
    @commands.Cog.listener('on_command_error')
    async def error_handle(self, ctx: commands.Context, error: Exception):
        print(error)
        if isinstance(error, utils.exceptions.NotRegistered):
            await ctx.reply("이 명령어를 이용약관에 동의한 유저만 사용할수 있습니다. `진단아 가입`을 통해 가입을 진행해 주세요.")
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.reply("이 명령어는 DM체널에서만 이용할수 있습니다.")
def setup(bot):
    bot.add_cog(CheckCog(bot))