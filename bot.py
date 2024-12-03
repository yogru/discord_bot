import discord
from discord.ext import commands

from src.dependencies import env

# 봇 초기화
intents = discord.Intents.default()
intents.message_content = True  # 메시지 콘텐츠 접근 허용
bot = commands.Bot(command_prefix='!', intents=intents)

# 봇이 준비되었을 때
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# 간단한 명령어 추가
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')

# 봇 실행
bot.run(env.BOT_KEY)