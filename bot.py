import asyncio

import discord
from discord.ext import commands
from src.dependencies import env, gpt

# 봇 초기화
intents = discord.Intents.default()
intents.message_content = True  # 메시지 콘텐츠 접근 허용
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError) and isinstance(error.original, RuntimeError):
        # RuntimeError의 메시지 추출
        await ctx.send(f"에러 발생 했습니다. {str(error.original)}")
    else:
        # 기타 에러 처리
        await ctx.send(f"알 수 없는 에러가 발생했습니다: {str(error)}")


# 봇이 준비되었을 때
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')


# m_dict = {
#
# }

# # 간단한 명령어 추가
# @bot.command()
# async def hello(ctx):
#     await ctx.send(f'Hello, {ctx.author.name}!')
#
#
# @bot.command()
# async def m(ctx, *, user_input: str):
#     if ctx.author.name in ["brony2684", 'flairth']:
#         d = m_dict.get(ctx.author.name, [])
#         d.append(user_input)
#         m_dict[ctx.author.name] = d
#
#
# @bot.command()
# async def mc(ctx):
#     if ctx.author.name in ["brony2684", 'flairth']:
#         m_dict[ctx.author.name] = []
#
#
# @bot.command()
# async def c(ctx, *, user_input: str):
#     if ctx.author.name in ["brony2684", 'flairth']:
#         prompt_list = m_dict.get(ctx.author.name, [])
#         messages = prompt_list.copy()
#         messages.append(user_input)
#         gpt.add_message(role='user', message=' '.join(messages))
#         ret = gpt.compilation()
#         await ctx.send(ret)
#         return
#     await ctx.send(f'선생님 돈내세요, {ctx.author.name}!')
#
#
# @bot.command()
# async def k(ctx):
#     image_url = 'https://cdn.discordapp.com/attachments/1064150890761691159/1313424686587052032/IMG_3133.webp?ex=6750158f&is=674ec40f&hm=b3173fe15dc33f799b15633b63f30dd4191b32c88880dde331b8ab446d407689&'
#     await ctx.send(image_url)


async def load_cogs():
    # Cog 동적 로드
    await bot.load_extension('src.app.present.bot.file_cog')
    await bot.load_extension('src.app.present.bot.user_cog')
    await bot.load_extension('src.app.present.bot.chat_cog')
    await bot.load_extension('src.app.present.bot.help_cog')


async def main():
    async with bot:
        await load_cogs()  # Cog 로드
        await bot.start(env.BOT_KEY)


asyncio.run(main())
