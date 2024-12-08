import discord
from discord.ext import commands

from src.dependencies import auth_use_case, env
from src.domain.model import UserGrantEnum
from src.infra.gpt import GPT


class ChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gpt_dict = {}

    def get_gpt(self, user_id: str) -> GPT:
        gpt = self.gpt_dict.get(user_id, None)
        if gpt is None:
            self.gpt_dict[user_id] = GPT(env=env)
            return self.gpt_dict[user_id]
        return gpt

    @commands.command(name='chat', aliases=['c'], help='{chat, c} 챗봇 기능')
    async def chat(self, ctx, *, user_input: str):
        auth_use_case.check_grant(
            user_id=ctx.author.name,
            grant_enum=UserGrantEnum.USE_CHAT_BOT
        )
        gpt = self.get_gpt(user_input)
        gpt.add_message(role='user', message=user_input)
        ret = gpt.compilation()
        await ctx.send(ret)


async def setup(bot):
    await bot.add_cog(ChatCog(bot))
