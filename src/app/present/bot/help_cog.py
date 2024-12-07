import discord
from discord.ext import commands


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=['h'], help='{help, h} 조회 기능')
    async def custom_help(self, ctx):
        # 명령어 목록 생성
        commands_list = []
        for command in self.bot.commands:
            # 비공개 명령어는 제외 (hidden=True로 설정된 명령어)
            if not command.hidden:
                commands_list.append(f"**{ctx.prefix}{command.name}** - {command.help or 'No description provided'}")

        # 임베드 메시지로 출력
        embed = discord.Embed(title="Help - Available Commands", color=discord.Color.blue())
        embed.description = "\n".join(commands_list)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
