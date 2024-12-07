from discord.ext import commands


class UserCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='cu', aliases=['create_user'], help='유저 생성 기능')
    async def cu(self, ctx):
        await ctx.send(f'아직 만드는 중, {ctx.author.name}!')
