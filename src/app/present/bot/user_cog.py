from discord.ext import commands


class UserCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create_user', aliases=['cu'], help='{cu, create_user} 유저 생성 기능 ')
    async def cu(self, ctx):
        await ctx.send(f'아직 만드는 중, {ctx.author.name}!')


async def setup(bot):
    await bot.add_cog(UserCog(bot))
