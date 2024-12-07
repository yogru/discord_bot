from discord.ext import commands

from src.dependencies import user_use_case, auth_use_case


class UserCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create_user', aliases=['cu'], help='{cu, create_user} 유저 생성 기능 예) !cu password')
    async def create_user(self, ctx, *, user_input: str):
        ret = user_use_case.create_user(
            user_id=ctx.author.name,
            password=user_input
        )
        await ctx.send(f'생성 완료, {ret.user_id}!')

    @commands.command(name='create_user_by_admin', aliases=['cua'],
                      help='{create_user_by_admin, cua} 유저 생성 기능 예) !cua user_id password')
    async def create_user_by_admin(self, ctx, *, user_input: str):
        auth_use_case.check_admin(
            user_id=ctx.author.name,
        )
        split_result = user_input.split(' ')
        ret = user_use_case.create_user(
            user_id=split_result[0],
            password=split_result[1]
        )
        await ctx.send(f'생성 완료, {ret.user_id}!')

    @commands.command(name='grant_user', aliases=['gu'],
                      help='{grant_user, gu} 유저에게 권한 부여 기능 예) !gu username [grantType]')
    async def grant_user(self, ctx, *, user_input: str):
        auth_use_case.check_admin(
            user_id=ctx.author.name,
        )
        split_result = user_input.split(' ')
        ret = user_use_case.grant_user(
            user_id=split_result[0],
            grant_str=split_result[1]
        )
        await ctx.send(f'권한 부여 완료, {ret.user_id}!')


async def setup(bot):
    await bot.add_cog(UserCog(bot))
