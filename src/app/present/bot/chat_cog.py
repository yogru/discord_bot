import discord
from discord.ext import commands

from src.dependencies import gpt


class ChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='chat', aliases=['c'], help='{chat, c} 챗봇 기능')
    async def chat(self, ctx, *, user_input: str):
        gpt.add_message(role='user', message=user_input)
        ret = gpt.compilation()
        await ctx.send(ret)


async def setup(bot):
    await bot.add_cog(ChatCog(bot))
