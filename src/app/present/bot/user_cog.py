from discord.ext import commands

from src.dependencies import user_use_case


class UserCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create_user', aliases=['cu'], help='{cu, create_user} 유저 생성 기능 예) !cu password')
    async def cu(self, ctx, *, user_input: str):
        ret = user_use_case.create_user(
            user_id=ctx.author.name,
            password=user_input
        )
        await ctx.send(f'생성 완료, {ret.user_id}!')


async def setup(bot):
    await bot.add_cog(UserCog(bot))
