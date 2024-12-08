from discord.ext import commands

from src.dependencies import auth_use_case, chat_use_case
from src.domain.model import UserGrantEnum


class ChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='chat', aliases=['c'], help='{chat, c} 챗봇 기능')
    async def chat(self, ctx, *, user_input: str):
        auth_use_case.check_grant(
            user_id=ctx.author.name,
            grant_enum=UserGrantEnum.USE_CHAT_BOT
        )
        answer = chat_use_case.create_chat(
            user_id=ctx.author.name,
            question=user_input,
        )
        await ctx.send(answer)

    @commands.command(name='persona', aliases=['p'], help='{persona, p} 페르소나 추가 기능 예제)!p 제목 내용')
    async def persona(self, ctx, *, user_input: str):
        split_list = user_input.split(' ')
        if len(split_list) < 2:
            await ctx.send(f"잘못된 입력 입니다.")
            return

        auth_use_case.check_grant(
            user_id=ctx.author.name,
            grant_enum=UserGrantEnum.USE_CHAT_BOT
        )

        prompt = ' '.join(split_list[1:])

        ret = chat_use_case.create_prompt(
            user_id=ctx.author.name,
            title=split_list[0],
            prompt=prompt,
        )
        await ctx.send(f"페르소나 생성 되었습니다.{ret}")


async def setup(bot):
    await bot.add_cog(ChatCog(bot))
